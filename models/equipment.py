class Equipment:
    """Базовий клас для зберігання загальних даних про обладнання."""

    def __init__(self, eq_id, model_name):
        """Ініціалізація об'єкта з прихованими атрибутами."""
        self.__id = eq_id
        self.__model = model_name
        self.__is_assigned = False

    def get_id(self):
        """Повертає ідентифікатор обладнання."""
        return self.__id

    def get_model(self):
        """Повертає назву моделі обладнання."""
        return self.__model

    def get_status(self):
        """Повертає поточний статус призначення (True/False)."""
        return self.__is_assigned

    def assign(self):
        """Змінює статус обладнання на 'призначено'."""
        self.__is_assigned = True

    def unassign(self):
        """Змінює статус обладнання на 'не призначено'."""
        self.__is_assigned = False

    def to_dict(self):
        """Повертає дані об'єкта у вигляді словника для подальшої обробки або збереження."""
        return {
            "id": self.__id,
            "model": self.__model,
            "is_assigned": self.__is_assigned
        }


class Laptop(Equipment):
    """Клас для зберігання даних про ноутбуки, наслідує Equipment."""

    def __init__(self, eq_id, model_name, os_type):
        """Ініціалізація ноутбука з викликом батьківського конструктора та додаванням типу ОС."""
        super().__init__(eq_id, model_name)
        self.__os_type = os_type

    def get_os_type(self):
        """Повертає тип операційної системи ноутбука."""
        return self.__os_type

    def to_dict(self):
        """Перевизначає метод серіалізації, додаючи специфічні для ноутбука дані."""
        base_dict = super().to_dict()
        base_dict["type"] = "Laptop"
        base_dict["os_type"] = self.__os_type
        return base_dict


class Monitor(Equipment):
    """Клас для зберігання даних про монітори, наслідує Equipment."""

    def __init__(self, eq_id, model_name, resolution):
        """Ініціалізація монітора з викликом батьківського конструктора та додаванням роздільної здатності."""
        super().__init__(eq_id, model_name)
        self.__resolution = resolution

    def get_resolution(self):
        """Повертає роздільну здатність монітора."""
        return self.__resolution

    def to_dict(self):
        """Перевизначає метод серіалізації, додаючи специфічні для монітора дані."""
        base_dict = super().to_dict()
        base_dict["type"] = "Monitor"
        base_dict["resolution"] = self.__resolution
        return base_dict