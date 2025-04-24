
def render_map(df):
    import pydeck as pdk
    if not df.empty and "Vĩ độ (Lat)" in df.columns and "Kinh độ (Lon)" in df.columns:
        deck = pdk.Deck(
            map_style="mapbox://styles/mapbox/streets-v12",
            initial_view_state=pdk.ViewState(
                latitude=df["Vĩ độ (Lat)"].mean(),
                longitude=df["Kinh độ (Lon)"].mean(),
                zoom=14,
                pitch=0,
            ),
            layers=[
                pdk.Layer(
                    "ScatterplotLayer",
                    data=df,
                    get_position="[Kinh độ (Lon), Vĩ độ (Lat)]",
                    get_color="[255, 0, 0, 160]",
                    get_radius=1,
                    radius_min_pixels=1,
                    radius_max_pixels=2,
                    pickable=False
                )
            ],
        )
        st.pydeck_chart(deck)
    else:
        st.warning("⚠️ Không có dữ liệu để hiển thị bản đồ.")



import streamlit as st
import pandas as pd
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
        st.session_state.vn2000_results = st.session_state.get("vn2000_results", [])
        st.session_state.vn2000_df = None
    
        raw_data = coords_input.replace('\t', ' ').replace('\n', ' ').split()
        points = []
        i = 0
        while i < len(raw_data):
            try:
                float(raw_data[i+1])
                float(raw_data[i+2])
                float(raw_data[i+3])
                points.append([raw_data[i+1], raw_data[i+2], raw_data[i+3]])
                i += 4
            except:
                try:
                    float(raw_data[i])
                    float(raw_data[i+1])
                    float(raw_data[i+2])
                    points.append([raw_data[i], raw_data[i+1], raw_data[i+2]])
                    i += 3
                except:
                    i += 1

        results = st.session_state.get("vn2000_results", [])
        for p in points:
            try:
                x, y, z = map(float, p)
                lat, lon, h = vn2000_to_wgs84_baibao(x, y, z, lon0)
                results.append((lat, lon, h))
            except:
                continue

        if results:
            df = pd.DataFrame(results, columns=["Vĩ độ (Lat)", "Kinh độ (Lon)", "Cao độ ellipsoid (H)"])
            st.session_state.vn2000_df = df
            st.dataframe(df)

            # Hiển thị tất cả điểm trên bản đồ
            
            
            # Hiển thị bản đồ tất cả điểm (dùng pydeck với chấm nhỏ)
            
    


if "vn2000_df" in st.session_state:
    df = st.session_state.vn2000_df
    render_map(df)



        st.warning("⚠️ Không có dữ liệu để hiển thị bản đồ.")
