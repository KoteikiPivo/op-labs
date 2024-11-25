# Вариант 11 - Предметная область поликлиники

import json
from classes import *
from crudclasses import *



pat = PatientCRUD()
libs1 = pat.create("AAA", 123)
libs2 = pat.create("BBB", 435)

json_obj = json.dumps(pat.all_to_json(), indent=4)

with open("sample.json", "w", encoding="utf-8") as outfile:
    outfile.write(json_obj)
