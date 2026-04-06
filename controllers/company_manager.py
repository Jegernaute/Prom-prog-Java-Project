from models.employee import Developer, Manager
from models.equipment import Laptop, Monitor
import json
import os

class CompanyManager:
    """Головний контролер для управління персоналом та технікою компанії."""

    def __init__(self):
        """Ініціалізація порожніх списків для зберігання працівників та обладнання."""
        self.__employees = []
        self.__equipment = []

    def _find_employee_by_id(self, emp_id):
        """Шукає працівника у списку за ідентифікатором."""
        for emp in self.__employees:
            if emp.get_id() == emp_id:
                return emp
        return None

    def _find_equipment_by_id(self, eq_id):
        """Шукає техніку у списку за ідентифікатором."""
        for item in self.__equipment:
            if item.get_id() == eq_id:
                return item
        return None

    def add_developer(self, emp_id, name, language):
        """Створює та додає розробника після перевірки унікальності ID."""
        if self._find_employee_by_id(emp_id) is not None:
            print("Помилка: ID вже існує")
            return

        new_dev = Developer(emp_id, name, language)
        self.__employees.append(new_dev)
        print(f"Розробника '{name}' успішно додано.")

    def add_manager(self, emp_id, name, department):
        """Створює та додає менеджера після перевірки унікальності ID."""
        if self._find_employee_by_id(emp_id) is not None:
            print("Помилка: ID вже існує")
            return

        new_manager = Manager(emp_id, name, department)
        self.__employees.append(new_manager)
        print(f"Менеджера '{name}' успішно додано.")

    def add_laptop(self, eq_id, model, os_type):
        """Створює та додає ноутбук після перевірки унікальності ID."""
        if self._find_equipment_by_id(eq_id) is not None:
            print("Помилка: ID вже існує")
            return

        new_laptop = Laptop(eq_id, model, os_type)
        self.__equipment.append(new_laptop)
        print(f"Ноутбук '{model}' успішно додано.")

    def add_monitor(self, eq_id, model, resolution):
        """Створює та додає монітор після перевірки унікальності ID."""
        if self._find_equipment_by_id(eq_id) is not None:
            print("Помилка: ID вже існує")
            return

        new_monitor = Monitor(eq_id, model, resolution)
        self.__equipment.append(new_monitor)
        print(f"Монітор '{model}' успішно додано.")

    def show_all_employees(self):
        """Виводить детальну інформацію про всіх працівників у компанії."""
        print("--- Список працівників ---")
        for emp in self.__employees:
            role = emp.__class__.__name__
            print(f"ID: {emp.get_id()} | Ім'я: {emp.get_name()} | Посада: {role}")
            print(f"Діяльність: {emp.do_work()}")
            print("-" * 25)

    def show_available_equipment(self):
        """Виводить перелік техніки яка наразі не видана жодному працівнику."""
        print("--- Доступна техніка ---")
        for item in self.__equipment:
            if item.get_status() == False:
                type_name = item.__class__.__name__
                print(f"[{type_name}] ID: {item.get_id()} | Модель: {item.get_model()}")
        print("-" * 25)

    def assign_equipment_to_employee(self, emp_id, eq_id):
        """Перевіряє доступність та ліміти після чого видає техніку працівнику."""
        employee = self._find_employee_by_id(emp_id)
        equipment = self._find_equipment_by_id(eq_id)

        if employee is None or equipment is None:
            print("Помилка: Працівника або техніку з вказаним ID не знайдено.")
            return

        if equipment.get_status() == True:
            print("Помилка: Ця техніка вже видана іншому працівнику.")
            return

        current_equipment = employee.get_equipment()

        # Підрахунок кількості техніки за типами
        laptop_count = sum(1 for item in current_equipment if isinstance(item, Laptop))
        monitor_count = sum(1 for item in current_equipment if isinstance(item, Monitor))

        # Перевірка лімітів
        if isinstance(equipment, Laptop) and laptop_count >= 1:
            print("Помилка: Ліміт ноутбуків вичерпано (максимум 1).")
            return

        if isinstance(equipment, Monitor) and monitor_count >= 2:
            print("Помилка: Ліміт моніторів вичерпано (максимум 2).")
            return

        # Успішна видача
        employee.add_equipment(equipment)
        equipment.assign()
        print(f"Успіх: Обладнання '{equipment.get_model()}' видано працівнику '{employee.get_name()}'.")

    def remove_employee(self, emp_id):
        """Звільняє працівника та відв'язує всю його техніку, повертаючи її у вільний статус."""
        employee = self._find_employee_by_id(emp_id)

        if employee is not None:
            # Зняття статусу "призначено" з усієї техніки працівника
            for item in employee.get_equipment():
                item.unassign()

            # Видалення працівника з бази
            self.__employees.remove(employee)
            print(f"Успіх: Працівника '{employee.get_name()}' звільнено, техніку повернуто на склад.")
        else:
            print("Помилка: Працівника з вказаним ID не знайдено.")

    def search_employee_by_name(self, name_query):
        """Шукає та виводить інформацію про працівників за частиною імені (без урахування регістру)."""
        found_count = 0
        # Приведення запиту до нижнього регістру для коректного порівняння
        search_lower = name_query.lower()

        print(f"--- Результати пошуку для '{name_query}' ---")
        for emp in self.__employees:
            # Перевірка входження підрядка в ім'я (також у нижньому регістрі)
            if search_lower in emp.get_name().lower():
                role = emp.__class__.__name__
                print(f"ID: {emp.get_id()} | Ім'я: {emp.get_name()} | Посада: {role}")
                found_count += 1

        if found_count == 0:
            print("Помилка: Працівників з таким ім'ям не знайдено.")
        print("-" * 25)

    def generate_text_report(self, filename="report.txt"):
        """Генерує читабельний текстовий звіт про всіх працівників та їхню техніку."""
        with open(filename, "w", encoding="utf-8") as file:
            file.write("=== ЗВІТ ПО КОМПАНІЇ ===\n\n")

            # Прохід по всім працівникам для запису їхніх даних
            for emp in self.__employees:
                role = emp.__class__.__name__
                file.write(f"ID: {emp.get_id()} | Ім'я: {emp.get_name()} | Посада: {role}\n")

                equipment_list = emp.get_equipment()
                # Перевірка наявності техніки
                if not equipment_list:
                    file.write("\t- Техніка відсутня\n")
                else:
                    # Запис кожної одиниці техніки з відступом
                    for item in equipment_list:
                        item_type = item.__class__.__name__
                        file.write(f"\t- [{item_type}] ID: {item.get_id()} | Модель: {item.get_model()}\n")

                # Порожній рядок між записами працівників для візуального розділення
                file.write("\n")

        print(f"Успіх: Текстовий звіт згенеровано у файл {filename}")

    def save_data(self, filename="data.json"):
        """Зберігає всі дані про працівників та обладнання у форматі JSON."""
        export_data = {
            "employees": [],
            "equipment": []
        }

        # Серіалізація техніки
        for item in self.__equipment:
            export_data["equipment"].append(item.to_dict())

        # Серіалізація працівників
        for emp in self.__employees:
            export_data["employees"].append(emp.to_dict())

        # Запис у файл із збереженням форматування та підтримкою кирилиці
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(export_data, file, indent=4, ensure_ascii=False)

        print(f"Дані успішно збережено у файл: {filename}")

    def load_data(self, filename="data.json"):
        """Завантажує дані з JSON-файлу та відновлює об'єкти і їхні зв'язки."""
        if not os.path.exists(filename):
            return

        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        # Очищення поточного стану перед завантаженням
        self.__employees = []
        self.__equipment = []

        # Відновлення техніки
        for item_data in data.get("equipment", []):
            new_equipment = None
            if item_data["type"] == "Laptop":
                new_equipment = Laptop(item_data["id"], item_data["model"], item_data["os_type"])
            elif item_data["type"] == "Monitor":
                new_equipment = Monitor(item_data["id"], item_data["model"], item_data["resolution"])

            if new_equipment:
                # Відновлення статусу видачі
                if item_data.get("is_assigned") == True:
                    new_equipment.assign()
                self.__equipment.append(new_equipment)

        # Відновлення працівників
        for emp_data in data.get("employees", []):
            new_employee = None
            if emp_data["role"] == "Developer":
                new_employee = Developer(emp_data["id"], emp_data["name"], emp_data["language"])
            elif emp_data["role"] == "Manager":
                new_employee = Manager(emp_data["id"], emp_data["name"], emp_data["department"])

            if new_employee:
                # Відновлення зв'язків з технікою
                saved_equipment = emp_data.get("equipment", [])
                for eq_dict in saved_equipment:
                    eq_id = eq_dict.get("id")
                    found_equipment = self._find_equipment_by_id(eq_id)
                    if found_equipment:
                        new_employee.add_equipment(found_equipment)

                self.__employees.append(new_employee)

        print(f"Дані успішно завантажено з файлу: {filename}")

    def return_equipment(self, emp_id, eq_id):
        """Повертає техніку від працівника на склад, роблячи її знову доступною."""
        employee = self._find_employee_by_id(emp_id)
        equipment = self._find_equipment_by_id(eq_id)

        if employee is None or equipment is None:
            print("Помилка: Працівника або техніку з вказаним ID не знайдено.")
            return

        # Перевірка чи техніка дійсно належить цьому працівнику
        if equipment in employee.get_equipment():
            # Видалення зі списку працівника та оновлення статусу об'єкта
            employee.remove_equipment(equipment)
            equipment.unassign()
            print(f"Успіх: Техніку '{equipment.get_model()}' повернуто на склад від '{employee.get_name()}'.")
        else:
            print(f"Помилка: Техніка ID {eq_id} не закріплена за працівником {employee.get_name()}.")

    def remove_equipment_from_system(self, eq_id):
        """Повністю видаляє техніку з бази даних компанії (списання)."""
        equipment = self._find_equipment_by_id(eq_id)

        if equipment is None:
            print("Помилка: Техніку з вказаним ID не знайдено.")
            return

        # Заборона видалення якщо техніка все ще у працівника
        if equipment.get_status() == True:
            print("Помилка: Неможливо списати техніку, яка закріплена за працівником. Спочатку поверніть її на склад.")
            return

        # Видалення об'єкта зі списку обладнання компанії
        self.__equipment.remove(equipment)
        print(f"Успіх: Техніку '{equipment.get_model()}' успішно списано та видалено з системи.")