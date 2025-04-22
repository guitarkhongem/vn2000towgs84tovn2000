
import streamlit as st
import pandas as pd
from vn2000_to_wgs84_baibao import vn2000_to_wgs84_baibao

st.set_page_config(page_title="VN2000 ➜ WGS84", layout="centered")

# Logo
st.image("logo.jpg", width=100)

# Tiêu đề chính
st.markdown("### 🛰️ VN2000 ➜ WGS84", unsafe_allow_html=True)
st.markdown("<div style='font-size: 0.7em; color: gray;'>Chuyển đổi tọa độ theo hệ quy chiếu quốc gia</div>", unsafe_allow_html=True)

# Nhập dữ liệu
st.markdown("#### 🔢 Nhập tọa độ VN2000 (X Y Z – cách nhau bởi dấu cách, tab hoặc enter):")
coords_input = st.text_area("Mỗi dòng một điểm hoặc nhập liên tục", height=200)

# Chọn kinh tuyến trục
lon0 = st.selectbox("🌐 Chọn kinh tuyến trục (°)", [
    102.75, 103.0, 103.5, 104.0, 104.25, 104.5, 105.0,
    105.25, 105.5, 106.0, 106.25, 106.5, 107.0, 107.25,
    107.5, 108.0, 108.25, 108.5, 109.0, 109.25, 109.5
], index=10)

# Nút chuyển đổi
if st.button("🔁 Chuyển đổi"):
    # Tách theo mọi ký tự trắng, xuống dòng hoặc tab
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
        st.warning("⚠️ Không có dữ liệu hợp lệ.")
