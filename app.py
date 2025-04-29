from shapely.geometry import Polygon, LineString
import sys
import os
sys.path.append(os.path.dirname(__file__))

import streamlit as st
import folium
import pandas as pd
import re
from streamlit_folium import st_folium
import logger
logger.log_visit()

from functions.background import set_background
from functions.parse import parse_coordinates
from functions.kml import df_to_kml
from functions.footer import show_footer
from functions.converter import vn2000_to_wgs84_baibao, wgs84_to_vn2000_baibao
from functions.mapgen import generate_map

# Setup page
st.set_page_config(page_title="VN2000 ⇄ WGS84 Converter", layout="wide")
set_background("assets/background.png")

# --- CSS chỉnh màu chữ nút thành đỏ đậm ---
st.markdown("""
<style>
div.stButton > button, div.stDownloadButton > button {
color: #B30000;
font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# Header
col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/logo.jpg", width=90)
with col2:
    st.title("VN2000 ⇄ WGS84 Converter")
    st.markdown("### BẤT ĐỘNG SẢN HUYỆN HƯỚNG HÓA")

# Danh sách kinh tuyến trục
lon0_choices = {
    104.5: "Kiên Giang, Cà Mau",
    104.75: "Lào Cai, Phú Thọ, Nghệ An, An Giang",
    105.0: "Vĩnh Phúc, Hà Nam, Ninh Bình, Thanh Hóa, Đồng Tháp, TP. Cần Thơ, Hậu Giang, Bạc Liêu",
    105.5: "Hà Giang, Bắc Ninh, Hải Dương, Hưng Yên, Nam Định, Thái Bình, Hà Tĩnh, Tây Ninh, Vĩnh Long, Trà Vinh",
    105.75: "TP. Hải Phòng, Bình Dương, Long An, Tiền Giang, Bến Tre, TP. Hồ Chí Minh",
    106.0: "Tuyên Quang, Hòa Bình, Quảng Bình",
    106.25: "Quảng Trị, Bình Phước",
    106.5: "Bắc Kạn, Thái Nguyên",
    107.0: "Bắc Giang, Thừa Thiên – Huế",
    107.25: "Lạng Sơn",
    107.5: "Kon Tum",
    107.75: "TP. Đà Nẵng, Quảng Nam, Đồng Nai, Bà Rịa – Vũng Tàu, Lâm Đồng",
    108.0: "Quảng Ngãi",
    108.25: "Bình Định, Khánh Hòa, Ninh Thuận",
    108.5: "Gia Lai, Đắk Lắk, Đắk Nông, Phú Yên, Bình Thuận"
}

lon0_display = [f"{lon} – {province}" for lon, province in lon0_choices.items()]
default_index = list(lon0_choices.keys()).index(106.25)

# Upload file chung
st.markdown("## 📤 Upload hoặc nhập dữ liệu toạ độ")

uploaded_file = st.file_uploader("Tải file TXT hoặc CSV", type=["txt", "csv"], key="upload_common")

if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    coords_input = st.text_area("Nội dung toạ độ", value=content, height=180, key="coords_input")
else:
    coords_input = st.text_area("Nội dung toạ độ", height=180, key="coords_input")

# Tabs
tab1, tab2 = st.tabs(["VN2000 ➔ WGS84", "WGS84 ➔ VN2000"])

with tab1:
    st.subheader("VN2000 ➔ WGS84")
    selected_display = st.selectbox("Chọn kinh tuyến trục", options=lon0_display, index=default_index, key="lon0_vn2000")
    selected_lon0 = list(lon0_choices.keys())[lon0_display.index(selected_display)]

    if st.button("Chuyển sang WGS84"):
        parsed, errors = parse_coordinates(coords_input)

        if parsed:
            df = pd.DataFrame(
                [(ten_diem, *vn2000_to_wgs84_baibao(x, y, h, selected_lon0)) for ten_diem, x, y, h in parsed],
                columns=["Tên điểm", "Vĩ độ (Lat)", "Kinh độ (Lon)", "H (m)"]
            )
            st.session_state.df = df
            st.session_state.textout = "\n".join(
                f"{row['Tên điểm']} {row['Vĩ độ (Lat)']} {row['Kinh độ (Lon)']} {row['H (m)']}"
                for _, row in df.iterrows()
            )
            st.success(f"✅ Đã xử lý {len(df)} điểm hợp lệ.")
        else:
            st.error("⚠️ Không có dữ liệu hợp lệ!")

        if errors:
            st.error(f"🚨 Có {len(errors)} dòng lỗi:")
            df_errors = pd.DataFrame(errors, columns=["Tên điểm", "X", "Y", "H"])
            st.dataframe(df_errors.style.set_properties(**{'background-color': 'pink'}))

with tab2:
    st.subheader("WGS84 ➔ VN2000")
    selected_display = st.selectbox("Chọn kinh tuyến trục", options=lon0_display, index=default_index, key="lon0_wgs84")
    selected_lon0 = list(lon0_choices.keys())[lon0_display.index(selected_display)]

    if st.button("Chuyển sang VN2000"):
        tokens = re.split(r'[\s\n]+', coords_input.strip())
        coords = []
        i = 0
        while i < len(tokens):
            chunk = []
            for _ in range(3):
                if i < len(tokens):
                    try:
                        chunk.append(float(tokens[i].replace(",", ".")))
                    except:
                        break
                    i += 1
            if len(chunk) == 2:
                chunk.append(0.0)
            if len(chunk) == 3:
                coords.append(chunk)
            else:
                i += 1

        if coords:
            df = pd.DataFrame(
                [("", *wgs84_to_vn2000_baibao(lat, lon, h, selected_lon0)) for lat, lon, h in coords],
                columns=["Tên điểm", "X (m)", "Y (m)", "h (m)"]
            )
            st.session_state.df = df
            st.session_state.textout = "\n".join(
                f"{row['Tên điểm']} {row['X (m)']} {row['Y (m)']} {row['h (m)']}"
                for _, row in df.iterrows()
            )
            st.success(f"Đã xử lý {len(df)} điểm.")
        else:
            st.error("Không có dữ liệu hợp lệ!")

if "df" in st.session_state:
    df = st.session_state.df

    if isinstance(df, pd.DataFrame) and {"Tên điểm", "Vĩ độ (Lat)", "Kinh độ (Lon)"}.issubset(df.columns):
        df_sorted = df.sort_values(by="Tên điểm", ascending=True)

        join_points = st.button("🔵 Nối các điểm thành đường khép kín")

        m = folium.Map(location=[df_sorted.iloc[0]["Vĩ độ (Lat)"], df_sorted.iloc[0]["Kinh độ (Lon)"]], zoom_start=15)

        if join_points:
            points = [(row["Vĩ độ (Lat)"], row["Kinh độ (Lon)"]) for _, row in df_sorted.iterrows()]
            if points[0] != points[-1]:
                points.append(points[0])

            folium.PolyLine(
                locations=points,
                weight=3,
                color="blue",
                tooltip="Polygon khép kín"
            ).add_to(m)

            for lat, lon in points[:-1]:  # Bỏ điểm trùng lặp cuối
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=2,
                    color='black',
                    fill=True,
                    fill_color='black'
                ).add_to(m)

        else:
            for _, row in df_sorted.iterrows():
                folium.Marker(
                    location=[row["Vĩ độ (Lat)"], row["Kinh độ (Lon)"]],
                    popup=row["Tên điểm"],
                    icon=folium.Icon(color="red", icon="info-sign")
                ).add_to(m)

        st.markdown("### 🗺️ Bản đồ các điểm")
        st_folium(m, width="100%", height=600)


show_footer()
