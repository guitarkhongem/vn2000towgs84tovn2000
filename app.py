import sys
import os
sys.path.append(os.path.dirname(__file__))

import streamlit as st
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
    st.markdown("### BẤT ĐỘNG SẢN HUYỆN HƯỚng Hóa")

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

# Tabs
tab1, tab2 = st.tabs(["VN2000 ➔ WGS84", "WGS84 ➔ VN2000"])

with tab1:
    st.subheader("VN2000 ➔ WGS84")
    selected_display = st.selectbox("Chọn kinh tuyến trục", options=lon0_display, index=default_index, key="lon0_vn2000")
    selected_lon0 = list(lon0_choices.keys())[lon0_display.index(selected_display)]

    st.markdown("#### Nhập toạ độ VN2000 (X Y H hoặc mã hiệu E/N)")
    coords_input = st.text_area("Mỗi dòng một giá trị", height=180)

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

    st.markdown("#### Nhập toạ độ WGS84 (Lat Lon H)")
    coords_input = st.text_area("Mỗi dòng một giá trị", height=180, key="wgs84input")

    uploaded_file_wgs84 = st.file_uploader("\ud83d\udcc2 Hoặc upload file TXT/CSV", type=["txt", "csv"], key="upload_wgs84")
    if uploaded_file_wgs84:
        try:
            df_uploaded = pd.read_csv(uploaded_file_wgs84, delim_whitespace=True, header=None)
        except:
            df_uploaded = pd.read_csv(uploaded_file_wgs84, header=None)

        coords = []
        for row in df_uploaded.values.tolist():
            if len(row) >= 3:
                try:
                    lat = float(str(row[0]).replace(",", "."))
                    lon = float(str(row[1]).replace(",", "."))
                    h = float(str(row[2]).replace(",", "."))
                    coords.append([lat, lon, h])
                except:
                    continue
            else:
                continue

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
            st.success(f"✅ Đã xử lý {len(df)} điểm từ file.")
        else:
            st.error("⚠️ File không có dòng hợp lệ!")

    elif st.button("Chuyển sang VN2000"):
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
            st.success(f"✅ Đã xử lý {len(df)} điểm.")
        else:
            st.error("⚠️ Không có dữ liệu hợp lệ!")

if "df" in st.session_state:
    df = st.session_state.df
    st.markdown("### Kết quả")
    st.dataframe(df)

    st.markdown("### Kết quả Text")
    st.text_area("Kết quả:", st.session_state.get("textout", ""), height=250)

    st.download_button(
        label="Tải xuống CSV",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="converted_points.csv",
        mime="text/csv"
    )

    kml = df_to_kml(df)
    if kml:
        st.download_button(
            label="Tải xuống KML",
            data=kml,
            file_name="converted_points.kml",
            mime="application/vnd.google-earth.kml+xml"
        )

    if isinstance(df, pd.DataFrame) and {"Vĩ độ (Lat)", "Kinh độ (Lon)"}.issubset(df.columns):
        st.markdown("### Bản đồ vệ tinh")

        st.markdown("""
        <style>
        iframe {
            height: 550px !important;
            min-height: 550px !important;
        }
        </style>
        """, unsafe_allow_html=True)

        m = generate_map(df)
        st_folium(m, width="100%", height=550)

show_footer()
