# Вариант 11 - Предметная область поликлиники/больницы
import json
from xml.etree import ElementTree as ElTree


class Person:
    """Базовый класс для людей"""

    def __init__(self, name: str, phone: int):
        if not isinstance(name, str):
            raise TypeError('Incorrect type for name')
        if not isinstance(phone, int) or phone < 0:
            raise TypeError('Invalid value for phone')
        self.name = name
        self.phone = phone


class Employee(Person):
    """Базовый класс для рабочих"""

    def __init__(self, name: str, phone: int, work_id: int):
        super().__init__(name, phone)
        if not isinstance(work_id, int) or work_id < 0:
            raise ValueError('Invalid value for work_id')
        self.work_id = work_id


class Doctor(Employee):
    """Класс докторов"""

    def __init__(self, name: str, phone: int, work_id: int, work_days: str):
        super().__init__(name, phone, work_id)
        if not isinstance(work_days, str):
            raise TypeError('Incorrect type for work_days')
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
        if not isinstance(patient_id, int) or patient_id < 0:
            raise ValueError('Invalid value for patient_id')
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
        if not isinstance(login, str):
            raise TypeError('Incorrect type for login')
        if not isinstance(passwd, str):
            raise TypeError('Incorrect type for passwd')
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
        if not isinstance(address, str):
            raise TypeError('Incorrect type for address')
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
        if not isinstance(symname, str):
            raise TypeError('Incorrect type for symname')
        if not isinstance(severity, int) or severity < 0:
            raise ValueError('Invalid value for severity')
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
        if not isinstance(treatname, str):
            raise TypeError('Incorrect type for treatname')
        if not isinstance(cost, int) or cost < 0:
            raise ValueError('Invalid value for cost')
        self.treatname = treatname
        self.cost = cost

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
        if not isinstance(symptom, Symptom):
            raise TypeError('Incorrect type for symptom')
        if not isinstance(ambulance, Ambulance):
            raise TypeError('Incorrect type for ambulance')
        if not isinstance(ord_id, int) or ord_id < 0:
            raise ValueError('Invalid value for ord_id')
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
        if not isinstance(order, Order):
            raise TypeError('Incorrect type for order')
        self.work_id = work_id
        self.order = order

    def to_json(self):
        return {
            'name': self.name,
            'phone': self.phone,
            'work_id': self.work_id,
            'order': self.order.to_json()
        }

# Классы ошибок


class CustomError(Exception):
    pass


class FileError(CustomError):
    def __init__(self, filename):
        self.filename = filename


class UpdateError(CustomError):
    def __init__(self, var):
        self.var = var


# -------------------Имплементации CRUD-------------------

class DoctorCRUD:
    """CRUD для докторов"""

    def __init__(self):
        self.doctor_list: Doctor = []
        self.current_id = 1

    def create(self, name: str, phone: int, work_days: str) -> Doctor:
        doc = Doctor(name, phone, self.current_id, work_days)
        self.doctor_list.append(doc)
        self.current_id += 1
        return doc

    def read_all(self):
        return self.doctor_list

    def read_by_id(self, doc_id: int):
        for doc in self.doctor_list:
            if doc.work_id == doc_id:
                return doc
        return None

    def update(self, doc_id: int, name: str = None,
               phone: int = None, work_days: str = None):
        if self.current_id >= doc_id:
            self.doctor_list[doc_id - 1] = Doctor(name, phone,
                                                  doc_id, work_days)
        else:
            raise (UpdateError('doc'))

    def delete(self, doc_id: int):
        doc = self.read_by_id(doc_id)
        if doc:
            self.doctor_list.remove(doc)
            return f"Doctor with id {doc_id} removed"
        return "Doctor not found"

    def class_to_json(self):
        return {
            'doctor_list': [doc.to_json() for doc in self.doctor_list]
        }

    def from_json(self, data):
        for doc in data['doctor_list']:
            self.create(doc['name'], doc['phone'], doc['work_days'])

    def class_to_xml(self, root: ElTree.Element):
        doctors = ElTree.SubElement(root, 'Doctors')
        for doc in self.doctor_list:
            d = ElTree.SubElement(doctors, 'Doctor')
            d.set('name', doc.name)
            d.set('phone', str(doc.phone))
            d.set('work_id', str(doc.work_id))
            d.set('work_days', doc.work_days)


