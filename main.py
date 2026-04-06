import os
from controllers.company_manager import CompanyManager
from utils.validators import get_non_empty_string, get_valid_choice, CancelOperation


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
        print("(Підказка: введіть '0' під час будь-якого запиту для скасування операції)")
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
        print("13 - Показати статистику (Дашборд)")
        print("14 - Експортувати дані в CSV (Excel)")
        print("0 - Зберегти та Вийти")

        # Використання валідатора для вибору пункту меню
        choice = input("Ваш вибір: ").strip()

        # Обгортка для перехоплення непередбачуваних помилок
        try:
            if choice == '1':
                name = get_non_empty_string("Введіть ім'я розробника: ")
                language = get_non_empty_string("Введіть мову програмування: ")
                manager.add_developer(name, language)
                pause_screen()

            elif choice == '2':
                name = get_non_empty_string("Введіть ім'я менеджера: ")
                allowed_departments = ["IT", "HR", "Sales", "Marketing", "Finance"]
                department = get_valid_choice(f"Оберіть відділ {allowed_departments}: ", allowed_departments)
                manager.add_manager(name, department)
                pause_screen()

            elif choice == '3':
                model = get_non_empty_string("Введіть модель ноутбука: ")
                os_type = get_valid_choice("Введіть тип ОС (Windows/Mac/Linux): ", ["Windows", "Mac", "Linux"])
                manager.add_laptop(model, os_type)
                pause_screen()

            elif choice == '4':
                model = get_non_empty_string("Введіть модель монітора: ")
                resolution = get_non_empty_string("Введіть роздільну здатність: ")
                manager.add_monitor(model, resolution)
                pause_screen()

            elif choice == '5':
                manager.show_all_employees()
                manager.show_available_equipment()

                # Заміна на get_non_empty_string бо ID тепер є текстом
                emp_id = get_non_empty_string("Введіть ID працівника: ")
                eq_id = get_non_empty_string("Введіть ID техніки: ")
                manager.assign_equipment_to_employee(emp_id, eq_id)
                pause_screen()

            elif choice == '6':
                manager.show_all_employees()
                pause_screen()

            elif choice == '7':
                manager.show_available_equipment()
                pause_screen()

            elif choice == '8':
                # Вивід контексту перед запитом ID
                manager.show_all_employees()
                emp_id = get_non_empty_string("Введіть ID працівника для звільнення: ")
                manager.remove_employee(emp_id)
                pause_screen()

            elif choice == '9':
                # Вивід контексту перед запитом ID
                manager.show_all_employees()
                emp_id = get_non_empty_string("Введіть ID працівника, який повертає техніку: ")
                eq_id = get_non_empty_string("Введіть ID техніки для повернення: ")
                manager.return_equipment(emp_id, eq_id)
                pause_screen()

            elif choice == '10':
                # Вивід вільної техніки зі складу перед списанням
                manager.show_available_equipment()
                eq_id = get_non_empty_string("Введіть ID техніки для повного списання: ")
                manager.remove_equipment_from_system(eq_id)
                pause_screen()

            elif choice == '11':
                name_query = get_non_empty_string("Введіть ім'я або частину імені для пошуку: ")
                manager.search_employee_by_name(name_query)
                pause_screen()

            elif choice == '12':
                manager.generate_text_report()
                pause_screen()

            elif choice == '13':
                manager.show_statistics()
                pause_screen()

            elif choice == '14':
                manager.export_to_csv()
                pause_screen()

            elif choice == '0':
                manager.save_data()
                print("Дані збережено. До побачення!")
                break

            else:
                print("Невідома команда. Спробуйте ще раз.")
                pause_screen()

        except CancelOperation:
            # Перехоплення скасування та м'яке повернення до меню
            print("\n[!] Операцію скасовано користувачем. Повернення до головного меню.")
            pause_screen()

        except Exception as e:
            # Обробка критичних помилок без завершення програми
            print(f"Виникла помилка під час виконання: {e}")
            pause_screen()