import streamlit as st
from dataclasses import dataclass
from datetime import date, datetime
import json
from json import JSONEncoder


display = ("male", "female")

options = list(range(len(display)))

print(display)
print(len(display))
print(range(len(display)))
print(list(range(len(display))))

value = st.selectbox("gender", options, format_func=lambda x: display[x])

st.write(value)