class PatientCRUD():
    """CRUD для членов библиотеки"""

    def __init__(self):
        self.patient_list: Patient = []
        self.current_id = 1

    def create(self, name: str, phone: int) -> Patient:
        pat = Patient(name, phone, self.current_id)
        self.patient_list.append(pat)
        self.current_id += 1
        return pat

    def read_all(self):
        return self.patient_list

    def read_by_id(self, pat_id: int):
        for pat in self.patient_list:
            if pat.patient_id == pat_id:
                return pat
        return None

    def update(self, pat_id: int, name: str, phone: int):
        if self.current_id >= pat_id:
            self.patient_list[pat_id - 1] = Patient(name, phone, pat_id)
        else:
            raise (UpdateError('pat'))

    def delete(self, pat_id: int):
        pat = self.read_by_id(pat_id)
        if pat:
            self.patient_list.remove(pat)
            return f"Patient with id {pat_id} removed"
        return "Patient not found"

    def class_to_json(self):
        return {
            'patient_list': [pat.to_json() for pat in self.patient_list]
        }

    def from_json(self, data):
        for pat in data['patient_list']:
            self.create(pat['name'], pat['phone'])

    def class_to_xml(self, root: ElTree.Element):
        patients = ElTree.SubElement(root, 'Patients')
        for pat in self.patient_list:
            p = ElTree.SubElement(patients, 'Patient')
            p.set('name', pat.name)
            p.set('phone', str(pat.phone))
            p.set('patient_id', str(pat.patient_id))


class AccountCRUD():
    """CRUD для аккаунтов сайта больницы"""

    def __init__(self):
        self.account_list: Account = []
        self.current_id = 1

    def create(self, name: str, phone: int,
               login: str, passwd: str) -> Account:
        acc = Account(name, phone, self.current_id, login, passwd)
        self.account_list.append(acc)
        self.current_id += 1
        return acc

    def read_all(self):
        return self.account_list

    def read_by_id(self, acc_id: int):
        for acc in self.account_list:
            if acc.patient_id == acc_id:
                return acc
        return None

    def update(self, acc_id: int, name: str, phone: int,
               login: str, passwd: str):
        if self.current_id >= acc_id:
            self.account_list[acc_id - 1] = Account(name, phone, acc_id,
                                                    login, passwd)
        else:
            raise (UpdateError('acc'))

    def delete(self, acc_id: int):
        acc = self.read_by_id(acc_id)
        if acc:
            self.account_list.remove(acc)
            return f"Account with id {acc_id} removed"
        return "Account not found"

    def class_to_json(self):
        return {
            'account_list': [acc.to_json() for acc in self.account_list]
        }

    def from_json(self, data):
        for acc in data['account_list']:
            self.create(acc['name'], acc['phone'], acc['login'], acc['passwd'])

    def class_to_xml(self, root: ElTree.Element):
        accounts = ElTree.SubElement(root, 'Accounts')
        for acc in self.account_list:
            a = ElTree.SubElement(accounts, 'Account')
            a.set('name', acc.name)
            a.set('phone', str(acc.phone))
            a.set('patient_id', str(acc.patient_id))
            a.set('login', acc.login)
            a.set('passwd', acc.passwd)


