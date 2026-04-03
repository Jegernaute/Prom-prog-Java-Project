class Employee:
    """Базовий клас для зберігання загальних даних про працівника."""

    def __init__(self, emp_id, name):
        """Ініціалізація працівника з прихованими атрибутами та порожнім списком техніки."""
        self.__id = emp_id
        self.__name = name
        self.__equipment_list = []

    def get_id(self):
        """Повертає ідентифікатор працівника."""
        return self.__id

    def get_name(self):
        """Повертає ім'я працівника."""
        return self.__name

    def get_equipment(self):
        """Повертає список виданої техніки (об'єктів)."""
        return self.__equipment_list

    def add_equipment(self, item):
        """Додає об'єкт техніки до списку працівника."""
        self.__equipment_list.append(item)

    def remove_equipment(self, item):
        """Видаляє об'єкт техніки зі списку працівника, якщо він там є."""
        if item in self.__equipment_list:
            self.__equipment_list.remove(item)
        else:
            print("Помилка: Ця техніка не закріплена за цим працівником.")

    def do_work(self):
        """Абстрактний метод для демонстрації поліморфізму."""
        raise NotImplementedError("Цей метод має бути перевизначений у дочірніх класах.")

    def to_dict(self):
        """Серіалізує дані працівника та викликає серіалізацію для кожної одиниці його техніки."""
        equipment_dicts = [item.to_dict() for item in self.__equipment_list]

        return {
            "id": self.__id,
            "name": self.__name,
            "equipment": equipment_dicts
        }

class Developer(Employee):
    """Клас для розробників наслідує Employee."""

    def __init__(self, emp_id, name, programming_language):
        """Ініціалізація розробника з вказівкою мови програмування."""
        super().__init__(emp_id, name)
        self.__programming_language = programming_language

    def get_language(self):
        """Повертає мову програмування розробника."""
        return self.__programming_language

    def do_work(self):
        """Перевизначений метод: розробник пише код."""
        return f"Розробник {self.get_name()} пише код на {self.__programming_language}."

    def to_dict(self):
        """Перевизначає серіалізацію додаючи роль та мову програмування."""
        base_dict = super().to_dict()
        base_dict["role"] = "Developer"
        base_dict["language"] = self.__programming_language
        return base_dict

class Manager(Employee):
    """Клас для менеджерів наслідує Employee."""

    def __init__(self, emp_id, name, department):
        """Ініціалізація менеджера з вказівкою відділу."""
        super().__init__(emp_id, name)
        self.__department = department

    def get_department(self):
        """Повертає назву відділу менеджера."""
        return self.__department

    def do_work(self):
        """Перевизначений метод: менеджер керує відділом."""
        return f"Менеджер {self.get_name()} керує відділом {self.__department}."

    def to_dict(self):
        """Перевизначає серіалізацію додаючи роль та відділ."""
        base_dict = super().to_dict()
        base_dict["role"] = "Manager"
        base_dict["department"] = self.__department
        return base_dict