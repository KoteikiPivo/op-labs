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


class Doctor(Employee):
    """Класс докторов"""
    def __init__(self, name: str, phone: int, work_id: int, work_days: str):
        super().__init__(name, phone, work_id)
        self.work_days = work_days
    
    def to_json(self):
        return {
            'name': self.name,
            'phone': self.phone,
            'work_id': self.work_id,
            'work_days': self.work_days
        }


class Patient(Person):
    """Классы пациентов"""
    def __init__(self, name: str, phone: int, patient_id: int):
        super().__init__(name, phone)
        self.patient_id = patient_id
        
    def to_json(self):
        return {
            'name': self.name,
            'phone': self.phone,
            'patient_id': self.patient_id
        }


class Account(Patient):
    """Классы аккаунтов сайта больницы"""
    def __init__(self, name: str, phone: int, patient_id: int,
                 login: str, passwd: str):
        super().__init__(name, phone, patient_id)
        self.login = login
        self.passwd = passwd

    def to_json(self):
        return {
            'name': self.name,
            'phone': self.phone,
            'patient_id': self.patient_id,
            'login': self.login,
            'passwd': self.passwd
        }

class Ambulance(Person):
    """Класс пациента, вызывающего скорую"""
    def __init__(self, name: str, phone: int, address: str):
        super().__init__(name, phone)
        self.address = address
    
    def to_json(self):
        return {
            'name': self.name,
            'phone': self.phone,
            'address': self.address
        }


class Symptom:
    """Классы симптомов"""
    def __init__(self, symname: str, severity: int):
        self.symname = symname
        self.severity = severity

    def to_json(self):
        return {
            'symname': self.symname,
            'severity': self.severity
        }

class Treatment(Symptom):
    """Классы лечения симптомов"""
    def __init__(self, symname: str, severity: int, treatname: str, cost: int):
        super().__init__(symname, severity)
        self.cost = cost
        self.treatname = treatname
    
    def to_json(self):
        return {
            'symname': self.symname,
            'severity': self.severity,
            'treatname': self.treatname,
            'cost': self.cost
        }


class Order:
    """Класс вызывов скорой"""
    def __init__(self, symptom: Symptom, ambulance: Ambulance, ord_id: int):
        self.symptom = symptom
        self.ambulance = ambulance
        self.ord_id = ord_id

    def to_json(self):
        return {
            'symptom': self.symptom.to_json(),
            'ambulance': self.ambulance.to_json(),
            'ord_id': self.ord_id
        }

class AmbulanceDriver(Employee):
    """Класс водителей скорой"""
    def __init__(self, name: str, phone: int, work_id: int, order: Order):
        super().__init__(name, phone, work_id)
        self.work_id = work_id
        self.order = order

    def to_json(self):
        return {
            'name': self.name,
            'phone': self.phone,
            'work_id': self.work_id,
            'order': self.order.to_json()
        }