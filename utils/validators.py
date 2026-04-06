class CancelOperation(Exception):
    """Виняток для миттєвого переривання поточної операції користувачем (введення 0)."""
    pass


def get_non_empty_string(prompt):
    """Отримує та перевіряє непорожній рядок. Перериває роботу при введенні 0."""
    while True:
        user_input = input(prompt).strip()
        if user_input == '0':
            raise CancelOperation()

        if user_input:
            return user_input
        print("Помилка: Введення не може бути порожнім. Спробуйте ще раз або введіть '0' для скасування.")


def get_valid_integer(prompt):
    """Отримує та перевіряє ціле число. Перериває роботу при введенні 0."""
    while True:
        input_str = input(prompt).strip()
        if input_str == '0':
            raise CancelOperation()

        try:
            return int(input_str)
        except ValueError:
            print("Помилка: Будь ласка, введіть коректне ціле число або '0' для скасування.")


def get_valid_choice(prompt, allowed_choices):
    """Отримує введення та перевіряє його наявність у списку дозволених варіантів. Перериває роботу при введенні 0."""
    while True:
        user_input = input(prompt).strip()
        if user_input == '0':
            raise CancelOperation()

        if user_input in allowed_choices:
            return user_input
        print(f"Помилка: Дозволено вводити лише {allowed_choices}. Введіть '0' для скасування.")