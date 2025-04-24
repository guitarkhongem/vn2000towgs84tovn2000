
import streamlit as st
from vn2000_to_wgs84_baibao import vn2000_to_wgs84_baibao
from wgs84_to_vn2000_baibao import wgs84_to_vn2000_baibao

st.set_page_config(page_title="VN2000 ⇄ WGS84 Converter", layout="centered")

st.title("📍 Chuyển đổi tọa độ VN2000 ⇄ WGS84")
st.markdown("### Công cụ chuyển đổi tọa độ dựa trên thuật toán bài báo khoa học")

tab1, tab2 = st.tabs(["➡️ VN2000 → WGS84", "⬅️ WGS84 → VN2000"])

with tab1:
    st.subheader("VN2000 ➜ WGS84")
    col1, col2 = st.columns(2)
    with col1:
        x = st.number_input("🧮 Hoành độ x (m)", value=1855759.3584, format="%.10f")
        z = st.number_input("📏 Cao độ (m)", value=846.1115, format="%.4f")
    with col2:
        y = st.number_input("🧮 Tung độ y (m)", value=546151.8072, format="%.10f")
        lon0 = st.number_input("🌐 Kinh tuyến trục (°)", value=106.25)

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
        lat = st.number_input("🌎 Vĩ độ (Lat)", value=16.77839876, format="%.10f")
        h = st.number_input("📏 Cao độ elipsoid (H)", value=832.2537253, format="%.7f")
    with col2:
        lon = st.number_input("🌍 Kinh độ (Lon)", value=106.68477742, format="%.10f")
        lon0 = st.number_input("🌐 Kinh tuyến trục (°)", value=106.25)

    if st.button("🔄 Chuyển sang VN2000", key="btn2"):
        x, y, h_vn = wgs84_to_vn2000_baibao(lat, lon, h, lon0)
        st.success("🎯 Kết quả VN2000:")
        st.markdown(f"**x:** `{x:.4f}` m")
        st.markdown(f"**y:** `{y:.4f}` m")
        st.markdown(f"**Cao độ chuẩn (h):** `{h_vn:.4f}` m")

st.markdown("---")
st.markdown("🔍 **Nguồn công thức**: Bài báo khoa học: **CÔNG TÁC TÍNH CHUYỂN TỌA ĐỘ TRONG CÔNG NGHỆ MÁY BAY KHÔNG NGƯỜI LÁI CÓ ĐỊNH VỊ TÂM CHỤP CHÍNH XÁC**  
**Tác giả**: Trần Trung Anh¹, Quách Mạnh Tuấn²  
¹ Trường Đại học Mỏ - Địa chất  
² Công ty CP Xây dựng và Thương mại QT Miền Bắc  
**Trình bày tại**: HỘI NGHỊ KHOA HỌC QUỐC GIA VỀ CÔNG NGHỆ ĐỊA KHÔNG GIAN TRONG KHOA HỌC TRÁI ĐẤT VÀ MÔI TRƯỜNG
")
