import sys
import os
sys.path.append(os.path.dirname(__file__))

import streamlit as st
import pandas as pd
import re
import folium
from streamlit_folium import st_folium
from shapely.geometry import Polygon, LineString
import logger
logger.log_visit()

from functions.background import set_background
from functions.parse import parse_coordinates
from functions.kml import df_to_kml
from functions.footer import show_footer
from functions.converter import vn2000_to_wgs84_baibao, wgs84_to_vn2000_baibao

st.set_page_config(page_title="VN2000 ⇄ WGS84 Converter", layout="wide")
set_background("assets/background.png")

st.markdown("""
<style>
div.stButton > button, div.stDownloadButton > button {
color: #B30000;
font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/logo.jpg", width=90)
with col2:
    st.title("VN2000 ⇄ WGS84 Converter")
    st.markdown("### BẤT ĐỘNG SẢN HUYỆN HƯỚNG HÓA")

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

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("## 📄 Upload hoặc nhập toạ độ")
    uploaded_file = st.file_uploader("Tải file TXT hoặc CSV", type=["txt", "csv"], key="upload_common")

    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")
        coords_input = st.text_area("Nội dung toạ độ", value=content, height=180, key="coords_input")
    else:
        coords_input = st.text_area("Nội dung toạ độ", height=180, key="coords_input")

    selected_display = st.selectbox("🧭 Chọn kinh tuyến trục", options=lon0_display, index=default_index)
st.markdown("### 🔄 Chuyển đổi toạ độ")

tab1, tab2 = st.tabs(["VN2000 ➔ WGS84", "WGS84 ➔ VN2000"])

with tab1:
    if st.button("➡️ Chuyển sang WGS84"):
        parsed, errors = parse_coordinates(coords_input)

        if parsed:
            df = pd.DataFrame(
                [(ten_diem, *vn2000_to_wgs84_baibao(x, y, h, float(selected_display.split('–')[0].strip()))) for ten_diem, x, y, h in parsed],
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

with tab2:
    if st.button("⬅️ Chuyển sang VN2000"):
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
                [("", *wgs84_to_vn2000_baibao(lat, lon, h, float(selected_display.split('–')[0].strip()))) for lat, lon, h in coords],
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

with col2:
    st.markdown("### 📊 Kết quả")
    if "df" in st.session_state:
        df = st.session_state.df
        st.dataframe(df)
        st.text_area("📄 Text kết quả", st.session_state.get("textout", ""), height=250)

        col_csv, col_kml, col_maptype, col_join = st.columns(4)
        with col_csv:
            st.download_button(
                label="💾 Tải CSV",
                data=df.to_csv(index=False).encode("utf-8"),
                file_name="converted_points.csv",
                mime="text/csv"
            )
        with col_kml:
            kml = df_to_kml(df)
            if kml:
                st.download_button(
                    label="💾 Tải KML",
                    data=kml,
                    file_name="converted_points.kml",
                    mime="application/vnd.google-earth.kml+xml"
                )
        with col_maptype:
            map_type = st.selectbox(options=["Giao Thông", "Vệ tinh"], index=0, key="map_type")
        with col_join:
            if "join_points" not in st.session_state:
                st.session_state.join_points = False
            if st.button("🔵 Nối điểm"):
                st.session_state.join_points = not st.session_state.join_points

        st.markdown("---")
        st.markdown("### 🗺️ Bản đồ")

        tileset = "OpenStreetMap" if st.session_state.get("map_type", "Giao Thông") == "Giao Thông" else "Esri.WorldImagery"

        df_sorted = df.sort_values(by="Tên điểm", ascending=True)
        m = folium.Map(location=[df_sorted.iloc[0]["Vĩ độ (Lat)"], df_sorted.iloc[0]["Kinh độ (Lon)"]], zoom_start=15, tiles=tileset)

        if st.session_state.join_points:
            points = [(row["Vĩ độ (Lat)"], row["Kinh độ (Lon)"]) for _, row in df_sorted.iterrows()]
            if points[0] != points[-1]:
                points.append(points[0])

            folium.PolyLine(
                locations=points,
                weight=3,
                color="blue",
                tooltip="Polygon khép kín"
            ).add_to(m)

            for lat, lon in points[:-1]:
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=2,
                    color='black',
                    fill=True,
                    fill_color='black'
                ).add_to(m)
        else:
            for _, row in df_sorted.iterrows():
                folium.CircleMarker(
                    location=[row["Vĩ độ (Lat)"], row["Kinh độ (Lon)"]],
                    radius=6,
                    color='red',
                    fill=True,
                    fill_color='red'
                ).add_to(m)

        st_folium(m, width="100%", height=750)


show_footer()