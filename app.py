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

st.markdown(
    """
    <style>
    div.stButton > button, div.stDownloadButton > button {
        color: #B30000;
        font-weight: bold;
    }
    iframe {
        height: 400px !important;
        min-height: 400px !important;
    }
    .css-1aumxhk { width: 100% !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

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
# Longitude zone selector
# =========================
lon0 = select_lon0()

# =========================
# Main layout
# =========================
col_left, col_mid, col_map = st.columns([1, 1, 2])

# =========================
# Input column
# =========================
with col_left:
    st.markdown("## 📄 Upload hoặc nhập toạ độ")
    uploaded_file = st.file_uploader("Tải file TXT hoặc CSV", type=["txt", "csv"])

    content = ""
    if uploaded_file is not None:
        content = uploaded_file.read().decode("utf-8")

    coords_input = st.text_area("Nội dung toạ độ", value=content, height=180)

    st.markdown(
        """
        | STT | Định dạng nhập | Ghi chú |
        |-----|---------------|--------|
        | 1 | `E12345678 N56781234` | EN |
        | 2 | `A01 X Y H` | STT X Y H |
        | 3 | `A01 X Y` | STT X Y |
        | 4 | `X Y` | XY |
        | 5 | `X Y H` | XYH |

        ✅ Phân cách: khoảng trắng, tab, dấu phẩy, xuống dòng
        """,
        unsafe_allow_html=True,
    )

    st.markdown("### 🔄 Chuyển đổi toạ độ")
    tab1, tab2 = st.tabs(["VN2000 ➔ WGS84", "WGS84 ➔ VN2000"])

# =========================
# VN2000 ➜ WGS84
# =========================
with tab1:
    if st.button("➡️ Chuyển sang WGS84"):
        parsed, errors = parse_coordinates(coords_input)
        if parsed:
            df = pd.DataFrame(
                [(ten, *vn2000_to_wgs84_baibao(x, y, h, lon0)) for ten, x, y, h in parsed],
                columns=["STT", "Vĩ độ (Lat)", "Kinh độ (Lon)", "H (m)"],
            )
            df["Tên điểm"] = df["STT"]
            st.session_state.df = df
            st.success(f"✅ Đã xử lý {len(df)} điểm.")
        else:
            st.error("⚠️ Không có dữ liệu hợp lệ!")

# =========================
# WGS84 ➜ VN2000
# =========================
with tab2:
    if st.button("⬅️ Chuyển sang VN2000"):
        tokens = re.split(r"[,\s\n]+", coords_input.strip())
        coords = []
        i = 0
        while i + 1 < len(tokens):
            try:
                lat = float(tokens[i])
                lon = float(tokens[i + 1])
                h = float(tokens[i + 2]) if i + 2 < len(tokens) else 0.0
                coords.append((lat, lon, h))
                i += 3
            except:
                i += 1

        if coords:
            df = pd.DataFrame(
                [(str(i + 1), *wgs84_to_vn2000_baibao(lat, lon, h, lon0))
                 for i, (lat, lon, h) in enumerate(coords)],
                columns=["Tên điểm", "X (m)", "Y (m)", "h (m)"],
            )
            st.session_state.df = df
            st.success(f"✅ Đã xử lý {len(df)} điểm.")
        else:
            st.error("⚠️ Không có dữ liệu hợp lệ!")

# =========================
# Output preview + CAD
# =========================
with col_mid:
    st.markdown("### 📊 Kết quả")
    if "df" in st.session_state:
        df = st.session_state.df
        st.dataframe(df, height=250)

        col_csv, col_kml = st.columns(2)
        with col_csv:
            st.download_button(
                "📀 Tải CSV",
                df.to_csv(index=False).encode("utf-8"),
                "converted_points.csv",
                "text/csv",
            )

        with col_kml:
            kml = df_to_kml(df)
            if kml:
                st.download_button(
                    "📀 Tải KML",
                    kml,
                    "converted_points.kml",
                    "application/vnd.google-earth.kml+xml",
                )

        # ===== Xuất CAD – CHỈ KHI CÓ X/Y =====
        if {"X (m)", "Y (m)"} <= set(df.columns):
            st.markdown("### 🧱 Xuất bản vẽ CAD")
            if st.button("📐 Xuất file CAD (DXF)"):
                tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".dxf")
                pts = [(r["Tên điểm"], r["X (m)"], r["Y (m)"]) for _, r in df.iterrows()]
                export_to_dxf(pts, tmp.name)

                with open(tmp.name, "rb") as f:
                    st.download_button(
                        "⬇️ Tải DXF",
                        f,
                        file_name="toado_vn2000.dxf",
                        mime="application/dxf",
                    )

# =========================
# Map rendering (GIỮ NGUYÊN)
# =========================
with col_map:
    st.markdown("### 🗺️ Bản đồ")
    if "df" in st.session_state and {"Vĩ độ (Lat)", "Kinh độ (Lon)"} <= set(st.session_state.df.columns):
        df_sorted = st.session_state.df.sort_values(
            by="Tên điểm",
            key=lambda c: c.map(sort_point_name),
        )

        map_type = st.selectbox("Chế độ bản đồ", ["Giao Thông", "Vệ tinh"])
        tileset = "OpenStreetMap" if map_type == "Giao Thông" else "Esri.WorldImagery"

        m = folium.Map(
            location=[df_sorted.iloc[0]["Vĩ độ (Lat)"], df_sorted.iloc[0]["Kinh độ (Lon)"]],
            zoom_start=15,
            tiles=tileset,
        )

        if st.session_state.get("join_points", False):
            pts = [(r["Vĩ độ (Lat)"], r["Kinh độ (Lon)"]) for _, r in df_sorted.iterrows()]
            draw_polygon(m, pts)
            add_numbered_markers(m, df_sorted)
        else:
            add_numbered_markers(m, df_sorted)

        st_folium(m, width="100%", height=400)

# =========================
# Footer
# =========================
show_footer()
