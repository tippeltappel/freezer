import streamlit as st


def callback1():
    st.session_state


def callback2():
    st.session_state


st.text_input("enter some text", on_change=callback1, key="text1")


with st.form("form1"):
    st.text_input("Name:", key="name")
    st.number_input("Age", key="age")
    st.form_submit_button("Submit form1", on_click=callback2)
