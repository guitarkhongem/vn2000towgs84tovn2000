
def render_map(df):
    import pydeck as pdk
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



import streamlit as st
st.set_page_config(page_title="VN2000 ⇄ WGS84 Converter", layout="centered")
import pandas as pd
from functions import vn2000_to_wgs84_baibao, wgs84_to_vn2000_baibao


col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("logo.jpg", width=90)
with col_title:
    st.markdown("<h5 style='margin-bottom:0;'>BẤT ĐỘNG SẢN HUYỆN HƯỚNG HÓA</h5>", unsafe_allow_html=True)
    st.markdown("<h6 style='color:gray;'>VN2000 ⇄ WGS84</h6>", unsafe_allow_html=True)

tab1, tab2 = st.tabs(["➡️ VN2000 → WGS84", "⬅️ WGS84 → VN2000"])

with tab1:
    st.markdown("#### 🔢 Nhập tọa độ VN2000 (X Y Z – cách nhau bởi dấu cách, tab hoặc enter):")
    coords_input = st.text_area("Mỗi dòng một điểm hoặc nhập liên tục", height=200, key="vn2000_input")
    lon0 = st.selectbox("🌐 Chọn kinh tuyến trục (°)", [
        102.75, 103.0, 103.5, 104.0, 104.25, 104.5, 105.0,
        105.25, 105.5, 106.0, 106.25, 106.5, 107.0, 107.25,
        107.5, 108.0, 108.25, 108.5, 109.0, 109.25, 109.5
    ], index=10, key="lon0_vn2000")

    
    if st.button("🔁 Chuyển sang WGS84"):

        parsed = parse_coordinates(coords_input, group=3)
        results = []
        for row in parsed:
            x, y, z = row
            lat, lon, h = vn2000_to_wgs84_baibao(x, y, z, lon0)
            results.append((lat, lon, h))
        if results:
            df = pd.DataFrame(results, columns=["Vĩ độ (Lat)", "Kinh độ (Lon)", "Cao độ ellipsoid (H)"])
            st.session_state.vn2000_df = df
            st.dataframe(df)
        else:
            st.warning("⚠️ Không có dữ liệu hợp lệ hoặc không đủ X Y Z để xử lý.")
        
        st.warning("⚠️ Không có dữ liệu để hiển thị bản đồ.")







import streamlit as st

import pandas as pd

from functions import vn2000_to_wgs84_baibao, wgs84_to_vn2000_baibao

def parse_coordinates(text, group=3):
    lines = text.strip().splitlines()
    coords = []
    for line in lines:
        line = line.strip().replace('\t', ' ')
        parts = [p for p in line.replace(',', '.').split() if p.replace('.', '', 1).replace('-', '', 1).isdigit()]
        if len(parts) >= group:
            try:
                values = list(map(float, parts[:group]))
                coords.append(values)
            except:
                continue
    return coords






col_logo, col_title = st.columns([1, 5])

with col_logo:

    st.image("logo.jpg", width=90)

with col_title:

    st.markdown("<h5 style='margin-bottom:0;'>BẤT ĐỘNG SẢN HUYỆN HƯỚNG HÓA</h5>", unsafe_allow_html=True)

    st.markdown("<h6 style='color:gray;'>VN2000 ⇄ WGS84</h6>", unsafe_allow_html=True)



tab1, tab2 = st.tabs(["➡️ VN2000 → WGS84", "⬅️ WGS84 → VN2000"])



with tab1:

    st.markdown("#### 🔢 Nhập tọa độ VN2000 (X Y Z – cách nhau bởi dấu cách, tab hoặc enter):")

    coords_input = st.text_area("Mỗi dòng một điểm hoặc nhập liên tục", height=200, key="vn2000_input")

    lon0 = st.selectbox("🌐 Chọn kinh tuyến trục (°)", [

        102.75, 103.0, 103.5, 104.0, 104.25, 104.5, 105.0,

        105.25, 105.5, 106.0, 106.25, 106.5, 107.0, 107.25,

        107.5, 108.0, 108.25, 108.5, 109.0, 109.25, 109.5

    ], index=10, key="lon0_vn2000")



    

    if st.button("🔁 Chuyển sang WGS84"):

        parsed = parse_coordinates(coords_input, group=3)
        results = []
        for row in parsed:
            x, y, z = row
            lat, lon, h = vn2000_to_wgs84_baibao(x, y, z, lon0)
            results.append((lat, lon, h))
        if results:
            df = pd.DataFrame(results, columns=["Vĩ độ (Lat)", "Kinh độ (Lon)", "Cao độ ellipsoid (H)"])
            st.session_state.vn2000_df = df
            st.dataframe(df)
        else:
            st.warning("⚠️ Không có dữ liệu hợp lệ hoặc không đủ X Y Z để xử lý.")
        