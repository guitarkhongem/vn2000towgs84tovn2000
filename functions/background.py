import base64
import streamlit as st

def set_background(png_file):
    with open(png_file, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    page_bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{b64}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)
