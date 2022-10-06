# test.py
import json
from json import JSONEncoder
from dataclasses import dataclass

@dataclass
class Unit:
    name: str
    rank: int

@dataclass
class Category:
    name: str
    rank: int

@dataclass
class Freezer:
    units: list[Unit]
    categories: list[Category]

class FreezerEncoder(JSONEncoder):
    def default(self, freezer):
        return ({"units":freezer.units},{"categories":freezer.categories})

# filepathes
units_file = "data/test.json"

# test data
freezer = Freezer
freezer.units = [{"name":"ml","rank":88},{"name":"gr","rank":88}]   
freezer.categories = [{"name":"Gemüse","rank":11},{"name":"Fleisch","rank":22}]   

def units_obj_save(file_name):
    with open (file_name,"w") as f:
        f.write(jsonpickle.encode(freezer))

def units_obj_load(file_name):
    with open (file_name,"r") as f:
        return json.load(f)

print(freezer.units)
print(freezer.categories)
JSONStr=json.dumps(freezer,indent=4,cls=FreezerEncoder)
print(JSONStr)
freezer=json.loads(JSONStr,cls=FreezerEncoder)
#units_obj_save(units_file) 
#freezer.units=units_obj_load(units_file)       
print(freezer.units)
print(freezer.categories)