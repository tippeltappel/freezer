from dataclasses import dataclass
from typing import List,Optional
import streamlit as st

@dataclass
class Unit:
    name:str
    rank:int =99


if __name__ == "__main__":
    unit1 = Unit("ml",99)
    unit2 = Unit("gr",88)
    unit3 = Unit("Stck.",77)
    unit4 = Unit("Kg",66)
    units =[unit1,unit2,unit3,unit4]
    print(units)
    units.sort(key=lambda x: x.rank)
    print(units)
    
    index = st.selectbox("Einheiten", range(len(units)), format_func=lambda x: units[x].name)

    #st.write("units:", units[index].rank)
    #st.write("index:", index)
    