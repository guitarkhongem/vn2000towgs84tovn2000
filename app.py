import os
import re
import tempfile

import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
from PIL import Image

# --- Custom functions ---
from functions.background import set_background
from functions.parse import parse_coordinates
from functions.kml import df_to_kml
from functions.footer import show_footer
from functions.converter import vn2000_to_wgs84_baibao, wgs84_to_vn2000_baibao
from functions.edges import add_edge_lengths
from functions.markers import add_numbered_markers
from functions.polygon import draw_polygon
from functions.area import compare_areas
from functions.lon0_selector import select_lon0
from functions.sort_utils import sort_point_name
from functions.EdgeLengths import compute_edge_lengths
from functions.export_dxf import export_to_dxf

# =========================
# Page setup
# =========================
st.set_page_config(page_title="VN2000 ⇄ WGS84 Converter", layout="wide")
set_background("assets/background.png")

st.markdown("""
<style>
div.stButton > button, div.stDownloadButton > button {
    color: #B30000;
    font-weight: bold;
}
iframe {
    height: 400px !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# Header
# =========================
col1, col2 = st.columns([1, 5])
with col1:
    st.image("assets/logo.jpg", width=90)
with col2:
    st.title("VN2000 ⇄ WGS84 Converter")
    st.markdown("### BẤT ĐỘNG SẢN HUYỆN HƯỚNG HÓA")

# =========================
# Longitude selector
# =========================
lon0 = select_lon0()

# =========================
# Layout
# =========================
col_left, col_mid, col_map = st.columns([1, 1, 2])

# =========================
# Input
# =========================
with col_left:
    uploaded_file = st.file_uploader("📄 Upload TXT / CSV", ["txt", "csv"])
    content = uploaded_file.read().decode("utf-8") if uploaded_file else ""
    coords_input = st.text_area("Toạ độ", content, height=180)

    st.markdown("### 🔄 Chuyển đổi")
    tab1, tab2 = st.tabs(["VN2000 ➜ WGS84", "WGS84 ➜ VN2000"])

# =========================
# VN2000 ➜ WGS84
# =========================
with tab1:
    if st.button("➡️ Chuyển sang WGS84"):
        parsed, _ = parse_coordinates(coords_input)
        if parsed:
            df = pd.DataFrame(
                [(t, *vn2000_to_wgs84_baibao(x, y, h, lon0)) for t, x, y, h in parsed],
                columns=["Tên điểm", "Vĩ độ (Lat)", "Kinh độ (Lon)", "H (m)"]
            )
            st.session_state.df = df
        else:
            st.error("Không có dữ liệu hợp lệ")

# =========================
# WGS84 ➜ VN2000
# =========================
with tab2:
    if st.button("⬅️ Chuyển sang VN2000"):
        tokens = re.split(r"[,\s\n]+", coords_input.strip())
        pts = []
        i = 0
        while i + 1 < len(tokens):
            try:
                lat, lon = float(tokens[i]), float(tokens[i+1])
                h = float(tokens[i+2]) if i+2 < len(tokens) else 0
                pts.append((lat, lon, h))
                i += 3
            except:
                i += 1

        if pts:
            df = pd.DataFrame(
                [(str(i+1), *wgs84_to_vn2000_baibao(lat, lon, h, lon0))
                 for i, (lat, lon, h) in enumerate(pts)],
                columns=["Tên điểm", "X (m)", "Y (m)", "H (m)"]
            )
            st.session_state.df = df

# =========================
# Output + CAD
# =========================
with col_mid:
    if "df" in st.session_state:
        df = st.session_state.df
        st.dataframe(df)

        st.download_button("📀 CSV", df.to_csv(index=False), "points.csv")

        kml = df_to_kml(df)
        if kml:
            st.download_button("🌍 KML", kml, "points.kml")

        st.markdown("### 🧱 Xuất CAD (DXF)")
        if st.button("📐 Xuất DXF"):
            pts = []

            if {"X (m)", "Y (m)"} <= set(df.columns):
                pts = [(r["Tên điểm"], r["X (m)"], r["Y (m)"]) for _, r in df.iterrows()]
            else:
                parsed, _ = parse_coordinates(coords_input)
                pts = [(t, x, y) for t, x, y, _ in parsed]

            if pts:
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".dxf")
                export_to_dxf(pts, tmp.name)
                st.download_button("⬇️ Tải DXF", open(tmp.name, "rb"), "toado_vn2000.dxf")

# =========================
# Map
# =========================
with col_map:
    if "df" in st.session_state and {"Vĩ độ (Lat)", "Kinh độ (Lon)"} <= set(st.session_state.df.columns):
        dfm = st.session_state.df.sort_values(
            "Tên điểm", key=lambda c: c.map(sort_point_name)
        )

        col_btn1, col_btn2, col_btn3 = st.columns(3)

        with col_btn1:
            if st.button("🔵 Nối điểm"):
                st.session_state.join_points = not st.session_state.get("join_points", False)

        with col_btn2:
            if st.button("📐 Tính diện tích"):
                parsed, _ = parse_coordinates(coords_input)
                if parsed:
                    xy = [(x, y) for _, x, y, _ in parsed]
                    latlon = [(r["Vĩ độ (Lat)"], r["Kinh độ (Lon)"]) for _, r in dfm.iterrows()]
                    A1, A2, _, ha1, ha2 = compare_areas(xy, latlon)
                    st.info(f"VN2000: {ha1:.2f} ha | WGS84: {ha2:.2f} ha")

        with col_btn3:
            if st.button("📏 Hiện cạnh"):
                st.session_state.show_lengths = not st.session_state.get("show_lengths", False)

        m = folium.Map(
            location=[dfm.iloc[0]["Vĩ độ (Lat)"], dfm.iloc[0]["Kinh độ (Lon)"]],
            zoom_start=15
        )

        pts = [(r["Vĩ độ (Lat)"], r["Kinh độ (Lon)"]) for _, r in dfm.iterrows()]
        if st.session_state.get("join_points", False):
            draw_polygon(m, pts)
            if st.session_state.get("show_lengths", False):
                add_edge_lengths(m, pts)

        add_numbered_markers(m, dfm)
        st_folium(m, width="100%", height=400)

# =========================
# Footer
# =========================
show_footer()
