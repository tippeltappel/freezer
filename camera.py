import streamlit as st
from PIL import Image

img = st.camera_input("Aufnahme")
if img:
    img1 = Image.open(img)
    st.write("image format : " + img1.format)
    st.write("image size W x H : " +
             str(img1.size[0]) + " x " + str(img1.size[1]))
    st.write("image mode : " + img1.mode)

    img1.save("data/media/img2.jpg")

    img2 = Image.open("data/media/img2.jpg")
    st.image(img2)
    st.write("image format : " + img2.format)
    st.write("image size W x H : " +
             str(img2.size[0]) + " x " + str(img2.size[1]))
    st.write("image mode : " + img2.mode)
    img2.thumbnail((128, 128))
    st.image(img2)


"""
if img:
    st.image(img)
    img_name = "data/media/" + "img1"
    with open(img_name, "w") as f:
        f.write(img)

file = st.file_uploader("Choose a text file")
if file:
    #bytes_data = uploaded_file.read()
    st.write("filename:", file.name)
    # st.write(bytes_data)
    file_name = "data/media/" + file.name
    with open(file_name, "w") as f:
        f.write("Woops! I have deleted the content!")
"""