class AmbulanceCRUD():
    """CRUD для пациентов, вызывающих скорую"""

    def __init__(self):
        self.ambulance_list: Ambulance = []

    def create(self, name: str, phone: int, address: str) -> Ambulance:
        amb = Ambulance(name, phone, address)
        self.ambulance_list.append(amb)
        return amb

    def read_all(self):
        return self.ambulance_list

    def read_by_address(self, address_search: str):
        for amb in self.ambulance_list:
            if amb.address == address_search:
                return amb
        return None

    def update(self, address_search: str, name: str,
               phone: int, address: str):
        amb = self.read_by_address(address_search)
        if amb:
            if name is not None:
                amb.name = name
            else:
                raise (UpdateError('name'))
            if phone is not None:
                amb.phone = phone
            else:
                raise (UpdateError('phone'))
            if address is not None:
                amb.address = address
            else:
                raise (UpdateError('address'))
            return amb
        else:
            raise (UpdateError('amb'))

    def delete(self, address_search: str):
        amb = self.read_by_address(address_search)
        if amb:
            self.ambulance_list.remove(amb)
            return f"Ambulance with address {address_search} removed"
        return "Ambulance not found"

    def class_to_json(self):
        return {
            'ambulance_list': [amb.to_json() for amb in self.ambulance_list]
        }

    def from_json(self, data):
        for amb in data['ambulance_list']:
            self.create(amb['name'], amb['phone'], amb['address'])

    def class_to_xml(self, root: ElTree.Element):
        ambulances = ElTree.SubElement(root, 'Ambulances')
        for amb in self.ambulance_list:
            a = ElTree.SubElement(ambulances, 'Ambulance')
            a.set('name', amb.name)
            a.set('phone', str(amb.phone))
            a.set('address', amb.address)


class SymptomCRUD():
    """CRUD для симптома"""

    def __init__(self):
        self.sym_list: Symptom = []

    def create(self, symname: str, severity: int) -> Symptom:
        symptom = Symptom(symname, severity)
        self.sym_list.append(symptom)
        return symptom

    def read_all(self):
        return self.sym_list

    def read_by_symname(self, symname_search: str):
        for symptom in self.sym_list:
            if symptom.symname == symname_search:
                return symptom
        return None

    def update(self, symname_search: str, symname: str, severity: int):
        symptom = self.read_by_symname(symname_search)
        if symptom:
            if symname is not None:
                symptom.symname = symname
            else:
                raise (UpdateError('symname'))
            if severity is not None:
                symptom.severity = severity
            else:
                raise (UpdateError('severity'))
            return symptom
        else:
            raise (UpdateError('symptom'))

    def delete(self, symname_search: str):
        symptom = self.read_by_symname(symname_search)
        if symptom:
            self.sym_list.remove(symptom)
            return f"Symptom with symname {symname_search} removed"
        return "Symptom not found"

    def class_to_json(self):
        return {
            'sym_list': [symptom.to_json() for symptom in self.sym_list]
        }

    def from_json(self, data):
        for sym in data['sym_list']:
            self.create(sym['symname'], sym['severity'])

    def class_to_xml(self, root: ElTree.Element):
        symptoms = ElTree.SubElement(root, 'Symptoms')
        for sym in self.sym_list:
            s = ElTree.SubElement(symptoms, 'Symptom')
            s.set('symname', sym.symname)
            s.set('severity', str(sym.severity))


class TreatmentCRUD():
    """CRUD для лечения симптомов"""

    def __init__(self):
        self.treat_list: Treatment = []

    def create(self, symname: str, severity: int, treatname: str, cost: int) -> Treatment:
        treatment = Treatment(symname, severity, treatname, cost)
        self.treat_list.append(treatment)
        return treatment

    def read_all(self):
        return self.treat_list

    def read_by_symname(self, symname_search: str):
        for treatment in self.treat_list:
            if treatment.symname == symname_search:
                return treatment
        return None

    def update(self, symname_search: str, symname: str,
               severity: int, treatname: str, cost: int):
        treatment = self.read_by_symname(symname_search)
        if treatment:
            if symname is not None:
                treatment.symname = symname
            else:
                raise (UpdateError('symname'))
            if severity is not None:
                treatment.severity = severity
            else:
                raise (UpdateError('severity'))
            if treatname is not None:
                treatment.treatname = treatname
            else:
                raise (UpdateError('treatname'))
            if cost is not None:
                treatment.cost = cost
            else:
                raise (UpdateError('cost'))
            return treatment
        else:
            raise (UpdateError('treatment'))

    def delete(self, symname_search: str):
        treatment = self.read_by_symname(symname_search)
        if treatment:
            self.treat_list.remove(treatment)
            return f"Treatment with symname {symname_search} removed"
        return "Treatment not found"

    def class_to_json(self):
        return {
            'treat_list': [treatment.to_json() for treatment in self.treat_list]
        }

    def from_json(self, data):
        for treatment in data['treat_list']:
            self.create(treatment['symname'], treatment['severity'],
                        treatment['treatname'], treatment['cost'])

    def class_to_xml(self, root: ElTree.Element):
        treatments = ElTree.SubElement(root, 'Treatments')
        for treatment in self.treat_list:
            t = ElTree.SubElement(treatments, 'Treatment')
            t.set('symname', treatment.symname)
            t.set('severity', str(treatment.severity))
            t.set('treatname', treatment.treatname)
            t.set('cost', str(treatment.cost))


