import pandas as pd

import streamlit as st
from functions import vn2000_to_wgs84_baibao, wgs84_to_vn2000_baibao

st.set_page_config(page_title="VN2000 ⇄ WGS84 Converter", layout="centered")
col_logo, col_title = st.columns([1, 5])
with col_logo:
    st.image("logo.jpg", width=90)
with col_title:
    st.markdown("<h5 style='margin-bottom:0;'>BẤT ĐỘNG SẢN HUYỆN HƯỚNG HÓA</h5>", unsafe_allow_html=True)
    st.markdown("<h6 style='color:gray;'>VN2000 ⇄ WGS84</h6>", unsafe_allow_html=True)

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
        temp = []
        i = 0
        while i < len(raw_data):
            try:
                # Thử lấy 4 phần tử, nếu phần đầu không phải số thực thì bỏ
                float(raw_data[i+1])
                float(raw_data[i+2])
                float(raw_data[i+3])
                temp.append([raw_data[i+1], raw_data[i+2], raw_data[i+3]])
                i += 4
            except:
                try:
                    # Nếu 3 phần tử liền nhau là tọa độ thì giữ
                    float(raw_data[i])
                    float(raw_data[i+1])
                    float(raw_data[i+2])
                    temp.append([raw_data[i], raw_data[i+1], raw_data[i+2]])
                    i += 3
                except:
                    i += 1
        points = temp

            parts = line.replace('\t', ' ').strip().split()
            if len(parts) == 4:  # Bỏ STT đầu tiên
                parts = parts[1:]
            if len(parts) == 3:
                try:
                    float(parts[0]); float(parts[1]); float(parts[2])
                    points.append(parts)
                except:
                    continue
    
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
            
            df = pd.DataFrame(results, columns=["Vĩ độ (Lat)", "Kinh độ (Lon)", "Cao độ ellipsoid (H)"])
            st.dataframe(df)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Tải kết quả CSV", data=csv, file_name="VN2000_to_WGS84.csv", mime="text/csv")
    
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
        temp = []
        i = 0
        while i < len(raw_data):
            try:
                # Thử lấy 4 phần tử, nếu phần đầu không phải số thực thì bỏ
                float(raw_data[i+1])
                float(raw_data[i+2])
                float(raw_data[i+3])
                temp.append([raw_data[i+1], raw_data[i+2], raw_data[i+3]])
                i += 4
            except:
                try:
                    # Nếu 3 phần tử liền nhau là tọa độ thì giữ
                    float(raw_data[i])
                    float(raw_data[i+1])
                    float(raw_data[i+2])
                    temp.append([raw_data[i], raw_data[i+1], raw_data[i+2]])
                    i += 3
                except:
                    i += 1
        points = temp

            parts = line.replace('\t', ' ').strip().split()
            if len(parts) == 4:  # Bỏ STT đầu tiên
                parts = parts[1:]
            if len(parts) == 3:
                try:
                    float(parts[0]); float(parts[1]); float(parts[2])
                    points.append(parts)
                except:
                    continue
    
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
            
            df = pd.DataFrame(results, columns=["Hoành độ x", "Tung độ y", "Cao độ chuẩn (h)"])
            st.dataframe(df)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Tải kết quả CSV", data=csv, file_name="WGS84_to_VN2000.csv", mime="text/csv")
    
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

