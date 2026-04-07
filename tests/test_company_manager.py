import os
import unittest
from controllers.company_manager import CompanyManager


class TestCompanyManager(unittest.TestCase):
    """Набір модульних тестів для перевірки бізнес-логіки контролера компанії."""

    def setUp(self):
        """Підготовка ізольованого середовища перед кожним тестом.
        Створюється новий чистий екземпляр контролера."""
        self.manager = CompanyManager()

    def test_assign_equipment_success(self):
        """Перевіряє успішну видачу вільної техніки існуючому працівнику."""
        emp_id = self.manager.add_developer("Тестер", "Python")
        eq_id = self.manager.add_laptop("MacBook", "Mac")

        self.manager.assign_equipment_to_employee(emp_id, eq_id)

        developer = self.manager._find_employee_by_id(emp_id)

        self.assertEqual(len(developer.get_equipment()), 1)

    def test_laptop_limit_enforcement(self):
        """Перевіряє бізнес-логіку: працівник не може отримати більше одного ноутбука."""
        emp_id = self.manager.add_developer("Ліміт-Тестер", "Java")
        eq1_id = self.manager.add_laptop("ThinkPad", "Windows")
        eq2_id = self.manager.add_laptop("MacBook Pro", "Mac")

        self.manager.assign_equipment_to_employee(emp_id, eq1_id)

        self.manager.assign_equipment_to_employee(emp_id, eq2_id)

        developer = self.manager._find_employee_by_id(emp_id)
        laptop1 = self.manager._find_equipment_by_id(eq1_id)
        laptop2 = self.manager._find_equipment_by_id(eq2_id)

        self.assertEqual(len(developer.get_equipment()), 1)
        self.assertTrue(laptop1.get_status())
        self.assertFalse(laptop2.get_status())

    def test_add_employee_success(self):
        """Перевіряє успішне додавання працівників різних типів та їх наявність у системі."""
        self.manager.add_developer("Олексій", "Python")
        self.manager.add_manager("Марія", "HR")

        employees_count = len(self.manager._CompanyManager__employees)
        self.assertEqual(employees_count, 2)

    def test_remove_employee_success(self):
        """Перевіряє коректність видалення працівника з бази даних."""
        emp_id = self.manager.add_developer("Іван", "C++")

        self.manager.remove_employee(emp_id)

        employee = self.manager._find_employee_by_id(emp_id)
        self.assertIsNone(employee)

    def test_remove_equipment_success(self):
        """Перевіряє повне видалення техніки із системи (списання)."""
        eq_id = self.manager.add_monitor("Dell UltraSharp", "4K")

        self.manager.remove_equipment_from_system(eq_id)

        equipment = self.manager._find_equipment_by_id(eq_id)
        self.assertIsNone(equipment)

    def test_remove_assigned_equipment_fails(self):
        """Перевіряє заборону списання техніки, яка наразі закріплена за працівником."""
        emp_id = self.manager.add_developer("Дмитро", "Go")
        eq_id = self.manager.add_laptop("Lenovo Legion", "Windows")
        self.manager.assign_equipment_to_employee(emp_id, eq_id)

        self.manager.remove_equipment_from_system(eq_id)

        equipment = self.manager._find_equipment_by_id(eq_id)
        self.assertIsNotNone(equipment)
        self.assertTrue(equipment.get_status())

    def test_monitor_limit_enforcement(self):
        """Перевіряє бізнес-логіку: працівник не може отримати більше двох моніторів."""
        emp_id = self.manager.add_developer("Олег", "JavaScript")
        mon1_id = self.manager.add_monitor("LG 24", "1080p")
        mon2_id = self.manager.add_monitor("Dell 27", "1440p")
        mon3_id = self.manager.add_monitor("Samsung 32", "4K")

        self.manager.assign_equipment_to_employee(emp_id, mon1_id)
        self.manager.assign_equipment_to_employee(emp_id, mon2_id)
        self.manager.assign_equipment_to_employee(emp_id, mon3_id)

        employee = self.manager._find_employee_by_id(emp_id)
        mon3 = self.manager._find_equipment_by_id(mon3_id)

        self.assertEqual(len(employee.get_equipment()), 2)
        self.assertFalse(mon3.get_status())

    def test_assign_already_assigned_equipment(self):
        """Перевіряє неможливість видачі техніки, яка вже закріплена за іншим працівником."""
        emp1_id = self.manager.add_developer("Анна", "Python")
        emp2_id = self.manager.add_manager("Богдан", "Sales")
        lap_id = self.manager.add_laptop("HP ProBook", "Windows")

        self.manager.assign_equipment_to_employee(emp1_id, lap_id)
        self.manager.assign_equipment_to_employee(emp2_id, lap_id)

        emp2 = self.manager._find_employee_by_id(emp2_id)
        self.assertEqual(len(emp2.get_equipment()), 0)

    def test_return_equipment_success(self):
        """Перевіряє успішне повернення техніки від працівника на склад."""
        emp_id = self.manager.add_developer("Віктор", "Ruby")
        lap_id = self.manager.add_laptop("Asus ZenBook", "Windows")
        self.manager.assign_equipment_to_employee(emp_id, lap_id)

        self.manager.return_equipment(emp_id, lap_id)

        employee = self.manager._find_employee_by_id(emp_id)
        laptop = self.manager._find_equipment_by_id(lap_id)

        self.assertEqual(len(employee.get_equipment()), 0)
        self.assertFalse(laptop.get_status())

    def test_return_unassigned_equipment_fails(self):
        """Перевіряє коректну обробку спроби повернути техніку, яка не закріплена за працівником."""
        emp_id = self.manager.add_manager("Олена", "Marketing")
        mon_id = self.manager.add_monitor("Philips 24", "1080p")

        self.manager.return_equipment(emp_id, mon_id)

        employee = self.manager._find_employee_by_id(emp_id)
        monitor = self.manager._find_equipment_by_id(mon_id)

        self.assertFalse(monitor.get_status())
        self.assertEqual(len(employee.get_equipment()), 0)

    def test_search_employee_case_insensitive(self):
        """Перевіряє пошук працівника за частиною імені без врахування великих чи малих літер."""
        self.manager.add_developer("Олександр", "Python")
        self.manager.add_manager("Олексій", "HR")
        self.manager.add_developer("Іван", "Java")

        results = self.manager.search_employee_by_name("олекс")

        self.assertEqual(len(results), 2)
        names = [emp.get_name() for emp in results]
        self.assertIn("Олександр", names)
        self.assertIn("Олексій", names)

    def test_save_and_load_data_integrity(self):
        """Перевіряє коректність збереження та відновлення даних (працівників, техніки та їх зв'язків) через JSON."""
        test_filename = "test_data_integration.json"

        emp_id = self.manager.add_developer("Тест-збереження", "C#")
        lap_id = self.manager.add_laptop("Dell XPS", "Windows")
        self.manager.assign_equipment_to_employee(emp_id, lap_id)

        self.manager.save_data(test_filename)

        new_manager = CompanyManager()
        new_manager.load_data(test_filename)

        restored_emp = new_manager._find_employee_by_id(emp_id)
        self.assertIsNotNone(restored_emp)
        self.assertEqual(restored_emp.get_name(), "Тест-збереження")

        restored_equipment_list = restored_emp.get_equipment()
        self.assertEqual(len(restored_equipment_list), 1)
        self.assertEqual(restored_equipment_list[0].get_id(), lap_id)

        if os.path.exists(test_filename):
            os.remove(test_filename)

if __name__ == "__main__":
    unittest.main()