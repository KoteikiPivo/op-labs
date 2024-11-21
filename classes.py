
class Person:
    """Базовый класс для людей"""
    def __init__(self, name: str, phone: int):
        self.name = name
        self.phone = phone


class Employee(Person):
    """Базовый класс для рабочих"""
    def __init__(self, name: str, phone: int, work_id: int):
        super().__init__(name, phone)
        self.work_id = work_id



class Librarian(Employee):
    """Класс библиотекарей"""
    def __init__(self, name: str, phone: int, work_id: int, work_days: str):
        super().__init__(name, phone, work_id)
        self.work_days = work_days


class Member(Person):
    """Классы членов библиотеки"""
    def __init__(self, name: str, phone: int, member_id: int):
        super().__init__(name, phone)
        self.member_id = member_id

class Account(Member):
    """Классы аккаунтов электронной библиотеки"""
    def __init__(self, name: str, phone: int, member_id: int,
                 login: str, passwd: str):
        super().__init__(name, phone, member_id)
        self.login = login
        self.passwd = passwd


class Customer(Person):
    """Класс клиента доставки"""
    def __init__(self, name: str, phone: int, address: str):
        super().__init__(name, phone)
        self.address = address



class Book:
    """Классы книг библиотеки"""
    def __init__(self, title: str, author: str, year: int):
        self.title = title
        self.author = author
        self.year = year

class EBook(Book):
    """Классы электронных книг библиотеки"""
    def __init__(self, title: str, author: str, year: int, cost: int):
        super().__init__(title, author, year)
        self.cost = cost



class Order:
    """Класс заказов"""
    def __init__(self, book: Book, customer: Customer, ord_id: int):
        self.book = book
        self.customer = customer
        self.ord_id = ord_id

class DeliveryDriver(Employee):
    """Класс доставщиков"""
    def __init__(self, name: str, phone: int, work_id: int, order: Order):
        super().__init__(name, phone, work_id)
        self.work_id = work_id
        self.order = order