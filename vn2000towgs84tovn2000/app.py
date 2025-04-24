
import streamlit as st
from functions import vn2000_to_wgs84_baibao, wgs84_to_vn2000_baibao

st.set_page_config(page_title="VN2000 ⇄ WGS84 Converter", layout="centered")
st.title("📍 Chuyển đổi tọa độ VN2000 ⇄ WGS84")

tab1, tab2 = st.tabs(["➡️ VN2000 → WGS84", "⬅️ WGS84 → VN2000"])

with tab1:
    st.markdown("#### 🔢 Nhập tọa độ VN2000 (X Y Z – cách nhau bởi dấu cách, tab hoặc enter):")
    coords_input = st.text_area("Mỗi dòng một điểm hoặc nhập liên tục", height=200, key="vn2000_input")
    lon0 = st.selectbox("🌐 Chọn kinh tuyến trục (°)", [
        102.75, 103.0, 103.5, 104.0, 104.25, 104.5, 105.0,
        105.25, 105.5, 106.0, 106.25, 106.5, 107.0, 107.25,
        107.5, 108.0, 108.25, 108.5, 109.0, 109.25, 109.5
    ], index=10, key="lon0_vn2000")

    if st.button("🔁 Chuyển sang WGS84"):
        raw_data = coords_input.replace('\t', ' ').replace('\n', ' ').split()
        points = [raw_data[i:i+3] for i in range(0, len(raw_data), 3)]
        results = []
        for point in points:
            if len(point) == 3:
                try:
                    x, y, z = map(float, point)
                    lat, lon, h = vn2000_to_wgs84_baibao(x, y, z, lon0)
                    results.append((lat, lon, h))
                except:
                    continue
        if results:
            st.success("🎯 Kết quả chuyển đổi:")
            for idx, (lat, lon, h) in enumerate(results):
                st.markdown(f"**Điểm {idx+1}:** Lat: `{lat:.8f}` | Lon: `{lon:.8f}` | H: `{h:.3f}` m")
        else:
            st.warning("⚠️ Không có dữ liệu hợp lệ.")

with tab2:
    st.markdown("#### 🔢 Nhập tọa độ WGS84 (Lat Lon H – cách nhau bởi dấu cách, tab hoặc enter):")
    coords_input = st.text_area("Mỗi dòng một điểm hoặc nhập liên tục", height=200, key="wgs84_input")
    lon0 = st.selectbox("🌐 Chọn kinh tuyến trục (°)", [
        102.75, 103.0, 103.5, 104.0, 104.25, 104.5, 105.0,
        105.25, 105.5, 106.0, 106.25, 106.5, 107.0, 107.25,
        107.5, 108.0, 108.25, 108.5, 109.0, 109.25, 109.5
    ], index=10, key="lon0_wgs84")

    if st.button("🔁 Chuyển sang VN2000"):
        raw_data = coords_input.replace('\t', ' ').replace('\n', ' ').split()
        points = [raw_data[i:i+3] for i in range(0, len(raw_data), 3)]
        results = []
        for point in points:
            if len(point) == 3:
                try:
                    lat, lon, h = map(float, point)
                    x, y, h_vn = wgs84_to_vn2000_baibao(lat, lon, h, lon0)
                    results.append((x, y, h_vn))
                except:
                    continue
        if results:
            st.success("🎯 Kết quả chuyển đổi:")
            for idx, (x, y, h_vn) in enumerate(results):
                st.markdown(f"**Điểm {idx+1}:** x: `{x:.4f}` | y: `{y:.4f}` | h: `{h_vn:.4f}` m")
        else:
            st.warning("⚠️ Không có dữ liệu hợp lệ.")

# Ghi chú cuối trang
st.markdown("---")
st.markdown("🔍 **Nguồn công thức**: Bài báo khoa học: "
            "**CÔNG TÁC TÍNH CHUYỂN TỌA ĐỘ TRONG CÔNG NGHỆ MÁY BAY KHÔNG NGƯỜI LÁI CÓ ĐỊNH VỊ TÂM CHỤP CHÍNH XÁC**  \n"
            "Tác giả: Trần Trung Anh¹, Quách Mạnh Tuấn²  \n"
            "¹ Trường Đại học Mỏ - Địa chất  \n"
            "² Công ty CP Xây dựng và Thương mại QT Miền Bắc  \n"
            "_Trình bày tại: HỘI NGHỊ KHOA HỌC QUỐC GIA VỀ CÔNG NGHỆ ĐỊA KHÔNG GIAN TRONG KHOA HỌC TRÁI ĐẤT VÀ MÔI TRƯỜNG_")
