
import streamlit as st
import pandas as pd
from vn2000_to_wgs84_baibao import vn2000_to_wgs84_baibao, wgs84_to_vn2000_baibao

st.set_page_config(page_title="Chuyển đổi VN2000 ↔ WGS84", layout="centered")

# Logo và tiêu đề phụ
col1, col2 = st.columns([1, 3])
with col1:
    st.image("logo.jpg", width=100)
with col2:
    st.markdown("<h4 style='margin-top:40px;'>BẤT ĐỘNG SẢN HUYỆN HƯỚNG HÓA</h4>", unsafe_allow_html=True)

# Tiêu đề chính
st.markdown("### 🛰️ VN2000 ↔ WGS84", unsafe_allow_html=True)
st.markdown("<div style='font-size: 0.7em; color: gray;'>Chuyển đổi tọa độ theo hệ quy chiếu quốc gia</div>", unsafe_allow_html=True)

# Tabs chuyển đổi
tab1, tab2 = st.tabs(["🡺 VN2000 ➜ WGS84", "🡸 WGS84 ➜ VN2000"])

# TAB 1: VN2000 ➜ WGS84
with tab1:
    st.markdown("#### 🔢 Nhập tọa độ VN2000 (X Y Z – cách nhau bởi dấu cách, tab hoặc enter):")
    coords_input = st.text_area("Mỗi dòng một điểm hoặc nhập liên tục", height=200, key="vn2000_input")
    lon0 = st.selectbox("🌐 Chọn kinh tuyến trục (°)", [102.75, 103.0, 103.5, 104.0, 104.25, 104.5, 105.0,
        105.25, 105.5, 106.0, 106.25, 106.5, 107.0, 107.25, 107.5, 108.0, 108.25, 108.5, 109.0, 109.25, 109.5],
        index=10, key="lon0_vn2000")

    if st.button("🔁 Chuyển sang WGS84"):
        raw_data = coords_input.replace('\t', ' ').replace('\n', ' ')
        tokens = raw_data.split()

        rows = []
        for i in range(0, len(tokens), 3):
            try:
                x = float(tokens[i])
                y = float(tokens[i + 1])
                z = float(tokens[i + 2]) if i + 2 < len(tokens) else 0.0
                lat, lon, alt = vn2000_to_wgs84_baibao(x, y, z, lon0)
                rows.append({
                    "X": x, "Y": y, "Z": z,
                    "Kinh độ (Lon)": round(lon, 15),
                    "Vĩ độ (Lat)": round(lat, 15),
                    "Cao độ Altitude (m)": round(alt, 4)
                })
            except:
                continue
        if rows:
            st.success("✅ Chuyển đổi thành công!")
            st.dataframe(pd.DataFrame(rows), use_container_width=True)
        else:
            st.warning("⚠️ Không có dữ liệu hợp lệ.")

# TAB 2: WGS84 ➜ VN2000
with tab2:
    st.markdown("#### 🔢 Nhập tọa độ WGS84 (Lat Lon H – cách nhau bởi dấu cách, tab hoặc enter):")
    coords_input = st.text_area("Mỗi dòng một điểm hoặc nhập liên tục", height=200, key="wgs84_input")
    lon0 = st.selectbox("🌐 Chọn kinh tuyến trục (°)", [102.75, 103.0, 103.5, 104.0, 104.25, 104.5, 105.0,
        105.25, 105.5, 106.0, 106.25, 106.5, 107.0, 107.25, 107.5, 108.0, 108.25, 108.5, 109.0, 109.25, 109.5],
        index=10, key="lon0_wgs84")

    if st.button("🔁 Chuyển sang VN2000"):
        raw_data = coords_input.replace('\t', ' ').replace('\n', ' ')
        tokens = raw_data.split()

        rows = []
        for i in range(0, len(tokens), 3):
            try:
                lat = float(tokens[i])
                lon = float(tokens[i + 1])
                h = float(tokens[i + 2]) if i + 2 < len(tokens) else 0.0
                x, y, z = wgs84_to_vn2000_baibao(lat, lon, h, lon0)
                rows.append({
                    "Lat": lat, "Lon": lon, "H": h,
                    "X (VN2000)": round(x, 4),
                    "Y (VN2000)": round(y, 4),
                    "Z (VN2000)": round(z, 4)
                })
            except:
                continue
        if rows:
            st.success("✅ Chuyển đổi thành công!")
            st.dataframe(pd.DataFrame(rows), use_container_width=True)
        else:
            st.warning("⚠️ Không có dữ liệu hợp lệ.")

# Ghi chú nguồn công thức
st.markdown("---")
st.markdown("""
🔍 **Nguồn công thức**: Bài báo khoa học: **CÔNG TÁC TÍNH CHUYỂN TỌA ĐỘ TRONG CÔNG NGHỆ MÁY BAY KHÔNG NGƯỜI LÁI CÓ ĐỊNH VỊ TÂM CHỤP CHÍNH XÁC**  
Tác giả: Trần Trung Anh¹, Quách Mạnh Tuấn²  
¹ Trường Đại học Mỏ - Địa chất  
² Công ty CP Xây dựng và Thương mại QT Miền Bắc  
_Trình bày tại: HỘI NGHỊ KHOA HỌC QUỐC GIA VỀ CÔNG NGHỆ ĐỊA KHÔNG GIAN TRONG KHOA HỌC TRÁI ĐẤT VÀ MÔI TRƯỜNG_
""")