class OrderCRUD():
    """CRUD для вызовов скорой"""

    def __init__(self):
        self.order_list: Order = []
        self.current_id = 1

    def create(self, symptom: Symptom, ambulance: Ambulance) -> Order:
        ordr = Order(symptom, ambulance, self.current_id)
        self.order_list.append(ordr)
        return ordr

    def read_all(self):
        return self.order_list

    def read_by_id(self, ord_id: int):
        for ordr in self.order_list:
            if ordr.ord_id == ord_id:
                return ordr
        return None

    def update(self, ord_id: int, symptom: Symptom, ambulance: Ambulance):
        if self.current_id >= ord_id:
            self.order_list[ord_id - 1] = Order(symptom, ambulance, ord_id)
        else:
            raise (UpdateError('ordr'))

    def delete(self, ord_id: int):
        ordr = self.read_by_id(ord_id)
        if ordr:
            self.order_list.remove(ordr)
            return f"Order with ID {ord_id} removed"
        return "Order not found"

    def class_to_json(self):
        return {
            'order_list': [ordr.to_json() for ordr in self.order_list]
        }

    def from_json(self, data):
        for ordr in data['order_list']:
            sym = ordr['symptom']
            amb = ordr['ambulance']
            self.create(Symptom(sym['symname'],
                                sym['severity']),
                        Ambulance(amb['name'],
                                  amb['phone'],
                                  amb['address']))

    def class_to_xml(self, root: ElTree.Element):
        orders = ElTree.SubElement(root, 'Orders')
        for ordr in self.order_list:
            o = ElTree.SubElement(orders, 'Order')
            o.set('ord_id', str(ordr.ord_id))

            sym = ElTree.SubElement(o, 'Symptom')
            sym.set('symname', ordr.symptom.symname)
            sym.set('severity', str(ordr.symptom.severity))

            amb = ElTree.SubElement(o, 'Ambulance')
            amb.set('name', ordr.ambulance.name)
            amb.set('phone', str(ordr.ambulance.phone))
            amb.set('address', ordr.ambulance.address)


