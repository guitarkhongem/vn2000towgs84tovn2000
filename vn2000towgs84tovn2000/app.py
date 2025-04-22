
import streamlit as st
import os
from vn2000_to_wgs84_baibao import vn2000_to_wgs84_baibao

st.set_page_config(page_title="VN2000 ➜ WGS84 (chuẩn bài báo)", layout="centered")

if os.path.exists("logo.jpg"):
    st.image("logo.jpg", width=120)

st.title("📐 Chuyển đổi tọa độ VN2000 ➜ WGS84 (Công thức bài báo khoa học)")

st.markdown("#### 🔢 Nhập tọa độ VN-2000:")

x = st.number_input("Tọa độ X (Northing)", value=1855759.3584, format="%.4f")
y = st.number_input("Tọa độ Y (Easting)", value=546151.8072, format="%.4f")
h = st.number_input("Cao độ elipsoid (H)", value=846.1115, format="%.4f")
lon0 = st.number_input("Kinh tuyến trục (VD: 106.25)", value=106.25)

if st.button("🔄 Chuyển đổi"):
    lat, lon, h_out = vn2000_to_wgs84_baibao(x, y, h, lon0)
    h_out = round(h_out, 3)

    st.success("✅ Kết quả chuyển đổi (WGS84):")
    st.markdown(
        f"""
        <div style='background-color:#FFD700;padding:15px;border-radius:10px'>
        <h2 style='color:#000000;'>🧭 Kinh độ (Lon): <code>{lon}</code></h2>
        <h2 style='color:#000000;'>🧭 Vĩ độ (Lat): <code>{lat}</code></h2>
        <h2 style='color:#000000;'>🗻 Cao độ Altitude: <code>{h_out}</code> m</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")
    st.markdown("""
    <div style='font-size: 16px; color: gray;'>
    🔍 **Nguồn công thức**:  
    Bài báo khoa học: <strong>CÔNG TÁC TÍNH CHUYỂN TỌA ĐỘ TRONG CÔNG NGHỆ MÁY BAY KHÔNG NGƯỜI LÁI CÓ ĐỊNH VỊ TÂM CHỤP CHÍNH XÁC</strong><br>
    Tác giả: Trần Trung Anh<sup>1</sup>, Quách Mạnh Tuấn<sup>2</sup><br>
    <sup>1</sup>Trường Đại học Mỏ - Địa chất<br>
    <sup>2</sup>Công ty CP Xây dựng và Thương mại QT Miền Bắc<br><br>
    Trình bày tại: <strong>HỘI NGHỊ KHOA HỌC QUỐC GIA VỀ CÔNG NGHỆ ĐỊA KHÔNG GIAN TRONG KHOA HỌC TRÁI ĐẤT VÀ MÔI TRƯỜNG</strong>
    </div>
    """, unsafe_allow_html=True)



st.markdown("### 🔄 Chuyển ngược từ WGS84 ➜ VN2000")

lat_in = st.number_input("Vĩ độ (Lat)", value=16.77839862, format="%.8f", key="lat")
lon_in = st.number_input("Kinh độ (Lon)", value=106.6847777, format="%.8f", key="lon")
h_in = st.number_input("Cao độ Altitude (m)", value=832.2537252, format="%.4f", key="alt")
lon0_in = st.number_input("Kinh tuyến trục (VD: 106.25)", value=106.25, key="lon0")

if st.button("↩️ Chuyển về VN2000"):
    from vn2000_to_wgs84_baibao import wgs84_to_vn2000_baibao
    x_back, y_back, h_back = wgs84_to_vn2000_baibao(lat_in, lon_in, h_in, lon0_in)

    st.success("✅ Kết quả chuyển đổi (VN2000):")
    st.markdown(
        f"""
        <div style='background-color:#90ee90;padding:15px;border-radius:10px'>
        <h2 style='color:#000000;'>🧭 Tọa độ X (Northing): <code>{x_back}</code></h2>
        <h2 style='color:#000000;'>🧭 Tọa độ Y (Easting): <code>{y_back}</code></h2>
        <h2 style='color:#000000;'>🗻 Cao độ elipsoid (H): <code>{h_back}</code> m</h2>
        </div>
        """,
        unsafe_allow_html=True
    )
