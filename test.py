# test.py
import json
from typing import List

# load a dictionary from file with the keys 'foods', 'units',packings and 'categories'
freezer_file = "data/test.json"
with open(freezer_file, "r") as f:
    data = json.load(f)
print('var data: ' + str(type(data)))   
# extract #
# units = []
foods = data['foods']
print('var foods: ' + str(type(foods)))   
units = data['units']
print('var units: ' + str(type(units)))   
#print(units)
#units.sorted(key=lambda x: x.get('rank'))

#print(type(units))
#categories = data['categories']
#print(categories)
#categories.sort(key=lambda x: x.get('rank'))
#print(categories)
#unit_dropdown = units
#print(unit_dropdown)
#unit_dropdown.filter(key=lambda x: x.get('name'))
#print(unit_dropdown)
