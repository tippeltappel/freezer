# app.py
"""
Objekt mit Attributen aus simplen Datentypen kann mit obj.__dict__ zu einem Dictionary konvertiert werden.
Umgekehrt kann ein Dictionary mit obj=Obj(**dict) wieder in ein Objekt überführt werden.
Listen sollten mit obj=Obj(*list) in ein Objekt überführt werden können.
"""
import streamlit as st
from dataclasses import dataclass
from datetime import date, timedelta, datetime
import json
from json import JSONEncoder


@dataclass
class Food:
    category: str
    name: str
    brand: str
    packing: str
    size_initial: int
    size_remaining: int
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
class Packing:
    name: str
    rank: int


@dataclass
class Freezer:
    foods: list[Food]
    categories: list[Category]
    units: list[Unit]
    packings: list[Packing]


class FreezerEncoder(JSONEncoder):
    def default(self, freezer):
        return ({"foods": freezer.foods, "units": freezer.units, "categories": freezer.categories, "packings": freezer.packings})


def init_app():
    # browser tab title & favicon, "st.set_page_config" has to be first streamlit command in script
    st.set_page_config(
        page_title="Gefrierschrank", page_icon=":snowflake:", initial_sidebar_state="auto")
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
            freezer.packings = data['packings']
            # save freezer attributes in session state
            st.session_state.food_list = freezer.foods
            st.session_state.unit_list = freezer.units
            st.session_state.category_list = freezer.categories
            st.session_state.packing_list = freezer.packings

            # st.session_state

        except:
            # state: App used for the first time
            st.success("Willkommen bei der ersten Benutzung dieser App!")
            st.session_state.food_list = []
            st.session_state.unit_list = []
            st.session_state.category_list = []
            st.session_state.packing_list = []
            # st.session_state

        finally:
            st.session_state.app_initialized = True

    else:
        # state: App was refreshed after data entry
        # load data from session state
        freezer.foods = st.session_state.food_list
        freezer.units = st.session_state.unit_list
        freezer.categories = st.session_state.category_list
        freezer.packings = st.session_state.packing_list
        # st.session_state


def cb_enter_food():
    food = Food(st.session_state.f1_category,
                st.session_state.f1_name,
                st.session_state.f1_brand,
                st.session_state.f1_packing,
                st.session_state.f1_size_initial,
                st.session_state.f1_size_initial,  # default for size_remaining
                st.session_state.f1_unit,
                st.session_state.f1_ean,
                st.session_state.f1_frozen_on.isoformat(),
                st.session_state.f1_best_before.isoformat(),
                st.session_state.f1_bin)

    freezer.foods.append(food.__dict__)
    st.session_state.food_list = freezer.foods


def enter_food():
    ranked_categories = sorted(freezer.categories, key=lambda i: i['rank'])
    names_of_ranked_categories = [category['name']
                                  for category in ranked_categories]
    ranked_units = sorted(freezer.units, key=lambda i: i['rank'])
    names_of_ranked_units = [unit['name'] for unit in ranked_units]
    ranked_packings = sorted(freezer.packings, key=lambda i: i['rank'])
    names_of_ranked_packings = [packing['name'] for packing in ranked_packings]
    with st.form("f1", clear_on_submit=True):
        c1, c2, c3 = st.columns([1, 2, 1])
        c1.selectbox("Lebensmittelart",
                     names_of_ranked_categories, key="f1_category")
        c2.text_input("Lebensmittel",
                      placeholder="grüne Bohnen", key="f1_name")
        c3.text_input("Marke", placeholder="Hofgut", key="f1_brand")
        c1, c2, c3 = st.columns(3)
        c1.selectbox("Verpackungsart",
                     names_of_ranked_packings, key="f1_packing")
        c2.number_input("Inhaltsmenge", step=1, key="f1_size_initial")
        c3.selectbox("Maßeinheit", names_of_ranked_units, key="f1_unit")
        c1, c2, c3, c4 = st.columns(4)
        c1.text_input("EAN", max_chars=13, key="f1_ean")
        # c2.text_input("Eingefroren am:", max_chars=10, placeholder="2022-08-22", key="f1_frozen_on")
        c2.date_input("Eingefroren am:", key="f1_frozen_on")
        # c3.text_input("Haltbar bis:", max_chars=10,placeholder="2022-11-21", key="f1_best_before")
        c3.date_input("Haltbar bis:", value=date.today() +
                      timedelta(days=91), key="f1_best_before")
        c4.number_input("Fach", min_value=1,
                        max_value=max_bins, step=1, key="f1_bin")
        # ToDo: validation of food input
        if st.form_submit_button("Speichern", on_click=cb_enter_food):
            st.success(
                st.session_state.food_list[-1]['name'] + " wurde der Liste hinzugefügt")


def add_food():
    st.header("Einlagern")
    add_type = st.radio("Wie hinzufügen?", [
                        "Eintippen", "Duplizieren"], horizontal=True, label_visibility="visible")
    if add_type == "Eintippen":
        enter_food()
    else:
        pass


def cb_remove_food(i):
    st.session_state.food_name = freezer.foods[i]['name']
    freezer.foods.pop(i)
    st.session_state.food_list = freezer.foods


def remove_food():
    st.header("Auslagern")
    foods_index_list = list(range(len(freezer.foods)))
    i = st.selectbox("Gefriergut auswählen", foods_index_list,
                     format_func=lambda i: freezer.foods[i].get('name') + " - " + freezer.foods[i].get('brand') + " - " + freezer.foods[i].get('packing') + " - " + str(freezer.foods[i].get('size_remaining'))+"/" + str(freezer.foods[i].get('size_initial')) + " "+freezer.foods[i].get('unit') + " #"+freezer.foods[i].get('frozen_on') + "/ #"+freezer.foods[i].get('best_before')+" --> Fach: "+str(freezer.foods[i].get('bin')))
    food = Food(**freezer.foods[i])
    # st.write(food.__dict__)

    if st.button("Auslagern", on_click=cb_remove_food, args=[i]):
        st.success(st.session_state.food_name +
                   " wurde von der Liste gelöscht")


