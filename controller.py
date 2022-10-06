# controller.py
import json
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
class Freezer(object):
    units: list[Unit]
    categories: list[Category]

# filepathes
units_file = "data/units.json"

# test data
freezer = Freezer
freezer.units = [{"name":"ml","rank":88},{"name":"gr","rank":88}]   
freezer.categories = [{"name":"Gemüse","rank":11},{"name":"Fleisch","rank":22}]   

def units_obj_save(file_name):
    with open (file_name,"w") as f:
        json.dump(freezer,f,indent=4)

def units_obj_load(file_name):
    with open (file_name,"r") as f:
        return json.load(f)

print(freezer)
#units_obj_save(units_file) 
#freezer.units=units_obj_load(units_file)       
#print(freezer.units)