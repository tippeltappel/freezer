import streamlit as st
from dataclasses import dataclass
from datetime import date, datetime
import json
from json import JSONEncoder


@dataclass
class Food:
    category: str
    name: str
    brand: str
    size_initial: int
    unit: str
    packing: str
    frozen_on: str
    best_before: str
    ean: str


@dataclass
class Category:
    name: str
    rank: int


@dataclass
class Unit:
    name: str
    rank: int


@dataclass
class Freezer:
    foods: list[Food]
    categories: list[Category]
    units: list[Unit]


freezer = Freezer
unit1_dict = {"name": "ml", "rank": 77}
print("---------------------------")
print(unit1_dict)
print(unit1_dict['name'])
print(json.dumps(unit1_dict, indent=4))
dict = json.loads(json.dumps(unit1_dict))
print(dict)
print(dict['rank'])
#unit1 = json.loads(json.dumps(unit1_dict), object_hook=Unit)
unit1 = Unit
unit1.name = "ml"
unit1.rank = "66"


freezer.foods = [{"name": "grüne Bohnen", "brand": "Hofgut", "size_initial": "750", "unit": "gr."},
                 {"name": "Pizza Hawaii", "brand": "Dr.Oetker", "size_initial": "1", "unit": "St."}]
freezer.units = [{"name": "ml", "rank": 88}, {"name": "gr", "rank": 88}]
freezer.categories = [{"name": "Gemüse", "rank": 11},
                      {"name": "Fleisch", "rank": 22}]

# st.write(freezer.foods[0]['name'])
