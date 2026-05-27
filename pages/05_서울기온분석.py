import streamlit as st
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="서울 기온 분석", layout="wide")

st.title("📈 서울 특정 날짜 기온 변화")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("seoul.csv", encoding="euc-kr")

    df["날짜"] = pd.to_datetime(df["날짜"])
    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    return df

df = load_data()

# 월/일 선택
col1, col2 = st.columns(2)

with col1:
    month = st.selectbox("월 선택", sorted(df["월"].unique()))

with col2:
    possible_days = sorted(df[df["월"] == month]["일"].unique())
    day = st.selectbox("일 선택", possible_days)

# 선택 날짜 데이터
filtered = df[(df["월"] == month) & (df["일"] == day)]

# 그래프 생성
fig = go.Figure()

# 최고기온
fig.add_trace(
    go.Scatter(
        x=filtered["연도"],
        y=filtered["최고기온(℃)"],
        mode="lines+markers",
        name="최고기온",
        line=dict(color="hotpink", width=3),
    )
)

# 최저기온
fig.add_trace(
    go.Scatter(
        x=filtered["연도"],
        y=filtered["최저기온(℃)"],
        mode="lines+markers",
        name="최저기온",
        line=dict(color="#A7D8FF", width=3),
    )
)

fig.update_layout(
    title=f"{month}월 {day}일 연도별 최고·최저기온 변화",
    xaxis_title="연도",
    yaxis_title="기온 (℃)",
    hovermode="x unified",
    template="plotly_white",
    height=600
)

st.plotly_chart(fig, use_container_width=True)

# 데이터 표
with st.expander("데이터 보기"):
    st.dataframe(
        filtered[["연도", "최고기온(℃)", "최저기온(℃)", "평균기온(℃)"]]
        .sort_values("연도")
        .reset_index(drop=True)
    )
