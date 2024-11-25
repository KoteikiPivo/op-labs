# Вариант 11 - Предметная область поликлиники

import json
from classes import *
from crudclasses import *

class Hospital:
    """Класс больницы"""
    def __init__(self):
        self.doctor = DoctorCRUD()
        self.patient = PatientCRUD()
        self.account = AccountCRUD()
        self.ambulance = AmbulanceCRUD()
        self.symptom = SymptomCRUD()
        self.treatment = TreatmentCRUD()
        self.order = OrderCRUD()
        self.driver = AmbulanceDriverCRUD()
    
    def all_to_json(self):
        return {
            'doctor_crud': self.doctor.class_to_json(),
            'patient_crud': self.patient.class_to_json(),
            'account_crud': self.account.class_to_json(),
            'ambulance_crud': self.ambulance.class_to_json(),
            'symptom_crud': self.symptom.class_to_json(),
            'treatment_crud': self.treatment.class_to_json(),
            'order_crud': self.order.class_to_json(),
            'driver_crud': self.driver.class_to_json()
        }



hospital = Hospital()
# Использование CRUD классов для заполнения данных
hospital.doctor.create("Doctor 1",21321,"Monday, Friday")
hospital.doctor.create("Doctor 2",21321,"Tuesday")
hospital.patient.create("Patient", 21312)
hospital.account.create("acc1", 123, "qwerty", "12345")
hospital.account.create("acc2", 456, "logggiiiiin", "qwerty12345")
hospital.ambulance.create("Dying Patient", 88005553535, 
                          "Shosse Frezer, 10, Moscow, Russia, 109202")
hospital.symptom.create("Coronavirus", 10)
hospital.treatment.create("Cancer", 100, "Gummy bears", 1000)
hospital.order.create(hospital.symptom.read_by_symname("Coronavirus"), hospital.ambulance.read_by_address("Shosse Frezer, 10, Moscow, Russia, 109202"))
hospital.driver.create("John Drive", 7777777, hospital.order.read_by_id(1))

# Чтение
print([doc.name for doc in hospital.doctor.read_all()], "\n")

# Редактирование
print(hospital.patient.read_by_id(1).name)
hospital.patient.update(1, "New Patient Name", 123456)
print(hospital.patient.read_by_id(1).name, "\n")

# Удаление
print(hospital.account.read_all())
hospital.account.delete(1)
print(hospital.account.read_all())

# Сохранение в json
try:
    json_obj = json.dumps(hospital.all_to_json(), indent=4)
except AttributeError:
    print("Error: Couldn't find a class through the 'read_by' function")

try:
    with open("sample.json", "w", encoding="utf-8") as outfile:
        outfile.write(json_obj)
except NameError:
    print("Error: Couldn't export data to json")
