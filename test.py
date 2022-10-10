# test.py
import json
from typing import List


def save_obj_to_json_file(obj, file_name, custom_encoder):
    with open(file_name, "w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=4, cls=custom_encoder)


 # load a dictionary from file with the keys 'foods', 'units' and 'categories'
freezer_file = "data/test.json"
with open(freezer_file, "r") as f:
    data = json.load(f)
# extract values of the 3 dictionaries which are lists of dictionaries in turn
units = []
foods = data['foods']
units = data['units']
print(units)
units.sort(key=lambda x: x.get('rank'))
print(units)
categories = data['categories']
print(categories)
categories.sort(key=lambda x: x.get('rank'))
print(categories)
unit_dropdown = units
print(unit_dropdown)
#unit_dropdown.filter(key=lambda x: x.get('name'))
print(unit_dropdown)
