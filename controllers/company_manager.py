import csv
from datetime import datetime

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

    def _log_action(self, message, filename="audit.log"):
        """Записує подію у файл аудиту з точною відміткою дати та часу."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(filename, "a", encoding="utf-8") as file:
            file.write(f"[{now}] {message}\n")

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

    def add_developer(self, name, language):
        """Додає нового розробника до бази компанії."""
        new_dev = Developer(name, language)
        self.__employees.append(new_dev)
        print(f"Успіх: Розробника '{name}' додано до системи.")
        self._log_action(f"Створено працівника: {name} (ID: {new_dev.get_id()})")
        return new_dev.get_id()

    def add_manager(self, name, department):
        """Додає нового менеджера до бази компанії."""
        new_manager = Manager(name, department)
        self.__employees.append(new_manager)
        print(f"Успіх: Менеджера '{name}' додано до системи.")
        self._log_action(f"Створено працівника: {name} (ID: {new_manager.get_id()})")
        return new_manager.get_id()

    def add_laptop(self, model, os_type):
        """Додає новий ноутбук на склад компанії."""
        new_laptop = Laptop(model, os_type)
        self.__equipment.append(new_laptop)
        print(f"Успіх: Ноутбук '{model}' додано на склад.")
        self._log_action(f"Додано на склад техніку: {model} (ID: {new_laptop.get_id()})")
        return new_laptop.get_id()

    def add_monitor(self, model, resolution):
        """Додає новий монітор на склад компанії."""
        new_monitor = Monitor(model, resolution)
        self.__equipment.append(new_monitor)
        print(f"Успіх: Монітор '{model}' додано на склад.")
        self._log_action(f"Додано на склад техніку: {model} (ID: {new_monitor.get_id()})")
        return new_monitor.get_id()

    def show_all_employees(self):
        """Виводить список усіх працівників компанії та закріплену за ними техніку."""
        if not self.__employees:
            print("Список працівників порожній.")
            return

        print("--- Список Працівників ---")
        for emp in self.__employees:
            print(f"{emp} | Посада: {emp.__class__.__name__}")
            equipment_list = emp.get_equipment()
            if not equipment_list:
                print("  - Техніка: відсутня")
            else:
                print("  - Техніка:")
                for item in equipment_list:
                    print(f"    - {item}")
        print("-" * 26)

    def show_available_equipment(self):
        """Виводить список усієї техніки, яка зараз знаходиться на складі і доступна для видачі."""
        available_items = [item for item in self.__equipment if not item.get_status()]

        if not available_items:
            print("На складі немає вільної техніки.")
            return

        print("--- Вільна Техніка на Складі ---")
        for item in available_items:
            print(item)
        print("-" * 32)

    def assign_equipment_to_employee(self, emp_id, eq_id):
        """Закріплює вільну техніку за вказаним працівником."""
        employee = self._find_employee_by_id(emp_id)
        equipment = self._find_equipment_by_id(eq_id)

        if employee and equipment:
            if not equipment.get_status():
                # ліміт ноутів
                if equipment.__class__.__name__ == "Laptop":
                    # Шукає чи є вже хоча б один ноутбук у списку техніки працівника
                    has_laptop = any(item.__class__.__name__ == "Laptop" for item in employee.get_equipment())
                    if has_laptop:
                        print(
                            f"Помилка: Працівник '{employee.get_name()}' вже має закріплений ноутбук. Ліміт перевищено.")
                        return  # Перериває метод видача не відбувається

                # ліміт моніторів
                if equipment.__class__.__name__ == "Monitor":
                    monitor_count = sum(1 for item in employee.get_equipment() if item.__class__.__name__ == "Monitor")
                    if monitor_count >= 2:
                        print(
                            f"Помилка: Працівник '{employee.get_name()}' вже має 2 монітори. Максимальний ліміт перевищено.")
                        return

                employee.add_equipment(equipment)
                equipment.assign()
                print(f"Успіх: Техніку '{equipment.get_model()}' видано працівнику '{employee.get_name()}'.")
                self._log_action(f"Видано техніку {equipment.get_model()} працівнику {employee.get_name()}")
            else:
                print("Помилка: Ця техніка вже видана іншому працівнику.")
        else:
            print("Помилка: Невірно вказано ID працівника або техніки.")

    def remove_employee(self, emp_id):
        """Звільняє працівника та відв'язує всю його техніку, повертаючи її у вільний статус."""
        employee = self._find_employee_by_id(emp_id)

        if employee is not None:
            # Зняття статусу призначено з усієї техніки працівника
            for item in employee.get_equipment():
                item.unassign()

            # Видалення працівника з бази
            self.__employees.remove(employee)
            print(f"Успіх: Працівника '{employee.get_name()}' звільнено, техніку повернуто на склад.")
            self._log_action(f"Працівника {employee.get_name()} звільнено")
        else:
            print("Помилка: Працівника з вказаним ID не знайдено.")

    def search_employee_by_name(self, name_query):
        """Шукає працівників за частковим збігом імені (нечутливо до регістру) та повертає список результатів."""
        query = name_query.lower()
        found_employees = [emp for emp in self.__employees if query in emp.get_name().lower()]

        if not found_employees:
            print(f"За запитом '{name_query}' нікого не знайдено.")
        else:
            print(f"--- Результати пошуку ('{name_query}') ---")
            for emp in found_employees:
                print(f"{emp} | Посада: {emp.__class__.__name__}")

        return found_employees

    def show_statistics(self):
        """Виводить загальну аналітику та статистику по працівниках і техніці компанії."""
        print("\n=== АНАЛІТИКА ТА СТАТИСТИКА ===")

        # Аналітика персоналу
        total_employees = len(self.__employees)
        # Використовує генератори списків для швидкого підрахунку
        dev_count = sum(1 for emp in self.__employees if emp.__class__.__name__ == "Developer")
        mgr_count = sum(1 for emp in self.__employees if emp.__class__.__name__ == "Manager")

        print(f"Загальна кількість працівників: {total_employees}")
        print(f"  - Розробників: {dev_count}")
        print(f"  - Менеджерів: {mgr_count}")

        # Аналітика техніки
        total_equipment = len(self.__equipment)
        assigned_count = sum(1 for item in self.__equipment if item.get_status() == True)
        available_count = total_equipment - assigned_count

        print(f"\nЗагальна кількість техніки: {total_equipment}")
        print(f"  - Видано на руки: {assigned_count}")
        print(f"  - Вільно на складі: {available_count}")
        print("===============================\n")

        self._log_action("Перегляд статистики компанії")

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
                    # Запис кожної одиниці техніки
                    for item in equipment_list:
                        item_type = item.__class__.__name__
                        file.write(f"\t- [{item_type}] ID: {item.get_id()} | Модель: {item.get_model()}\n")

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

        # Відновлення техніки з передачею збереженого ID
        for item_data in data.get("equipment", []):
            new_equipment = None
            if item_data["type"] == "Laptop":
                new_equipment = Laptop(item_data["model"], item_data["os_type"], eq_id=item_data["id"])
            elif item_data["type"] == "Monitor":
                new_equipment = Monitor(item_data["model"], item_data["resolution"], eq_id=item_data["id"])

            if new_equipment:
                # Відновлення статусу видачі
                if item_data.get("is_assigned") == True:
                    new_equipment.assign()
                self.__equipment.append(new_equipment)

        # Відновлення працівників з передачею збереженого ID
        for emp_data in data.get("employees", []):
            new_employee = None
            if emp_data["role"] == "Developer":
                new_employee = Developer(emp_data["name"], emp_data["language"], emp_id=emp_data["id"])
            elif emp_data["role"] == "Manager":
                new_employee = Manager(emp_data["name"], emp_data["department"], emp_id=emp_data["id"])

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
        """Повертає техніку від працівника на склад роблячи її знову доступною."""
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
            self._log_action(f"Техніку {equipment.get_model()} повернуто на склад від {employee.get_name()}")
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
        self._log_action(f"Техніку {equipment.get_model()} (ID: {eq_id}) списано з системи")

    def export_to_csv(self, filename="report.csv"):
        """Експортує дані про працівників та їхню техніку у формат CSV для читання в Excel."""
        # Використовується utf-8-sig для коректного відображення кирилиці в Microsoft Excel
        with open(filename, "w", newline="", encoding="utf-8-sig") as file:
            writer = csv.writer(file, delimiter=";")

            # Запис заголовків колонок
            writer.writerow(["ID", "Ім'я", "Посада", "Кількість техніки", "Деталі техніки"])

            # Обробка даних кожного працівника
            for emp in self.__employees:
                role = emp.__class__.__name__
                equipment_list = emp.get_equipment()

                # Формування текстового опису техніки працівника
                if not equipment_list:
                    equipment_details_string = "Немає"
                else:
                    # Збір моделей техніки в один рядок через кому
                    equipment_details_string = ", ".join([item.get_model() for item in equipment_list])

                # Запис сформованого рядка даних у файл
                writer.writerow([emp.get_id(), emp.get_name(), role, len(equipment_list), equipment_details_string])

        print(f"Успіх: Дані експортовано у файл {filename}")
        # Фіксація події експорту в журналі аудиту
        self._log_action(f"Експортовано дані у CSV файл: {filename}")