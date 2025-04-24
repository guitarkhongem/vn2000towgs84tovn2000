import streamlit as st
st.set_page_config(page_title="VN2000 ⇄ WGS84 Converter", layout="centered")

import pandas as pd
import math
from functions import vn2000_to_wgs84_baibao, wgs84_to_vn2000_baibao

# Thư viện Folium
import folium
from streamlit_folium import st_folium

def parse_coordinates(text, group=3):
    """
    Chia token space/tab/newline thành groups of `group` float.
    Hỗ trợ cả nhập STT đầu dòng sẽ bị bỏ qua.
    """
    # Thay thế tab và newline thành khoảng trắng rồi tách tokens
    tokens = text.replace('\t', ' ').replace('\n', ' ').split()
    coords = []
    i = 0
    # Lặp qua tokens theo từng nhóm `group`
    while i + group <= len(tokens):
        chunk = tokens[i:i+group]
        try:
            # Nếu cả chunk đều có thể float được => thêm vào kết quả
            vals = list(map(float, chunk))
            coords.append(vals)
            i += group
        except ValueError:
            # Nếu chunk không hợp lệ, bỏ qua token đầu và thử lại
            i += 1
    return coords

def render_map(df):
    """Hiển thị các điểm lên bản đồ vệ tinh Folium."""
    if df is None or df.empty:
        st.warning("⚠️ Không có dữ liệu để hiển thị bản đồ.")
        return

    # Đổi cột cho Folium
    lat_col = "Vĩ độ (Lat)" if "Vĩ độ (Lat)" in df.columns else "latitude"
    lon_col = "Kinh độ (Lon)" if "Kinh độ (Lon)" in df.columns else "longitude"
    df_map = df.rename(columns={lat_col: "latitude", lon_col: "longitude"})

    # Tọa độ trung tâm
    center_lat = float(df_map["latitude"].mean())
    center_lon = float(df_map["longitude"].mean())

    # Tạo bản đồ vệ tinh Esri
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=14,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri.WorldImagery"
    )

    # Vẽ mỗi điểm dưới dạng CircleMarker nhỏ
    for idx, row in df_map.iterrows():
        folium.CircleMarker(
            location=(row["latitude"], row["longitude"]),
            radius=3,         # 3 pixel giống vị trí GPS
            color="red",
            fill=True,
            fill_opacity=0.8,
        ).add_to(m)

    # Hiển thị trong Streamlit
    st_folium(m, width=700, height=500)


st.title("VN2000 ⇄ WGS84 Converter")

tab1, tab2 = st.tabs(["➡️ VN2000 → WGS84", "⬅️ WGS84 → VN2000"])

with tab1:
    st.markdown("#### 🔢 Nhập tọa độ VN2000 (X Y Z – space/tab/newline):")
    coords_input = st.text_area("", height=150, key="vn_in")
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
    coords_input = st.text_area("", height=150, key="wg_in")
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

# Nếu có DataFrame, vẽ bản đồ
if "df" in st.session_state:
    render_map(st.session_state.df)

st.markdown("---")
st.markdown(
    "Tác giả: Trần Trường Sinh  \n"
    "Số điện thoại: 0917.750.555  \n"
)
st.markdown("---")
st.markdown(
    "🔍 **Nguồn công thức**: Bài báo khoa học: **CÔNG TÁC TÍNH CHUYỂN TỌA ĐỘ TRONG CÔNG NGHỆ MÁY BAY KHÔNG NGƯỜI LÁI...**  \n"
    "Tác giả: Trần Trung Anh¹, Quách Mạnh Tuấn²  \n"
    "¹ Trường Đại học Mỏ - Địa chất  \n"
    "² Công ty CP Xây dựng và Thương mại QT Miền Bắc  \n"
    "_Hội nghị Quốc Gia Về Công Nghệ Địa Không Gian, 2021_"
)
