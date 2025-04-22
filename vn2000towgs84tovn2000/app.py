
import streamlit as st
import pandas as pd
from vn2000_to_wgs84_baibao import vn2000_to_wgs84_baibao

st.set_page_config(page_title="VN2000 ➜ WGS84", layout="centered")

# Logo
st.image("logo.jpg", width=100)

# Tiêu đề chính
st.markdown("## 📍 Chuyển đổi tọa độ VN2000 ➜ WGS84")
st.markdown("### ✅ Áp dụng đầy đủ công thức từ **bài báo khoa học** tại HỘI NGHỊ KHOA HỌC QUỐC GIA VỀ CÔNG NGHỆ ĐỊA KHÔNG GIAN")

# Nhập dữ liệu
st.markdown("#### 🔢 Nhập tọa độ VN2000 (X, Y, Z – cách nhau bởi dấu cách hoặc tab):")
coords_input = st.text_area("Mỗi dòng một điểm", height=200)

# Chọn kinh tuyến trục
lon0 = st.selectbox("🌐 Chọn kinh tuyến trục (°)", [
    102.75, 103.0, 103.5, 104.0, 104.25, 104.5, 105.0,
    105.25, 105.5, 106.0, 106.25, 106.5, 107.0, 107.25,
    107.5, 108.0, 108.25, 108.5, 109.0, 109.25, 109.5
], index=9)

# Nút chuyển đổi
if st.button("🔁 Chuyển đổi"):
    rows = []
    for line in coords_input.strip().split("\n"):
        parts = line.strip().split()
        if len(parts) >= 2:
            try:
                x = float(parts[0])
                y = float(parts[1])
                z = float(parts[2]) if len(parts) >= 3 else 0.0
                lat, lon, alt = vn2000_to_wgs84_baibao(x, y, z, lon0)
                rows.append({
                    "X": x,
                    "Y": y,
                    "Z": z,
                    "Kinh độ (Lon)": round(lon, 15),
                    "Vĩ độ (Lat)": round(lat, 15),
                    "Cao độ Altitude (m)": round(alt, 4)
                })
            except:
                continue

    if rows:
        st.success("✅ Chuyển đổi thành công!")
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ Không có dòng hợp lệ để chuyển đổi.")

# Ghi chú cuối trang
st.markdown("---")
st.markdown("**Nguồn công thức**: Bài báo _“CÔNG TÁC TÍNH CHUYỂN TỌA ĐỘ TRONG CÔNG NGHỆ MÁY BAY KHÔNG NGƯỜI LÁI CÓ ĐỊNH VỊ TÂM CHỤP CHÍNH XÁC”_ – Trần Trung Anh, Quách Mạnh Tuấn – Đại học Mỏ Địa chất, QT Miền Bắc.")
