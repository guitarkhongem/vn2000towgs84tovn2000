import streamlit as st
st.set_page_config(page_title="VN2000 ⇄ WGS84 Converter", layout="centered")

import pandas as pd
from functions import vn2000_to_wgs84_baibao, wgs84_to_vn2000_baibao

def parse_coordinates(text, group=3):
    """Chia token space/tab/newline thành các nhóm số float size=group."""
    tokens = text.replace('\t',' ').replace('\n',' ').split()
    coords, i = [], 0
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
    """Hiển thị DataFrame có 2 cột latitude/longitude lên bản đồ Streamlit."""
    if not df.empty and "Vĩ độ (Lat)" in df.columns and "Kinh độ (Lon)" in df.columns:
        df_map = df.rename(columns={"Vĩ độ (Lat)": "latitude", "Kinh độ (Lon)": "longitude"})
        st.map(df_map)
    else:
        st.warning("⚠️ Không có dữ liệu để hiển thị bản đồ.")

st.title("VN2000 ⇄ WGS84 Converter")

tab1, tab2 = st.tabs(["➡️ VN2000 → WGS84", "⬅️ WGS84 → VN2000"])

with tab1:
    st.markdown("#### 🔢 Nhập tọa độ VN2000 (X Y Z – space/tab/newline):")
    coords_input = st.text_area("", height=150, key="vn2000_in")
    lon0 = st.number_input("🌐 Kinh tuyến trục (°)", value=106.25, format="%.4f", key="lon0_vn")
    if st.button("🔁 Chuyển WGS84"):
        parsed = parse_coordinates(coords_input, group=3)
        results = []
        for x, y, z in parsed:
            lat, lon, h = vn2000_to_wgs84_baibao(x, y, z, lon0)
            results.append((lat, lon, h))
        if results:
            df = pd.DataFrame(results, columns=["Vĩ độ (Lat)", "Kinh độ (Lon)", "H (m)"])
            st.session_state.df = df
            st.dataframe(df)
        else:
            st.warning("⚠️ Không có dữ liệu hợp lệ (cần 3 số mỗi bộ).")

with tab2:
    st.markdown("#### 🔢 Nhập tọa độ WGS84 (Lat Lon H – space/tab/newline):")
    coords_input = st.text_area("", height=150, key="wgs84_in")
    lon0 = st.number_input("🌐 Kinh tuyến trục (°)", value=106.25, format="%.4f", key="lon0_wg")
    if st.button("🔁 Chuyển VN2000"):
        parsed = parse_coordinates(coords_input, group=3)
        results = []
        for lat, lon, h in parsed:
            x, y, h_vn = wgs84_to_vn2000_baibao(lat, lon, h, lon0)
            results.append((x, y, h_vn))
        if results:
            df = pd.DataFrame(results, columns=["X (m)", "Y (m)", "h (m)"])
            st.session_state.df = df
            st.dataframe(df)
        else:
            st.warning("⚠️ Không có dữ liệu hợp lệ (cần 3 số mỗi bộ).")

if "df" in st.session_state:
    render_map(st.session_state.df)

st.markdown("---")
st.markdown(
    "🔍 **Nguồn công thức**: Bài báo khoa học: **CÔNG TÁC TÍNH CHUYỂN TỌA ĐỘ TRONG CÔNG NGHỆ MÁY BAY KHÔNG NGƯỜI LÁI CÓ ĐỊNH VỊ TÂM CHỤP CHÍNH XÁC**  \n"
    "Tác giả: Trần Trung Anh¹, Quách Mạnh Tuấn²  \n"
    "¹ Trường Đại học Mỏ - Địa chất  \n"
    "² Công ty CP Xây dựng và Thương mại QT Miền Bắc  \n"
    "_Hội nghị Quốc Gia Về Công Nghệ Địa Không Gian, 2021_"
)
