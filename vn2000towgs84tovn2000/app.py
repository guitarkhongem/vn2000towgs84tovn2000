
import streamlit as st
st.set_page_config(page_title="VN2000 ⇄ WGS84 Converter", layout="centered")

import pandas as pd
import pydeck as pdk
from functions import vn2000_to_wgs84_baibao, wgs84_to_vn2000_baibao
import math

def parse_coordinates(text, group=3):
    tokens = text.replace('\t', ' ').replace('\n', ' ').split()
    coords = []
    i = 0
    while i + group <= len(tokens):
        chunk = tokens[i:i+group]
        try:
            vals = list(map(float, chunk))
            coords.append(vals)
            i += group
        except ValueError:
            i += 1
    return coords

def render_map(df):
    if not df.empty and "Vĩ độ (Lat)" in df.columns and "Kinh độ (Lon)" in df.columns:
        deck = pdk.Deck(
            map_style="mapbox://styles/mapbox/streets-v12",
            initial_view_state=pdk.ViewState(
                latitude=df["Vĩ độ (Lat)"].mean(),
                longitude=df["Kinh độ (Lon)"].mean(),
                zoom=14,
                pitch=0,
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=df,
                    get_position="[Kinh độ (Lon), Vĩ độ (Lat)]",
                    get_color="[255, 0, 0, 160]",
                    get_radius=1,
                    radius_min_pixels=1,
                    radius_max_pixels=2,
                    pickable=False
                )
            ],
        )
        st.pydeck_chart(deck)
    else:
        st.warning("⚠️ Không có dữ liệu để hiển thị bản đồ.")

st.title("VN2000 ⇄ WGS84 Converter")

tab1, tab2 = st.tabs(["➡️ VN2000 → WGS84", "⬅️ WGS84 → VN2000"])

with tab1:
    st.markdown("#### 🔢 Nhập tọa độ VN2000 (X Y Z – cách nhau dấu cách, tab hoặc enter):")
    coords_input = st.text_area("Mỗi dòng một điểm hoặc nhập liên tục", height=200, key="vn2000_input")
    lon0 = st.number_input("🌐 Kinh tuyến trục (°)", value=106.25, format="%.4f", key="lon0_vn2000")

    if st.button("🔁 Chuyển sang WGS84"):
        parsed = parse_coordinates(coords_input, group=3)
        results = []
        for x, y, z in parsed:
            lat, lon, h = vn2000_to_wgs84_baibao(x, y, z, lon0)
            results.append((lat, lon, h))
        if results:
            df = pd.DataFrame(results, columns=["Vĩ độ (Lat)", "Kinh độ (Lon)", "Cao độ ellipsoid (H)"])
            st.session_state.vn2000_df = df
            st.dataframe(df)
        else:
            st.warning("⚠️ Không có dữ liệu hợp lệ hoặc không đủ X Y Z để xử lý.")

with tab2:
    st.markdown("#### 🔢 Nhập tọa độ WGS84 (Lat Lon H – cách nhau dấu cách, tab hoặc enter):")
    coords_input = st.text_area("Mỗi dòng một điểm hoặc nhập liên tục", height=200, key="wgs84_input")
    lon0 = st.number_input("🌐 Kinh tuyến trục (°)", value=106.25, format="%.4f", key="lon0_wgs84")

    if st.button("🔁 Chuyển sang VN2000"):
        parsed = parse_coordinates(coords_input, group=3)
        results = []
        for lat, lon, h in parsed:
            x, y, h_vn = wgs84_to_vn2000_baibao(lat, lon, h, lon0)
            results.append((x, y, h_vn))
        if results:
            df = pd.DataFrame(results, columns=["x (m)", "y (m)", "Cao độ chuẩn (h)"])
            st.session_state.vn2000_df = df
            st.dataframe(df)
        else:
            st.warning("⚠️ Không có dữ liệu hợp lệ hoặc không đủ Lat Lon H để xử lý.")

if "vn2000_df" in st.session_state:
    render_map(st.session_state.vn2000_df)

st.markdown("---")
st.markdown("🔍 **Nguồn công thức**: Bài báo khoa học: **CÔNG TÁC TÍNH CHUYỂN TỌA ĐỘ TRONG CÔNG NGHỆ MÁY BAY KHÔNG NGƯỜI LÁI CÓ ĐỊNH VỊ TÂM CHỤP CHÍNH XÁC**  ")
st.markdown("Tác giả: Trần Trung Anh¹, Quách Mạnh Tuấn²")
st.markdown("¹ Trường Đại học Mỏ - Địa chất")
st.markdown("² Công ty CP Xây dựng và Thương mại QT Miền Bắc")
st.markdown("_Trình bày tại: HỘI NGHỊ KHOA HỌC QUỐC GIA VỀ CÔNG NGHỆ ĐỊA KHÔNG GIAN TRONG KHOA HỌC TRÁI ĐẤT VÀ MÔI TRƯỜNG_")
