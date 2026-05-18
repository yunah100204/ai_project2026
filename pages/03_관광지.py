# app.py
import streamlit as st
import folium
from streamlit.components.v1 import html

st.set_page_config(page_title="서울 인기 관광지 TOP10", layout="wide")

st.title("🌏 외국인들이 좋아하는 서울 관광지 TOP10")

tour_places = [
    {
        "name": "경복궁",
        "lat": 37.579617,
        "lon": 126.977041,
        "subway": "경복궁역",
        "fun": "한복 체험, 궁궐 산책, 야간개장"
    },
    {
        "name": "명동",
        "lat": 37.563757,
        "lon": 126.985302,
        "subway": "명동역",
        "fun": "쇼핑, 길거리 음식, 화장품 투어"
    },
    {
        "name": "남산서울타워",
        "lat": 37.551169,
        "lon": 126.988227,
        "subway": "명동역",
        "fun": "야경 감상, 케이블카, 사랑의 자물쇠"
    },
    {
        "name": "홍대거리",
        "lat": 37.556336,
        "lon": 126.922652,
        "subway": "홍대입구역",
        "fun": "버스킹, 카페 투어, 쇼핑"
    },
    {
        "name": "북촌한옥마을",
        "lat": 37.582604,
        "lon": 126.983998,
        "subway": "안국역",
        "fun": "한옥 감상, 사진 촬영, 전통문화 체험"
    },
    {
        "name": "롯데월드",
        "lat": 37.511115,
        "lon": 127.098167,
        "subway": "잠실역",
        "fun": "놀이기구, 퍼레이드, 아이스링크"
    },
    {
        "name": "동대문디자인플라자(DDP)",
        "lat": 37.566526,
        "lon": 127.009223,
        "subway": "동대문역사문화공원역",
        "fun": "야경, 전시회, 디자인 쇼핑"
    },
    {
        "name": "한강공원",
        "lat": 37.528316,
        "lon": 126.932455,
        "subway": "여의나루역",
        "fun": "치킨 먹방, 자전거, 피크닉"
    },
    {
        "name": "인사동",
        "lat": 37.574032,
        "lon": 126.985302,
        "subway": "안국역",
        "fun": "전통찻집, 기념품 쇼핑, 갤러리"
    },
    {
        "name": "코엑스",
        "lat": 37.512524,
        "lon": 127.058819,
        "subway": "삼성역",
        "fun": "별마당도서관, 아쿠아리움, 쇼핑"
    }
]

# 서울 중심 좌표
m = folium.Map(location=[37.5665, 126.9780], zoom_start=11)

# 관광지 마커 추가
for place in tour_places:
    popup_html = f"""
    <b>{place['name']}</b><br>
    🚇 가까운 지하철역: {place['subway']}<br>
    🎈 놀거리: {place['fun']}
    """
    
    folium.Marker(
        [place["lat"], place["lon"]],
        popup=popup_html,
        tooltip=place["name"],
        icon=folium.Icon(color="red", icon="star")
    ).add_to(m)

# HTML로 지도 출력
map_html = m._repr_html_()

html(
    f"""
    <div style="width:100%; height:700px;">
        {map_html}
    </div>

    <div style="margin-top:20px; padding:15px; border-radius:10px; background:#f5f5f5;">
        <h3>📍 관광지 정보</h3>
        <p>
        지도를 클릭하면 가까운 지하철역과 놀거리를 확인할 수 있습니다.
        </p>
    </div>
    """,
    height=800
)
