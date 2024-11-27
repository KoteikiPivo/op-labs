# Вариант 11 - Предметная область поликлиники/больницы
import json
from classes import *
from crudclasses import *


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
    if not isinstance(file_name, str):
        raise FileError(file_name)
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
    save_to_json(hospital,"files/output.json")


    # Чтение из json
    hospital2 = Hospital()
    import_from_json(hospital2, 'files/test_data.json')
    print('Некоторые данные, импортированные из test_data.json')
    print(hospital2.doctor.read_by_id(3).name)
    print(hospital2.order.read_by_id(1).symptom.symname, '\n')


    # Сохранение в xml
    save_to_xml(hospital2, 'files/output.xml')


    # Чтение из xml
    hospital3 = Hospital()
    import_from_xml(hospital3, 'files/test_data.xml')
    print('Некоторые данные, импортированные из test_data.xml')
    for m in hospital3.doctor.read_all():
        print(m.name)


try:
    main()
except FileError as e:
    print('Error opening file ', e.filename)
except UpdateError as e:
    print('Error updating varibale ', e.var)