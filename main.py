# Вариант 1 - Предметная область библиотеки

from classes import *
from crudclasses import *
import json


membs = MemberCRUD()
libs1 = membs.create("AAA", 123)
libs2 = membs.create("BBB", 435)

json_obj = json.dumps(membs.all_to_json(), indent=4)

with open("sample.json", "w", encoding="utf-8") as outfile:
    outfile.write(json_obj)
