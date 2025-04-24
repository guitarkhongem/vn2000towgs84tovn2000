import streamlit as st
st.set_page_config(page_title="VN2000 ⇄ WGS84 Converter", layout="centered")

import pandas as pd
import pydeck as pdk
from vn2000_to_wgs84_baibao import vn2000_to_wgs84_baibao, wgs84_to_vn2000_baibao

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

st.title("VN2000 ⇄ WGS84")

tab1, tab2 = st.tabs(["➡️ VN2000 → WGS84", "⬅️ WGS84 → VN2000"])

with tab1:
    st.markdown("#### 🔢 Nhập tọa độ VN2000 (X Y Z – cách nhau bởi dấu cách, tab hoặc enter):")
    coords_input = st.text_area("Mỗi dòng một điểm hoặc nhập liên tục", height=200, key="vn2000_input")
    lon0 = st.selectbox("🌐 Chọn kinh tuyến trục (°)", [106.25, 107.0, 108.0], index=0, key="lon0_vn2000")

    if st.button("🔁 Chuyển sang WGS84"):
        raw_data = coords_input.replace('\t', ' ').replace('\n', ' ')
        numbers = [float(i) for i in raw_data.split() if i.replace('.', '', 1).replace('-', '', 1).isdigit()]
        results = []

        for i in range(0, len(numbers) - 2, 3):
            x, y, z = numbers[i], numbers[i+1], numbers[i+2]
            lat, lon, h = vn2000_to_wgs84_baibao(x, y, z, lon0)
            results.append((lat, lon, h))

        if results:
            df = pd.DataFrame(results, columns=["Vĩ độ (Lat)", "Kinh độ (Lon)", "Cao độ ellipsoid (H)"])
            st.session_state.vn2000_df = df
            st.dataframe(df)
        else:
            st.warning("⚠️ Không có dữ liệu hợp lệ.")

with tab2:
    st.markdown("#### 🔢 Nhập tọa độ WGS84 (Lat Lon H – cách nhau bởi dấu cách, tab hoặc enter):")
    coords_input = st.text_area("Mỗi dòng một điểm hoặc nhập liên tục", height=200, key="wgs84_input")
    lon0 = st.selectbox("🌐 Chọn kinh tuyến trục (°)", [106.25, 107.0, 108.0], index=0, key="lon0_wgs84")

    if st.button("🔁 Chuyển sang VN2000"):
        raw_data = coords_input.replace('\t', ' ').replace('\n', ' ')
        numbers = [float(i) for i in raw_data.split() if i.replace('.', '', 1).replace('-', '', 1).isdigit()]
        results = []

        for i in range(0, len(numbers) - 2, 3):
            lat, lon, h = numbers[i], numbers[i+1], numbers[i+2]
            x, y, h_vn = wgs84_to_vn2000_baibao(lat, lon, h, lon0)
            results.append((x, y, h_vn))

        if results:
            df = pd.DataFrame(results, columns=["x (m)", "y (m)", "Cao độ chuẩn (h)"])
            st.session_state.vn2000_df = df
            st.dataframe(df)
        else:
            st.warning("⚠️ Không có dữ liệu hợp lệ.")

# Bản đồ từ df
if "vn2000_df" in st.session_state:
    render_map(st.session_state.vn2000_df)

# Nguồn bài báo
st.markdown("---")
st.markdown("🔍 **Nguồn công thức**: Bài báo khoa học: **CÔNG TÁC TÍNH CHUYỂN TỌA ĐỘ TRONG CÔNG NGHỆ MÁY BAY KHÔNG NGƯỜI LÁI CÓ ĐỊNH VỊ TÂM CHỤP CHÍNH XÁC**  \n"
            "Tác giả: Trần Trung Anh¹, Quách Mạnh Tuấn²  \n"
            "¹ Trường Đại học Mỏ - Địa chất  \n"
            "² Công ty CP Xây dựng và Thương mại QT Miền Bắc  \n"
            "_Trình bày tại: HỘI NGHỊ KHOA HỌC QUỐC GIA VỀ CÔNG NGHỆ ĐỊA KHÔNG GIAN TRONG KHOA HỌC TRÁI ĐẤT VÀ MÔI TRƯỜNG_")
