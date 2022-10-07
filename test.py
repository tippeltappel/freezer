# test.py
from hashlib import new
import json
from json import JSONEncoder
from dataclasses import dataclass


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
class Unit:
    name: str
    rank: int


@dataclass
class Category:
    name: str
    rank: int


@dataclass
class Freezer:
    foods: list[Food]
    units: list[Unit]
    categories: list[Category]


class FreezerEncoder(JSONEncoder):
    def default(self, freezer):
        return ({"foods": freezer.foods, "units": freezer.units, "categories": freezer.categories})


def save_obj_to_json_file(obj, file_name, custom_encoder):
    with open(file_name, "w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=4, cls=custom_encoder)


def load_freezer_obj_from_file(file_name, obj):
    with open(file_name, "r") as f:
        dict_data = json.load(f)
    obj.foods = dict_data["foods"]
    obj.units = dict_data["units"]
    obj.categories = dict_data["categories"]
    return obj


# filepathes
freezer_file = "data/test.json"

# test data
freezer = Freezer
freezer.foods = [{"name": "grüne Bohnen", "brand": "Hofgut", "size_initial": "750", "unit": "gr."},
                 {"name": "Pizza Hawaii", "brand": "Dr.Oetker", "size_initial": "1", "unit": "St."}]
freezer.units = [{"name": "ml", "rank": 88}, {"name": "gr", "rank": 88}]
freezer.categories = [{"name": "Gemüse", "rank": 11},
                      {"name": "Fleisch", "rank": 22}]


save_obj_to_json_file(freezer, freezer_file, FreezerEncoder)

freezer = load_freezer_obj_from_file(freezer_file, freezer)
JSONStr = json.dumps(freezer, ensure_ascii=False, indent=4, cls=FreezerEncoder)
print(JSONStr)
print(freezer)