class AmbulanceDriverCRUD():
    """CRUD для водителей скорой"""

    def __init__(self):
        self.driver_list: AmbulanceDriver = []
        self.current_id = 1

    def create(self, name: str, phone: int, order: Order) -> AmbulanceDriver:
        drive = AmbulanceDriver(name, phone, self.current_id, order)
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

    def update(self, drive_id: int, name: str = None,
               phone: int = None, order: Order = None):
        if self.current_id >= drive_id:
            self.driver_list[drive_id - 1] = AmbulanceDriver(name, phone,
                                                             drive_id, order)
        else:
            raise (UpdateError('drive'))

    def delete(self, drive_id: int):
        drive = self.read_by_id(drive_id)
        if drive:
            self.driver_list.remove(drive)
            return f"Driver with id {drive_id} removed"
        return "Driver not found"

    def class_to_json(self):
        return {
            'driver_list': [drive.to_json() for drive in self.driver_list]
        }

    def from_json(self, data):
        for drive in data['driver_list']:
            sym = drive['order']['symptom']
            amb = drive['order']['ambulance']
            self.create(drive['name'], drive['phone'],
                        Order(Symptom(sym['symname'],
                                      sym['severity']),
                              Ambulance(amb['name'],
                                        amb['phone'],
                                        amb['address']),
                              drive['order']['ord_id']))

    def class_to_xml(self, root: ElTree.Element):
        drivers = ElTree.SubElement(root, 'Drivers')
        for drive in self.driver_list:
            d = ElTree.SubElement(drivers, 'Driver')
            d.set('name', drive.name)
            d.set('phone', str(drive.phone))
            d.set('work_id', str(drive.work_id))

            ordr = ElTree.SubElement(d, 'Order')
            ordr.set('ord_id', str(drive.order.ord_id))

            sym = ElTree.SubElement(ordr, 'Symptom')
            sym.set('symname', drive.order.symptom.symname)
            sym.set('severity', str(drive.order.symptom.severity))

            amb = ElTree.SubElement(ordr, 'Ambulance')
            amb.set('name', drive.order.ambulance.name)
            amb.set('phone', str(drive.order.ambulance.phone))
            amb.set('address', drive.order.ambulance.address)


# -------------------Дополнительные классы и функции-------------------

class Hospital:
    """Обобщение всех CRUDов"""

    def __init__(self):
        self.doctor = DoctorCRUD()
        self.patient = PatientCRUD()
        self.account = AccountCRUD()
        self.ambulance = AmbulanceCRUD()
        self.symptom = SymptomCRUD()
        self.treatment = TreatmentCRUD()
        self.order = OrderCRUD()
        self.driver = AmbulanceDriverCRUD()


def all_to_json(hosp: Hospital):
    return {
        'doctor_crud': hosp.doctor.class_to_json(),
        'patient_crud': hosp.patient.class_to_json(),
        'account_crud': hosp.account.class_to_json(),
        'ambulance_crud': hosp.ambulance.class_to_json(),
        'symptom_crud': hosp.symptom.class_to_json(),
        'treatment_crud': hosp.treatment.class_to_json(),
        'order_crud': hosp.order.class_to_json(),
        'driver_crud': hosp.driver.class_to_json()
    }


def save_to_json(hosp: Hospital, file_name: str):
    json_obj = json.dumps(all_to_json(hosp), indent=4)
    with open(file_name, "w", encoding="utf-8") as outfile:
        outfile.write(json_obj)


def import_from_json(hosp: Hospital, file_name: str):
    with open(file_name, 'r', encoding='utf-8') as file:
        data = json.load(file)

    hosp.doctor.from_json(data['doctor_crud'])
    hosp.patient.from_json(data['patient_crud'])
    hosp.account.from_json(data['account_crud'])
    hosp.ambulance.from_json(data['ambulance_crud'])
    hosp.symptom.from_json(data['symptom_crud'])
    hosp.treatment.from_json(data['treatment_crud'])
    hosp.order.from_json(data['order_crud'])
    hosp.driver.from_json(data['driver_crud'])


def save_to_xml(hosp: Hospital, file_name: str):
    root = ElTree.Element('Hospital')
    hosp.doctor.class_to_xml(root)
    hosp.patient.class_to_xml(root)
    hosp.account.class_to_xml(root)
    hosp.ambulance.class_to_xml(root)
    hosp.symptom.class_to_xml(root)
    hosp.treatment.class_to_xml(root)
    hosp.order.class_to_xml(root)
    hosp.driver.class_to_xml(root)

    tree = ElTree.ElementTree(root)
    tree.write(file_name)


