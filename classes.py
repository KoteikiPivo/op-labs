# Базовый класс для людей
class Person:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

# Базовый класс для рабочих
class Employee(Person):
    def __init__(self, name, phone, work_id):
        super.__init__(name, phone)
        self.work_id = work_id

class Librarian(Employee):
    def __init__(self, name, phone, work_id, work_days):
        super.__init__(name, phone, work_id)
        self.work_days = work_days

class DeliveryDriver(Employee):
    def __init__(self, name, phone, work_id, order):
        super.__init__(name, phone, work_id)
        self.work_id = work_id
        self.order = None

    def give_order(self, new_order):
        self.order = new_order

#class Member(Person):
    #def __init__(self, name, phone, )