def cb_edit_food(i):
    st.session_state.food_name = st.session_state.f2_name
    food = Food(st.session_state.f2_category,
                st.session_state.f2_name,
                st.session_state.f2_brand,
                st.session_state.f2_packing,
                st.session_state.f2_size_initial,
                st.session_state.f2_size_remaining,
                st.session_state.f2_unit,
                st.session_state.f2_ean,
                st.session_state.f2_frozen_on.isoformat(),
                st.session_state.f2_best_before.isoformat(),
                st.session_state.f2_bin)

    freezer.foods[i] = food.__dict__
    st.session_state.food_list = freezer.foods


def edit_food():
    st.header("Bearbeiten")
    foods_index_list = list(range(len(freezer.foods)))
    i = st.selectbox("Gefriergut auswählen", foods_index_list,
                     format_func=lambda i: freezer.foods[i].get('name') + " - " + freezer.foods[i].get('brand') + " - " + freezer.foods[i].get('packing') + " - " + str(freezer.foods[i].get('size_remaining'))+"/" + str(freezer.foods[i].get('size_initial')) + " "+freezer.foods[i].get('unit') + " #"+freezer.foods[i].get('frozen_on') + "/ #"+freezer.foods[i].get('best_before')+" --> Fach: "+str(freezer.foods[i].get('bin')))
    food = Food(**freezer.foods[i])

    ranked_categories = sorted(freezer.categories, key=lambda i: i['rank'])
    names_of_ranked_categories = [category['name']
                                  for category in ranked_categories]
    ranked_units = sorted(freezer.units, key=lambda i: i['rank'])
    names_of_ranked_units = [unit['name'] for unit in ranked_units]
    ranked_packings = sorted(freezer.packings, key=lambda i: i['rank'])
    names_of_ranked_packings = [packing['name'] for packing in ranked_packings]
    with st.form("f2", clear_on_submit=True):
        c1, c2, c3 = st.columns([1, 2, 1])
        c1.selectbox("Lebensmittelart", names_of_ranked_categories,
                     index=names_of_ranked_categories.index(food.category), key="f2_category")
        c2.text_input("Lebensmittel", food.name, key="f2_name")
        c3.text_input("Marke", food.brand, key="f2_brand")
        c1, c2, c3 = st.columns(3)
        c1.selectbox("Verpackungsart",
                     names_of_ranked_packings, key="f2_packing")
        c2.number_input("ursprüngliche Inhaltsmenge", int(
            food.size_initial), step=1, key="f2_size_initial")
        c3.selectbox("Maßeinheit", names_of_ranked_units, key="f2_unit")
        c1, c2, c3, c4 = st.columns(4)
        c1.text_input("EAN", food.ean, max_chars=13, key="f2_ean")
        c2.date_input("Eingefroren am:", value=datetime.fromisoformat(
            food.frozen_on), key="f2_frozen_on")
        c3.date_input("Haltbar bis:", value=datetime.fromisoformat(
            food.best_before), key="f2_best_before")
        c4.number_input("Fach", min_value=1, max_value=max_bins,
                        value=int(food.bin), step=1, key="f2_bin")
        st.number_input("verbleibende Inhaltsmenge",
                        int(food.size_remaining), step=1, key="f2_size_remaining")

        if st.form_submit_button("Speichern", on_click=cb_edit_food, args=[i]):
            st.success(st.session_state.food_name +
                       " wurde in der Liste geändert")

def cb_edit_settings(setting):
    match setting:
        case "categories":
            freezer.categories=st.session_state.category_list
        case "units":
            freezer.units=st.session_state.unit_list
        case "packings":
            freezer.packings=st.session_state.packing_list



def edit_settings():
    st.header("Einstellungen bearbeiten")
    task = st.radio("Wähle zu ändernde Einstellung", [
        "Kategorien", "Maßeinheiten", "Verpackungen"], horizontal=True, label_visibility="visible")
    match task:
        case "Kategorien":
            st.text_area("Kategorien",freezer.categories,height=200,on_change=cb_edit_settings,args=("categories",),key="category_list")
        case "Maßeinheiten":
            st.text_area("Maßeinheiten",freezer.units,height=200,on_change=cb_edit_settings,args=("units",),key="unit_list")
        case "Verpackungen":
            st.text_area("Verpackungen",freezer.packings,height=200,on_change=cb_edit_settings,args=("packings",),key="packing_list")


def save_freezer(obj, file_name, custom_encoder):
    with open(file_name, "w") as f:
        json.dump(obj, f, ensure_ascii=False, indent=4, cls=custom_encoder)


def quit_app():
    save_freezer(freezer, freezer_file, FreezerEncoder)
    del st.session_state.app_initialized
    st.balloons()
    st.stop()


def app():
    init_app()
    # page title & header
    st.title("Gefrierschrank")
    task = st.radio("Waas du wollen tuun?", [
        "Einlagern", "Auslagern", "Bearbeiten","Einstellungen bearbeiten"], horizontal=True, label_visibility="visible")
    match task:
        case "Einlagern":
            add_food()
        case "Auslagern":
            remove_food()
        case "Bearbeiten":
            edit_food()
        case "Einstellungen bearbeiten":
            edit_settings()    

    # end session
    if st.button("Sitzung speichern & beenden", type='primary'):
        quit_app()


if __name__ == "__main__":
    freezer = Freezer
    freezer_file = "data/test.json"
    max_bins = 8
    app()
