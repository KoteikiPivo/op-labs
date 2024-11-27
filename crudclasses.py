# Имплементации CRUD для классов из "classes.py"
from xml.etree import ElementTree as ElTree
from classes import *

class DoctorCRUD:
    """CRUD для докторов"""
    def __init__(self):
        self.doctor_list: Doctor = []
        self.current_id = 1

    def create(self, name: str, phone: int, work_days: str) -> Doctor:
        lib = Doctor(name, phone, self.current_id, work_days)
        self.doctor_list.append(lib)
        self.current_id += 1
        return lib
    
    def read_all(self):
        return self.doctor_list
    
    def read_by_id(self, lib_id: int):
        for lib in self.doctor_list:
            if lib.work_id == lib_id:
                return lib
        return None
    
    def update(self, lib_id: int, name: str = None,
               phone: int = None, work_days: str = None):
        lib = self.read_by_id(lib_id)
        if lib:
            if name is not None:
                lib.name = name
            else:
                raise(UpdateError('name'))
            if phone is not None:
                lib.phone = phone
            else:
                raise(UpdateError('phone'))
            if work_days is not None:
                lib.work_days = work_days
            else:
                raise(UpdateError('work_days'))
            return lib
        else:
            raise(UpdateError('lib'))
    
    def delete(self, lib_id: int):
        lib = self.read_by_id(lib_id)
        if lib:
            self.doctor_list.remove(lib)
            return f"Doctor with id {lib_id} removed"
        return "Doctor not found"
    
    def class_to_json(self):
        return {
            'doctor_list': [lib.to_json() for lib in self.doctor_list]
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
        pat = self.read_by_id(pat_id)
        if pat:
            if name is not None:
                pat.name = name
            else:
                raise(UpdateError('name'))
            if phone is not None:
                pat.phone = phone
            else:
                raise(UpdateError('name'))
            return pat
        else:
                raise(UpdateError('pat'))
    
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
        acc = self.read_by_id(acc_id)
        if acc:
            if name is not None:
                acc.name = name
            else:
                raise(UpdateError('name'))
            if phone is not None:
                acc.phone = phone
            else:
                raise(UpdateError('phone'))
            if login is not None:
                acc.login = login
            else:
                raise(UpdateError('login'))
            if passwd is not None:
                acc.passwd = passwd
            else:
                raise(UpdateError('passwd'))
            return acc
        else:
                raise(UpdateError('acc'))
    
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
                raise(UpdateError('name'))
            if phone is not None:
                amb.phone = phone
            else:
                raise(UpdateError('phone'))
            if address is not None:
                amb.address = address
            else:
                raise(UpdateError('address'))
            return amb
        else:
                raise(UpdateError('amb'))
    
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
                raise(UpdateError('symname'))
            if severity is not None:
                symptom.severity = severity
            else:
                raise(UpdateError('severity'))
            return symptom
        else:
                raise(UpdateError('symptom'))
    
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
               severity: int, treatname:str, cost: int):
        treatment = self.read_by_symname(symname_search)
        if treatment:
            if symname is not None:
                treatment.symname = symname
            else:
                raise(UpdateError('symname'))
            if severity is not None:
                treatment.severity = severity
            else:
                raise(UpdateError('severity'))
            if treatname is not None:
                treatment.treatname = treatname
            else:
                raise(UpdateError('treatname'))
            if cost is not None:
                treatment.cost = cost
            else:
                raise(UpdateError('cost'))
            return treatment
        else:
                raise(UpdateError('treatment'))
    
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
        ordr = self.read_by_id(ord_id)
        if ordr:
            if symptom is not None:
                ordr.symptom = symptom
            else:
                raise(UpdateError('symptom'))
            if ambulance is not None:
                ordr.ambulance = ambulance
            else:
                raise(UpdateError('symptom'))
            return ordr
        else:
                raise(UpdateError('ordr'))
    
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
        drive = self.read_by_id(drive_id)
        if drive:
            if name is not None:
                drive.name = name
            else:
                raise(UpdateError('name'))
            if phone is not None:
                drive.phone = phone
            else:
                raise(UpdateError('phone'))
            if order is not None:
                drive.order = order
            else:
                raise(UpdateError('order'))
            return drive
        else:
                raise(UpdateError('drive'))
    
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
