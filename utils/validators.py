def get_non_empty_string(prompt_text):
    """Отримує від користувача текстовий рядок гарантуючи що він не є порожнім."""
    while True:
        # Отримання вводу з видаленням зайвих пробілів по краях
        user_input = input(prompt_text).strip()

        if user_input:
            return user_input

        print("Помилка: Це поле не може бути порожнім. Спробуйте ще раз.")

def get_valid_integer(prompt_text):
    """Отримує від користувача ціле число, обробляючи помилки неправильного формату."""
    while True:
        try:
            return int(input(prompt_text).strip())
        except ValueError:
            print("Помилка: Будь ласка, введіть ціле число.")


def get_valid_choice(prompt_text, valid_options):
    """Отримує від користувача значення, яке має збігатися з одним із дозволених варіантів."""
    while True:
        user_input = input(prompt_text).strip()
        if user_input in valid_options:
            return user_input
        print(f"Помилка: Оберіть один з варіантів {valid_options}")