def import_from_xml(hosp: Hospital, file_name: str):
    tree = ElTree.parse(file_name)
    root = tree.getroot()
    for doc in root.find('Doctors'):
        hosp.doctor.create(doc.get('name'), int(doc.get('phone')),
                           doc.get('work_days'))
    for pat in root.find('Patients'):
        hosp.patient.create(pat.get('name'), int(pat.get('phone')))
    for acc in root.find('Accounts'):
        hosp.account.create(acc.get('name'), int(acc.get('phone')),
                            acc.get('login'), acc.get('passwd'))
    for amb in root.find('Ambulances'):
        hosp.ambulance.create(amb.get('name'), int(amb.get('phone')),
                              amb.get('address'))
    for sym in root.find('Symptoms'):
        hosp.symptom.create(sym.get('symname'), int(sym.get('severity')))
    for treat in root.find('Treatments'):
        hosp.treatment.create(treat.get('symname'), int(treat.get('severity')),
                              treat.get('treatname'), int(treat.get('cost')))
    for ordr in root.find('Orders'):
        sym = ordr.find('Symptom')
        amb = ordr.find('Ambulance')
        hosp.order.create(Symptom(sym.get('symname'),
                                  int(sym.get('severity'))),
                          Ambulance(amb.get('name'), int(amb.get('phone')),
                                    amb.get('address')))

    for drive in root.find('Drivers'):
        ordr = drive.find('Order')
        sym = ordr.find('Symptom')
        amb = ordr.find('Ambulance')
        drive_ordr = Order(Symptom(sym.get('symname'),
                                   int(sym.get('severity'))),
                           Ambulance(amb.get('name'), int(amb.get('phone')),
                                     amb.get('address')),
                           int(ordr.get('ord_id')))
        hosp.driver.create(drive.get('name'), int(drive.get('phone')),
                           drive_ordr)


def main():
    hospital = Hospital()

    # Создание
    hospital.doctor.create("Doctor 1", 21321, "Monday, Friday")
    hospital.doctor.create("Doctor 2", 21321, "Tuesday")
    hospital.patient.create("Patient", 21312)
    hospital.account.create("acc1", 123, "qwerty", "12345")
    hospital.account.create("acc2", 456, "logggiiiiin", "qwerty12345")
    hospital.ambulance.create("Dying Patient", 88005553535,
                              "Shosse Frezer, 10, Moscow, Russia, 109202")
    hospital.symptom.create("Coronavirus", 10)
    hospital.treatment.create("Cancer", 100, "Gummy bears", 1000)
    hospital.order.create(hospital.symptom.read_by_symname(
        "Coronavirus"), hospital.ambulance.read_by_address("Shosse Frezer, 10, Moscow, Russia, 109202"))
    hospital.driver.create("John Drive", 7777777, hospital.order.read_by_id(1))

    # Чтение
    print('Имена всех докторов:')
    print([doc.name for doc in hospital.doctor.read_all()], "\n")

    # Редактирование
    print('Имя пациента:\n', hospital.patient.read_by_id(1).name)
    hospital.patient.update(1, "New Patient Name", 123456)
    print('Новое имя пациента:\n', hospital.patient.read_by_id(1).name, "\n")

    # Удаление
    print('Аккаунты:\n', hospital.account.read_all())
    hospital.account.delete(1)
    print('Аккаунты после удаления:\n', hospital.account.read_all(), '\n')

    # Сохранение в json
    save_to_json(hospital, 'lab1/files/output.json')

    # Чтение из json
    hospital2 = Hospital()
    import_from_json(hospital2, 'lab1/files/test_data.json')
    print('Некоторые данные, импортированные из test_data.json')
    print(hospital2.doctor.read_by_id(3).name)
    print(hospital2.order.read_by_id(1).symptom.symname, '\n')

    # Сохранение в xml
    save_to_xml(hospital2, 'lab1/files/output.xml')

    # Чтение из xml
    hospital3 = Hospital()
    import_from_xml(hospital3, 'lab1/files/test_data.xml')
    print('Некоторые данные, импортированные из test_data.xml')
    for m in hospital3.doctor.read_all():
        print(m.name)


try:
    main()
except FileError as e:
    print('Error opening file ', e.filename)
except UpdateError as e:
    print('Error updating varibale ', e.var)
