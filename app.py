# app.py
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
            food = Food(category, name, brand, size_initial, unit,
                        packing, frozen_on, best_before, ean)
            freezer.foods.append(food)
            st.session_state.freezer = freezer
            st.write(freezer.foods)


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
        st.session_state_freezer_file = "data/freezer.json"
        try:
            freezer = load_freezer_obj_from_file(
                st.session_state.freezer_file, freezer)
        except:
            st.session_state.freezer = ""
        finally:
            st.session_state.app_initialized = True

    else:
        freezer = st.session_state.freezer
        print(freezer)
        print(freezer.foods)
        print(freezer.units)
        print(freezer.categories)

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


"""














@dataclass
class Unit:
    name:str
    rank:int

units = ["ml","gr","Stck"]    

def settings_units(units):
    # page title & header
    st.title("Einstellungen")
    st.subheader("Einheiten")

    unit = st.selectbox("Einheiten",["ml","gr","Stck"])

    st.write(unit)

    with st.container():
        st.text_input("Einheit",placeholder="z.B. Kg oder ml")
        st.number_input("Rang",min_value=1,max_value=9,value=9,step=1)
        




class Trip:
    def __init__(self) -> None:
        # input data from trip section
        self.description = ""
        self.boat = ""
        self.first_day = date.today()
        self.last_day = date.today() + timedelta(days=14)
        self.number_of_participants = 0
        # data derived from trip section
        self._number_of_nights = 0
        self._boat_rate = 0
        self._max_boat_total = 0
        # input data from participants section
        self.participants = []
        # data derived from participants section
        self._participants_nights = 0
        self._participants_nights_om = 0
        self._boat_rate_by_participant_night = 0
        self._is_skipper_discount_entitled = False
        self._total = 0
        # input data from skipper section
        self.skipper = ""
        self.skipper_IBAN = ""
        self.skipper_BIC = ""
        self.is_skipper_discount_desired = False

    def __str__(self):
        return f"({self.description},{self.boat},{self.first_day},{self.last_day},{self.number_of_participants},{self.number_of_nights},{self.boat_rate},{self.max_boat_total},{self.participants_nights},{self.participants_nights_om},{self.boat_rate_by_participant_night},{self.is_skipper_discount_entitled},{self.total},{self.skipper},{self.skipper_IBAN},{self.skipper_BIC},{self.is_skipper_discount_desired})"

    @property
    def number_of_nights(self):
        return (self.last_day - self.first_day).days

    @property
    def boat_rate(self):
        return Bootspauschalen.get(self.boat)

    @property
    def max_boat_total(self):
        return self.boat_rate * self.number_of_nights

    @property
    def participants_nights(self):
        return sum([participant.number_of_nights for participant in self.participants])

    @property
    def participants_nights_om(self):
        return sum(
            [participant.number_of_nights_om for participant in self.participants]
        )

    @property
    def boat_rate_by_participant_night(self):
        return self.max_boat_total / self.participants_nights

    @property
    def total(self):
        return sum([participant.boat_total for participant in self.participants]) + sum(
            [participant.extra_total[0] for participant in self.participants]
        )

    @property
    def is_skipper_discount_entitled(self):
        if self.participants_nights_om / self.participants_nights >= 0.5:
            return True
        else:
            return False


class Participant(Trip):
    def __init__(self, trip) -> None:
        # input data from participants section
        self.name = ""
        self.type = ""
        self.first_day = trip.first_day
        self.last_day = trip.last_day
        # data derived from participants section
        self._number_of_nights = 0
        self._number_of_nights_om = 0
        self._rate_group = ""
        self._extra_rate = 0
        # this is a tuple which returns a foot note as second item in case skipper discount is applied
        self._extra_total = 0, ""
        self._boat_total = 0
        # data derived from trip section
        self.trip = trip

    def __str__(self):
        return f"({self.name},{self.type},{self.first_day},{self.last_day},{self.number_of_nights},{self.number_of_nights_om},{self.rate_group},{self.extra_rate},{self.extra_total},{self.boat_total})"

    @property
    def number_of_nights(self):
        return (self.last_day - self.first_day).days

    @property
    def number_of_nights_om(self):
        if self.type == "OM":
            return self.number_of_nights
        else:
            return 0

    @property
    def rate_group(self):
        return Beitragsstufen.get(self.type)

    @property
    def extra_rate(self):
        return Beitragsstufenaufschläge.get(self.rate_group + " " + self.trip.boat)

    @property
    def extra_total(self):
        # this is a tuple which returns a foot note as second item in case skipper discount is applied
        if (
            self.trip.skipper == self.name
            and self.trip.is_skipper_discount_entitled
            and self.trip.is_skipper_discount_desired
        ):
            return (self.number_of_nights * 0), "(*)"
        else:
            return (self.number_of_nights * self.extra_rate), ""

    @property
    def boat_total(self):
       return round_up(
            self.number_of_nights * self.trip.boat_rate_by_participant_night)
"""
