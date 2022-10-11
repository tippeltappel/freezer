# app.py
"""
Objekt mit Attributen aus simplen Datentypen kann mit obj.__dict__ zu einem Dictionary konvertiert werden.
Umgekehrt kann ein Dictionary mit obj=Obj(**dict) wieder in ein Objekt überführt werden.
Listen sollten mit obj=Obj(*list) in ein Objekt überführt werden können.
"""
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
    size_initial: float
    size_remaining: float
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


def enter_food(freezer):
    with st.form("enter_food", clear_on_submit=True):
        c1, c2, c3 = st.columns([1, 2, 1])
        category = c1.text_input("Lebensmittelart", placeholder="Gemüse")
        name = c2.text_input("Lebensmittel", placeholder="grüne Bohnen")
        brand = c3.text_input("Marke", placeholder="Hofgut")
        c1, c2, c3 = st.columns(3)
        size_initial = c1.number_input("Packungsgröße", step=25)
        unit = c2.text_input("Einheit", placeholder="gr")
        packing = c3.text_input("Verpackungsart", placeholder="Tüte")
        c1, c2, c3 = st.columns(3)
        frozen_on = c1.text_input(
            "Eingefroren am:", max_chars=10, placeholder="2022-08-22")
        best_before = c2.text_input(
            "Haltbar bis::", max_chars=10, placeholder="2022-11-21")
        ean = c3.text_input("EAN", max_chars=13)
        if st.form_submit_button("Speichern"):
            # ToDo: validation of food input
            food = Food(category, name, brand, size_initial, size_initial, unit,
                        packing, frozen_on, best_before, ean)
            # freezer.foods.append(food)
            # st.session_state.food_list = json.dumps(freezer.foods, indent=4)
            # st.json(freezer.foods)


def add_food(freezer):
    st.header("Einfrieren")
    add_type = st.radio("Wie hinzufügen?", [
                        "Neu", "Duplizieren"], horizontal=True, label_visibility="collapsed")
    if add_type == "Neu":
        enter_food(freezer)
    else:
        pass


def app():
    # browser tab title & favicon, "st.set_page_config" has to be first streamlit command in script
    st.set_page_config(
        page_title="Gefrierschrank", page_icon=":snowflake:")

    # initialize app
    st.session_state
    if 'app_initialized' not in st.session_state:
        freezer = Freezer(foods=[], units=[], categories=[])
        freezer_file = "data/test.json"
        try:
            # load a dictionary from file with the keys 'foods', 'units' and 'categories'
            with open(freezer_file, "r") as f:
                data = json.load(f)
            # extract values of the 3 dictionaries which are in turn lists of dictionaries
            food_list = data['foods']
            unit_list = data['units']
            category_list = data['categories']
        except:
            st.info("Willkommen bei der ersten Benutzung dieser App!")
            pass
        finally:
            st.session_state.app_initialized = True
            st.session_state.food_list = ""

    else:
        freezer.foods = json.loads(st.session_state.food_list)

    # page title & header
    st.title("Inhaltsverzeichnis")
    task = st.radio("Was willst Du tun?", [
                    "Einfrieren", "Auftauen"], horizontal=True, label_visibility="collapsed")
    if task == "Einfrieren":
        add_food(freezer)
    else:
        st.write("entnehmen")

    # end session
    if st.button("Sitzung beenden"):
        save_obj_to_json_file(
            freezer, st.session_state.freezer_file, FreezerEncoder)
        st.balloons()


if __name__ == "__main__":
    app()
