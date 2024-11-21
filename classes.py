"""Базовый класс для людей"""
class Person:
    def __init__(self, name: str, phone: int):
        self.name = name
        self.phone = phone

"""Базовый класс для рабочих"""
class Employee(Person):
    def __init__(self, name: str, phone: int, work_id: int):
        super().__init__(name, phone)
        self.work_id = work_id


"""Классы рабочих"""
class Librarian(Employee):
    def __init__(self, name: str, phone: int, work_id: int, work_days: str):
        super(Employee, self).__init__(name, phone, work_id)
        self.work_days = work_days

class DeliveryDriver(Employee):
    def __init__(self, name: str, phone: int, work_id: int, order: Order):
        super(Employee, self).__init__(name, phone, work_id)
        self.work_id = work_id
        self.order = order


"""Классы членов библиотеки"""
class Member(Person):
    def __init__(self, name: str, phone: int, member_id: int):
        super().__init__(name, phone)
        self.member_id = member_id

class Account(Member):
    def __init__(self, name: str, phone: int, member_id: int, login: str, passwd: str):
        super(Member, self).__init__(name, phone, member_id)
        self.login = login
        self.passwd = passwd

"""Класс клиента доставки"""
class Customer(Person):
    def __init__(self, name: str, phone: int, address: str):
        super().__init__(name, phone)
        self.address = address


"""Классы книг библиотеки"""
class Book:
    def __init__(self, title: str, author: str, year: int):
        self.title = title
        self.author = author
        self.year = year

class EBook(Book):
    def __init__(self, title: str, author: str, year: int, cost: int):
        super().__init__(title, author, year)
        self.cost = cost


"""Класс заказов"""
class Order:
    def __init__(self, book: Book, customer: Customer, id: int):
        self.book = book
        self.customer = customer
        self.id = id

