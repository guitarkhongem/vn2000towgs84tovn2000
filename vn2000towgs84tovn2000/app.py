import streamlit as st
import base64
import pandas as pd
import math
import re
import folium
import analytics
from streamlit_folium import st_folium
from functions import vn2000_to_wgs84_baibao, wgs84_to_vn2000_baibao

def set_background(png_file):
    with open(png_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{encoded_string}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        .stTextArea textarea {{
            background-color: rgba(0, 0, 0, 0.25) !important;
            color: white !important;
        }}
        .stTextInput > div > div > input {{
            background-color: rgba(0, 0, 0, 0.25) !important;
            color: white !important;
        }}
        .stButton>button {{
            background-color: #1a73e8;
            color: white;
        }}
        .markdown-text-container, .stMarkdown p {{
            color: white !important;
        }}
        .leaflet-container {{
            width: 100% !important;
            height: 600px !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

st.set_page_config(page_title="VN2000 ⇄ WGS84 Converter", layout="wide")
set_background("background.png")

col1, col2 = st.columns([1, 5], gap="small")
with col1:
    st.image("logo.jpg", width=80)
with col2:
    st.title("VN2000 ⇄ WGS84 Converter")
    st.markdown("### BẤT ĐỘNG SẢN HUYỆN HƯỚNG HÓA")

def parse_coordinates(text, group=3):
    tokens = re.split(r'\s+', text.strip())
    coords = []
    i = 0
    while i + group <= len(tokens):
        t0 = tokens[i]
        if (re.search(r'[A-Za-z]', t0) or ('.' not in t0 and re.fullmatch(r'\d+', t0) and len(tokens) - i >= group + 1)):
            i += 1
            continue
        chunk = tokens[i: i+group]
        try:
            vals = [float(x.replace(',', '.')) for x in chunk]
            coords.append(vals)
            i += group
        except ValueError:
            i += 1
    return coords

def df_to_kml(df):
    if not {"Kinh độ (Lon)", "Vĩ độ (Lat)", "H (m)"}.issubset(df.columns):
        return None
    kml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<kml xmlns="http://www.opengis.net/kml/2.2">',
        '  <Document>',
        '    <name>Computed Points (WGS84)</name>'
    ]
    for idx, row in df.iterrows():
        kml += [
            '    <Placemark>',
            f'      <name>Point {idx+1}</name>',
            '      <Point>',
            f'        <coordinates>{row["Kinh độ (Lon)"]},{row["Vĩ độ (Lat)"]},{row["H (m)"]}</coordinates>',
            '      </Point>',
            '    </Placemark>'
        ]
    kml += ['  </Document>', '</kml>']
    return "\n".join(kml)

tab1, tab2 = st.tabs(["➡️ VN2000 → WGS84", "⬅️ WGS84 → VN2000"])

with tab1:
    st.markdown("#### 🔢 Nhập tọa độ VN2000 (X Y Z – space/tab/newline hoặc kèm STT):")
    in_vn = st.text_area("", height=120, key="vn_in")
    lon0_vn = st.number_input("🌐 Kinh tuyến trục (°)", value=106.25, format="%.4f", key="lon0_vn")
    if st.button("🔁 Chuyển WGS84"):
        parsed = parse_coordinates(in_vn, group=3)
        results = [vn2000_to_wgs84_baibao(x, y, z, lon0_vn) for x, y, z in parsed]
        if results:
            df = pd.DataFrame(results, columns=["Vĩ độ (Lat)", "Kinh độ (Lon)", "H (m)"])
            st.session_state.df = df
        else:
            st.warning("⚠️ Không có dữ liệu hợp lệ (cần 3 số mỗi bộ).")

with tab2:
    st.markdown("#### 🔢 Nhập tọa độ WGS84 (Lat Lon H – space/tab/newline hoặc kèm STT):")
    in_wg = st.text_area("", height=120, key="wg_in")
    lon0_wg = st.number_input("🌐 Kinh tuyến trục (°)", value=106.25, format="%.4f", key="lon0_wg")
    if st.button("🔁 Chuyển VN2000"):
        parsed = parse_coordinates(in_wg, group=3)
        results = [wgs84_to_vn2000_baibao(lat, lon, h, lon0_wg) for lat, lon, h in parsed]
        if results:
            df = pd.DataFrame(results, columns=["X (m)", "Y (m)", "h (m)"])
            st.session_state.df = df
        else:
            st.warning("⚠️ Không có dữ liệu hợp lệ (cần 3 số mỗi bộ).")

if "df" in st.session_state:
    df = st.session_state.df
    st.markdown("### 📊 Kết quả chuyển đổi")
    st.dataframe(df)

    if {"Vĩ độ (Lat)", "Kinh độ (Lon)"}.issubset(df.columns):
        kml_str = df_to_kml(df)
        if kml_str:
            st.markdown("### 📥 Xuất file KML tọa độ tính được (WGS84)")
            st.download_button("Tải xuống KML", kml_str, "computed_points.kml", "application/vnd.google-earth.kml+xml")

        st.markdown("### 🛰️ Bản đồ vệ tinh với các điểm tọa độ")
        center_lat = df["Vĩ độ (Lat)"].mean()
        center_lon = df["Kinh độ (Lon)"].mean()
        m = folium.Map(
            location=[center_lat, center_lon],
            zoom_start=15,
            tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
            attr="Esri.WorldImagery"
        )
        for _, row in df.iterrows():
            folium.CircleMarker(
                location=(row["Vĩ độ (Lat)"], row["Kinh độ (Lon)"]),
                radius=3,
                color="red",
                fill=True,
                fill_opacity=0.8
            ).add_to(m)
        st_folium(m, width=1200, height=600)

st.markdown("---")
st.markdown("📌 Tác giả: Trần Trường Sinh  
📞 Số điện thoại: 0917.750.555")
st.markdown("🔍 **Nguồn công thức**: Bài báo khoa học: **CÔNG TÁC TÍNH CHUYỂN TỌA ĐỘ TRONG CÔNG NGHỆ MÁY BAY KHÔNG NGƯỜI LÁI CÓ ĐỊNH VỊ TÂM CHỤP CHÍNH XÁC**  
Tác giả: Trần Trung Anh¹, Quách Mạnh Tuấn²  
¹ Trường Đại học Mỏ - Địa chất  
² Công ty CP Xây dựng và Thương mại QT Miền Bắc  
_Hội nghị Khoa học Quốc gia Về Công nghệ Địa không gian, 2021_")