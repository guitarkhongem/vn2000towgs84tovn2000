
import streamlit as st
from functions import vn2000_to_wgs84_baibao, wgs84_to_vn2000_baibao

st.set_page_config(page_title="VN2000 ⇄ WGS84 Converter", layout="centered")
st.title("VN2000 ⇄ WGS84")

tab1, tab2 = st.tabs(["➡️ VN2000 → WGS84", "⬅️ WGS84 → VN2000"])

with tab1:
    st.subheader("VN2000 ➜ WGS84")
    col1, col2 = st.columns(2)
    with col1:
        x = st.number_input("🧮 X (m)", value=1855759.3584, format="%.10f", key="x_vn")
        z = st.number_input("📏 Z", value=846.1115, format="%.4f", key="z_vn")
    with col2:
        y = st.number_input("🧮 Y (m)", value=546151.8072, format="%.10f", key="y_vn")
        lon0 = st.number_input("🌐 Kinh tuyến trục (°)", value=106.25, key="lon0_vn")

    if st.button("🔄 Chuyển sang WGS84", key="btn1"):
        lat, lon, h = vn2000_to_wgs84_baibao(x, y, z, lon0)
        st.success("🎯 Kết quả WGS84:")
        st.markdown(f"**Kinh độ (Lon):** `{lon:.15f}`")
        st.markdown(f"**Vĩ độ (Lat):** `{lat:.15f}`")
        st.markdown(f"**Cao độ elipsoid (H):** `{h:.7f}` m")

with tab2:
    st.subheader("WGS84 ➜ VN2000")
    col1, col2 = st.columns(2)
    with col1:
        lat = st.number_input("🌎 Vĩ độ (Lat)", value=16.77839876, format="%.10f", key="lat_wgs")
        h = st.number_input("📏 Cao độ elipsoid (H)", value=832.2537253, format="%.7f", key="h_wgs")
    with col2:
        lon = st.number_input("🌍 Kinh độ (Lon)", value=106.68477742, format="%.10f", key="lon_wgs")
        lon0 = st.number_input("🌐 Kinh tuyến trục (°)", value=106.25, key="lon0_wgs")

    if st.button("🔄 Chuyển sang VN2000", key="btn2"):
        x, y, h_vn = wgs84_to_vn2000_baibao(lat, lon, h, lon0)
        st.success("🎯 Kết quả VN2000:")
        st.markdown(f"**x:** `{x:.4f}` m")
        st.markdown(f"**y:** `{y:.4f}` m")
        st.markdown(f"**Cao độ chuẩn (h):** `{h_vn:.4f}` m")

