# test.py
import json
from typing import List

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
