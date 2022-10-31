import streamlit as st


img = st.camera_input("Aufnahme")

if img:
    st.image(img)
    img_name = "data/media/" + "img1"
    with open(img_name, "w") as f:
        f.write(img)
"""
file = st.file_uploader("Choose a text file")
if file:
    #bytes_data = uploaded_file.read()
    st.write("filename:", file.name)
    # st.write(bytes_data)
    file_name = "data/media/" + file.name
    with open(file_name, "w") as f:
        f.write("Woops! I have deleted the content!")
"""
