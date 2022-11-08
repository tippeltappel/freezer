import streamlit as st
from datetime import date, datetime

st.session_state
d1 = st.date_input("enter date:", key="d1")
iso = d1.isoformat()
print(iso)
d2 = st.date_input("enter date:", value=st.session_state.d1, key="d2")
