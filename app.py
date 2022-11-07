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
    packing: str
    size_initial: float
    size_remaining: float
    unit: str
    ean: str
    frozen_on: str
    best_before: str
    bin: int


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


def save_freezer(obj, file_name, custom_encoder):
    with open(file_name, "w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=4, cls=custom_encoder)


def quit_app(freezer, freezer_file):
    save_freezer(freezer, freezer_file, FreezerEncoder)
    del st.session_state.app_initialized
    st.balloons()


def cb_enter_food():
    food = Food(st.session_state.f1_category,
                st.session_state.f1_name,
                st.session_state.f1_brand,
                st.session_state.f1_packing,
                st.session_state.f1_size_initial,
                st.session_state.f1_size_initial,  # default for size_remaining
                st.session_state.f1_unit,
                st.session_state.f1_ean,
                st.session_state.f1_frozen_on,
                st.session_state.f1_best_before,
                st.session_state.f1_bin)

    freezer.foods.append(food.__dict__)
    st.session_state.food_list = freezer.foods


def enter_food():
    with st.form("f1", clear_on_submit=False):
        c1, c2, c3 = st.columns([1, 2, 1])
        c1.text_input("Lebensmittelart",
                      placeholder="Gemüse", key="f1_category")
        c2.text_input("Lebensmittel",
                      placeholder="grüne Bohnen", key="f1_name")
        c3.text_input("Marke", placeholder="Hofgut", key="f1_brand")
        c1, c2, c3 = st.columns(3)
        c1.text_input("Verpackungsart", placeholder="Tüte", key="f1_packing")
        c2.number_input("Packungsgröße", step=25, key="f1_size_initial")
        c3.text_input("Einheit", placeholder="gr", key="f1_unit")
        c1, c2, c3, c4 = st.columns(4)
        c1.text_input("EAN", max_chars=13, key="ean")
        c2.text_input(
            "Eingefroren am:", max_chars=10, placeholder="2022-08-22", key="f1_frozen_on")
        c3.text_input("Haltbar bis:", max_chars=10,
                      placeholder="2022-11-21", key="f1_best_before")
        c4.number_input("Fach", step=1, key="f1_bin")
        # ToDo: validation of food input
        st.form_submit_button("Speichern", on_click=cb_enter_food)


def add_food():
    st.header("Einlagern")
    add_type = st.radio("Wie hinzufügen?", [
                        "Neu", "Duplizieren"], horizontal=True, label_visibility="visible")
    if add_type == "Neu":
        enter_food()
        pass
    else:
        pass


def edit_food():
    st.header("Bearbeiten")
    foods_index_list = list(range(len(freezer.foods)))
    i = st.selectbox("Gefriergut auswählen", foods_index_list,
                     format_func=lambda i: freezer.foods[i].get('name') + " - " + freezer.foods[i].get('brand') + " - " + freezer.foods[i].get('packing') + " - " + str(freezer.foods[i].get('size_remaining'))+"/" + str(freezer.foods[i].get('size_initial')) + " "+freezer.foods[i].get('unit')+" --> Fach: "+str(freezer.foods[i].get('bin')))
    food = Food(**freezer.foods[i])

    with st.form("edit_food", clear_on_submit=True):
        c1, c2, c3 = st.columns([1, 2, 1])
        category = c1.text_input("Lebensmittelart", food.category)
        name = c2.text_input("Lebensmittel", food.name)
        brand = c3.text_input("Marke", food.brand)
        c1, c2, c3 = st.columns(3)
        packing = c1.text_input("Verpackungsart", food.packing)
        size_initial = c2.number_input(
            "ursprünglicher Packungsgröße", float(food.size_initial), step=1.0)
        unit = c3.text_input("Einheit", food.unit)

        c1, c2, c3, c4 = st.columns(4)
        ean = c1.text_input("EAN", food.ean, max_chars=13)
        frozen_on = c2.text_input(
            "Eingefroren am:", food.frozen_on, max_chars=10)
        best_before = c3.text_input(
            "Haltbar bis:", food.best_before, max_chars=10)
        bin = c4.number_input("Fach", int(food.bin), step=1)

        size_remaining = st.number_input(
            "verbleibende Packungsgröße", float(food.size_initial), step=1.0)
        size_remaining = st.slider(
            "verbleibende Packungsgröße", float(food.size_remaining), step=1.0)

        if st.form_submit_button("Auslagern"):
            # ToDo: validation of food input
            food = Food(category, name, brand, packing, size_initial, size_initial,
                        unit, ean, frozen_on, best_before, bin)
            freezer.foods.append(food.__dict__)
            st.session_state.food_list = freezer.foods


def remove_food():
    def remove_food_callback(i):
        freezer.foods.pop(i)
        st.session_state.food_list = freezer.foods

    st.header("Auslagern")
    foods_index_list = list(range(len(freezer.foods)))
    i = st.selectbox("Gefriergut auswählen", foods_index_list,
                     format_func=lambda i: freezer.foods[i].get('name') + " - " + freezer.foods[i].get('brand') + " - " + freezer.foods[i].get('packing') + " - " + str(freezer.foods[i].get('size_remaining'))+"/" + str(freezer.foods[i].get('size_initial')) + " "+freezer.foods[i].get('unit')+" --> Fach: "+str(freezer.foods[i].get('bin')))
    food = Food(**freezer.foods[i])
    st.json(food.__dict__)

    st.button("Auslagern", on_click=remove_food_callback, args=[i])


def app():
    # browser tab title & favicon, "st.set_page_config" has to be first streamlit command in script
    st.set_page_config(
        page_title="Gefrierschrank", page_icon=":snowflake:")
    # initialize app
    if 'app_initialized' not in st.session_state:
        # stete: App was just opened
        try:
            # state: App has been used before with data probably saved to file
            # load a dictionary from file with the keys 'foods', 'units' and 'categories'
            with open(freezer_file, "r") as f:
                data = json.load(f)
            # extract values of the 3 dictionaries which are in turn lists of dictionaries
            freezer.foods = data['foods']
            freezer.units = data['units']
            freezer.categories = data['categories']
            # save freezer attributes in session state
            st.session_state.food_list = freezer.foods
            st.session_state.unit_list = freezer.units
            st.session_state.category_list = freezer.categories
            st.session_state

        except:
            # state: App used for the first time
            st.success("Willkommen bei der ersten Benutzung dieser App!")
            st.session_state.food_list = []
            st.session_state.unit_list = []
            st.session_state.category_list = []
            st.session_state

        finally:
            st.session_state.app_initialized = True

    else:
        # state: App was refreshed after data entry
        # load data from session state
        freezer.foods = st.session_state.food_list
        freezer.units = st.session_state.unit_list
        freezer.categories = st.session_state.category_list
        # st.session_state

    # page title & header
    st.title("Inhaltsverzeichnis")
    task = st.radio("Was willst Du tun?", [
        "Einlagern", "Auslagern", "Bearbeiten"], horizontal=True, label_visibility="visible")
    match task:
        case "Einlagern":
            add_food()
        case "Auslagern":
            remove_food()
        case "Bearbeiten":
            edit_food()

    # end session
    if st.button("Sitzung speichern & beenden"):
        quit_app()


if __name__ == "__main__":
    freezer = Freezer
    freezer_file = "data/test.json"
    app()
