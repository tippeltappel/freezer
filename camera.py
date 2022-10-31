import streamlit as st



img=st.camera_input("Aufnahme")

if img:
    st.image(img)
    
file = st.file_uploader("Choose a text file")
if file:
    #bytes_data = uploaded_file.read()
    st.write("filename:", file.name)
    #st.write(bytes_data)