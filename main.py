import os
from controllers.company_manager import CompanyManager
from utils.validators import get_non_empty_string, get_valid_integer, get_valid_choice

def clear_screen():
    """Очищує консоль."""
    os.system('cls' if os.name == 'nt' else 'clear')

def pause_screen():
    """Призупиняє виконання програми очікуючи на дію користувача."""
    input("\nНатисніть Enter для продовження...")


if __name__ == "__main__":
    # Ініціалізація головного контролера
    manager = CompanyManager()

    # Завантаження збережених даних перед початком роботи
    manager.load_data()

    # Головний цикл програми
    while True:
        # Очищення екрану перед кожним відображенням меню
        clear_screen()

        print("\n--- Головне Меню ---")
        print("1 - Додати Розробника")
        print("2 - Додати Менеджера")
        print("3 - Додати Ноутбук")
        print("4 - Додати Монітор")
        print("5 - Видати техніку працівнику")
        print("6 - Показати всіх працівників")
        print("7 - Показати вільну техніку")
        print("8 - Звільнити працівника")
        print("9 - Повернути техніку на склад")
        print("10 - Списати техніку з бази")
        print("11 - Знайти працівника за ім'ям")
        print("12 - Згенерувати текстовий звіт")
        print("0 - Зберегти та Вийти")

        # Використання валідатора для вибору пункту меню
        choice = get_non_empty_string("Ваш вибір: ")

        # Обгортка для перехоплення непередбачуваних помилок
        try:
            if choice == '1':
                emp_id = get_valid_integer("Введіть числовий ID розробника: ")
                name = get_non_empty_string("Введіть ім'я розробника: ")
                language = get_non_empty_string("Введіть мову програмування: ")
                manager.add_developer(emp_id, name, language)
                pause_screen()

            elif choice == '2':
                emp_id = get_valid_integer("Введіть числовий ID менеджера: ")
                name = get_non_empty_string("Введіть ім'я менеджера: ")
                department = get_non_empty_string("Введіть відділ: ")
                manager.add_manager(emp_id, name, department)
                pause_screen()

            elif choice == '3':
                eq_id = get_valid_integer("Введіть числовий ID ноутбука: ")
                model = get_non_empty_string("Введіть модель ноутбука: ")
                os_type = get_valid_choice("Введіть тип ОС (Windows/Mac/Linux): ", ["Windows", "Mac", "Linux"])
                manager.add_laptop(eq_id, model, os_type)
                pause_screen()

            elif choice == '4':
                eq_id = get_valid_integer("Введіть числовий ID монітора: ")
                model = get_non_empty_string("Введіть модель монітора: ")
                resolution = get_non_empty_string("Введіть роздільну здатність: ")
                manager.add_monitor(eq_id, model, resolution)
                pause_screen()


            elif choice == '5':
                manager.show_all_employees()
                manager.show_available_equipment()
                emp_id = get_valid_integer("Введіть ID працівника: ")
                eq_id = get_valid_integer("Введіть ID техніки: ")
                manager.assign_equipment_to_employee(emp_id, eq_id)
                pause_screen()

            elif choice == '6':
                manager.show_all_employees()
                pause_screen()

            elif choice == '7':
                manager.show_available_equipment()
                pause_screen()

            elif choice == '8':
                emp_id = get_valid_integer("Введіть ID працівника для звільнення: ")
                manager.remove_employee(emp_id)
                pause_screen()

            elif choice == '9':
                emp_id = get_valid_integer("Введіть ID працівника, який повертає техніку: ")
                eq_id = get_valid_integer("Введіть ID техніки для повернення: ")
                manager.return_equipment(emp_id, eq_id)
                pause_screen()

            elif choice == '10':
                eq_id = get_valid_integer("Введіть ID техніки для повного списання: ")
                manager.remove_equipment_from_system(eq_id)
                pause_screen()

            elif choice == '11':
                name_query = get_non_empty_string("Введіть ім'я або частину імені для пошуку: ")
                manager.search_employee_by_name(name_query)
                pause_screen()

            elif choice == '12':
                manager.generate_text_report()
                pause_screen()

            elif choice == '0':
                # Збереження стану та безпечний вихід без паузи
                manager.save_data()
                print("Дані збережено. До побачення!")
                break

            else:
                print("Невідома команда. Спробуйте ще раз.")
                pause_screen()

        except Exception as e:
            # Обробка критичних помилок без завершення програми
            print(f"Виникла помилка під час виконання: {e}")
            pause_screen()