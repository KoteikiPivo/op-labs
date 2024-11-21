# Имплементации CRUD для классов из "classes.py"
from classes import *


class LibrarianCRUD:
    def __init__(self):
        self.librarian_list: Librarian = []
        self.current_id = 1

    def create(self, name: str, phone: int, work_days: str) -> Librarian:
        lib = Librarian(name, phone, self.current_id, work_days)
        self.librarian_list.append(lib)
        self.current_id += 1
        return lib
    
    def read_all(self):
        return self.librarian_list
    
    def read_by_id(self, lib_id: int):
        for lib in self.librarian_list:
            if lib.work_id == lib_id:
                return lib
        return None
    
    def update(self, lib_id: int, name: str = None, phone: int = None, work_days: str = None):
        lib = self.read_by_id(lib_id)
        if lib:
            if name is not None:
                lib.name = name
            if phone is not None:
                lib.phone = phone
            if work_days is not None:
                lib.work_days = work_days
            return lib
        return None
    
    def delete(self, lib_id: int):
        lib = self.read_by_id(lib_id)
        if lib:
            self.librarian_list.remove(lib)
            return f"Librarian with id {lib_id} removed"
        return "Librarian not found"

class MemberCRUD:
    def __init__(self):
        self.member_list: Member = []
        self.current_id = 1

    def create(self, name: str, phone: int) -> Member:
        memb = Member(name, phone, self.current_id)
        self.member_list.append(memb)
        self.current_id += 1
        return memb
    
    def read_all(self):
        return self.member_list
    
    def read_by_id(self, memb_id: int):
        for memb in self.member_list:
            if memb.member_id == memb_id:
                return memb
        return None
    
    def update(self, memb_id: int, name: str, phone: int):
        memb = self.read_by_id(memb_id)
        if memb:
            if name is not None:
                memb.name = name
            if phone is not None:
                memb.phone = phone
            return memb
        return None
    
    def delete(self, memb_id: int):
        memb = self.read_by_id(memb_id)
        if memb:
            self.member_list.remove(memb)
            return f"Member with id {memb_id} removed"
        return "Member not found"

class AccountCRUD:
    def __init__(self):
        self.account_list: Account = []
        self.current_id = 1

    def create(self, name: str, phone: int, login: str, passwd: str) -> Account:
        acc = Account(name, phone, self.current_id, login, passwd)
        self.account_list.append(acc)
        self.current_id += 1
        return acc
    
    def read_all(self):
        return self.account_list
    
    def read_by_id(self, acc_id: int):
        for acc in self.account_list:
            if acc.member_id == acc_id:
                return acc
        return None
    
    def update(self, acc_id: int, name: str, phone: int, login: str, passwd: str):
        acc = self.read_by_id(acc_id)
        if acc:
            if name is not None:
                acc.name = name
            if phone is not None:
                acc.phone = phone
            if login is not None:
                acc.login = login
            if passwd is not None:
                acc.passwd = passwd
            return acc
        return None
    
    def delete(self, acc_id: int):
        acc = self.read_by_id(acc_id)
        if acc:
            self.account_list.remove(acc)
            return f"Account with id {acc_id} removed"
        return "Account not found"

class CustomerCRUD:
    def __init__(self):
        self.customer_list: Customer = []

    def create(self, name: str, phone: int, address: str) -> Customer:
        cust = Customer(name, phone, address)
        self.customer_list.append(cust)
        return cust
    
    def read_all(self):
        return self.customer_list
    
    def read_by_address(self, address_search: str):
        for cust in self.customer_list:
            if cust.address == address_search:
                return cust
        return None
    
    def update(self, address_search: str, name: str, phone: int, address: str):
        cust = self.read_by_address(address_search)
        if cust:
            if name is not None:
                cust.name = name
            if phone is not None:
                cust.phone = phone
            if address is not None:
                cust.address = address
            return cust
        return None
    
    def delete(self, address_search: str):
        cust = self.read_by_address(address_search)
        if cust:
            self.customer_list.remove(cust)
            return f"Customer with address {address_search} removed"
        return "Customer not found"

