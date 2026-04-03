from controllers.company_manager import CompanyManager

if __name__ == "__main__":
    # Ініціалізація головного контролера
    manager = CompanyManager()

    # Завантаження збережених даних перед початком роботи
    manager.load_data()

    # Головний цикл програми
    while True:
        print("\n--- Головне Меню ---")
        print("1 - Додати Розробника")
        print("2 - Додати Менеджера")
        print("3 - Додати Ноутбук")
        print("4 - Додати Монітор")
        print("5 - Видати техніку працівнику")
        print("6 - Показати всіх працівників")
        print("7 - Показати вільну техніку")
        print("8 - Звільнити працівника")
        print("0 - Зберегти та Вийти")

        # Отримання команди від користувача
        choice = input("Ваш вибір: ")

        # Обгортка для перехоплення непередбачуваних помилок під час виконання команд
        try:
            # Маршрутизація команд та збір даних від користувача
            if choice == '1':
                emp_id = input("Введіть ID розробника: ")
                name = input("Введіть ім'я розробника: ")
                language = input("Введіть мову програмування: ")
                manager.add_developer(emp_id, name, language)

            elif choice == '2':
                emp_id = input("Введіть ID менеджера: ")
                name = input("Введіть ім'я менеджера: ")
                department = input("Введіть відділ: ")
                manager.add_manager(emp_id, name, department)

            elif choice == '3':
                eq_id = input("Введіть ID ноутбука: ")
                model = input("Введіть модель ноутбука: ")
                os_type = input("Введіть тип ОС: ")
                manager.add_laptop(eq_id, model, os_type)

            elif choice == '4':
                eq_id = input("Введіть ID монітора: ")
                model = input("Введіть модель монітора: ")
                resolution = input("Введіть роздільну здатність: ")
                manager.add_monitor(eq_id, model, resolution)

            elif choice == '5':
                emp_id = input("Введіть ID працівника: ")
                eq_id = input("Введіть ID техніки: ")
                manager.assign_equipment_to_employee(emp_id, eq_id)

            elif choice == '6':
                manager.show_all_employees()

            elif choice == '7':
                manager.show_available_equipment()

            elif choice == '8':
                emp_id = input("Введіть ID працівника для звільнення: ")
                manager.remove_employee(emp_id)

            elif choice == '0':
                # Збереження стану та безпечний вихід з програми
                manager.save_data()
                print("Дані збережено. До побачення!")
                break

            else:
                print("Невідома команда. Спробуйте ще раз.")

        except Exception as e:
            # Вивід повідомлення про помилку без екстреного завершення програми
            print(f"Виникла помилка: {e}")