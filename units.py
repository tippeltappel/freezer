from dataclasses import dataclass
from typing import List,Optional
import streamlit as st

@dataclass
class Unit:
    name:str
    rank:int

unit1 = Unit("ml",99)
unit2 = Unit("gr",88)
unit3 = Unit("Stck.",77)
unit4 = Unit("Kg",66)
units =[unit1,unit2,unit3,unit4]
units.sort(key=lambda x: x.rank)

def unit_settings(units):
    unit_name,unit_rank,del_button=st.columns(3)
    for i in range(len(units)):
        units[i].name=unit_name.text_input("Einheit",value=units[i].name,label_visibility="collapsed") 
        units[i].rank=unit_rank.number_input("Rang",value=units[i].rank,label_visibility="collapsed")
        del_button.button("DEL",key="unit_del_button"+str(i))     


if __name__ == "__main__":
    unit_settings(units)
    
    
    #index = st.selectbox("Einheiten", range(len(units)), format_func=lambda x: units[x].name)

    #st.write("units:", units[index].rank)
    #st.write("index:", index)
    