class BookCRUD:
    def __init__(self):
        self.book_list: Book = []

    def create(self, title: str, author: str, year: int) -> Book:
        book = Book(title, author, year)
        self.book_list.append(book)
        return book
    
    def read_all(self):
        return self.book_list
    
    def read_by_title(self, title_search: str):
        for book in self.book_list:
            if book.title == title_search:
                return book
        return None
    
    def update(self, title_search: str, title: str, author: str, year: int):
        book = self.read_by_title(title_search)
        if book:
            if title is not None:
                book.title = title
            if phone is not None:
                book.author = author
            if year is not None:
                book.year = year
            return book
        return None
    
    def delete(self, title_search: str):
        book = self.read_by_title(title_search)
        if book:
            self.book_list.remove(book)
            return f"Book with title {title_search} removed"
        return "Book not found"

class EBookCRUD:
    def __init__(self):
        self.ebook_list: EBook = []

    def create(self, title: str, author: str, year: int, cost: int) -> EBook:
        ebook = EBook(title, author, year, cost)
        self.ebook_list.append(ebook)
        return ebook
    
    def read_all(self):
        return self.ebook_list
    
    def read_by_title(self, title_search: str):
        for ebook in self.ebook_list:
            if ebook.title == title_search:
                return ebook
        return None
    
    def update(self, title_search: str, title: str, author: str, year: int, cost: int):
        ebook = self.read_by_title(title_search)
        if ebook:
            if title is not None:
                ebook.title = title
            if phone is not None:
                ebook.author = author
            if year is not None:
                ebook.year = year
            if cost is not None:
                ebook.cost = cost
            return ebook
        return None
    
    def delete(self, title_search: str):
        ebook = self.read_by_title(title_search)
        if ebook:
            self.ebook_list.remove(book)
            return f"EBook with title {title_search} removed"
        return "EBook not found"

class OrderCRUD:
    def __init__(self):
        self.order_list: Order = []
        self.current_id = 1

    def create(self, book: Book, customer: Customer) -> Order:
        ordr = Order(book, customer, self.current_id)
        self.order_list.append(ordr)
        return ordr
    
    def read_all(self):
        return self.order_list
    
    def read_by_id(self, id: int):
        for ordr in self.order_list:
            if ordr.id == id:
                return ordr
        return None
    
    def update(self, id: int, book: Book, customer: Customer):
        ordr = self.read_by_id(id)
        if ordr:
            if book is not None:
                ordr.book = book
            if customer is not None:
                ordr.customer = customer
            return ordr
        return None
    
    def delete(self, id: int):
        ordr = self.read_by_id(id)
        if ordr:
            self.order_list.remove(ordr)
            return f"Order with ID {id} removed"
        return "Order not found"

class DeliveryDriverCRUD:
    def __init__(self):
        self.driver_list: DeliveryDriver = []
        self.current_id = 1

    def create(self, name: str, phone: int, order: Order) -> DeliveryDriver:
        drive = DeliveryDriver(name, phone, self.current_id, order)
        self.driver_list.append(drive)
        self.current_id += 1
        return drive
    
    def read_all(self):
        return self.driver_list
    
    def read_by_id(self, drive_id: int):
        for drive in self.driver_list:
            if drive.work_id == drive_id:
                return drive
        return None
    
    def update(self, drive_id: int, name: str = None, phone: int = None, order: Order = None):
        drive = self.read_by_id(drive_id)
        if drive:
            if name is not None:
                drive.name = name
            if phone is not None:
                drive.phone = phone
            if order is not None:
                drive.order = order
            return drive
        return None
    
    def delete(self, drive_id: int):
        drive = self.read_by_id(drive_id)
        if drive:
            self.driver_list.remove(drive)
            return f"Driver with id {drive_id} removed"
        return "Driver not found"