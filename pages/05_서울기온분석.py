import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 페이지 설정
st.set_page_config(
    page_title="서울 기온 분석",
    layout="wide"
)

st.title("📈 서울 특정 날짜 기온 변화 분석")

# 데이터 불러오기
@st.cache_data
def load_data():
    # CSV 읽기
    df = pd.read_csv("seoul.csv", encoding="euc-kr")

    # 날짜 문자열 정리
    df["날짜"] = df["날짜"].astype(str).str.strip()

    # 날짜 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"],
        errors="coerce"
    )

    # 잘못된 날짜 제거
    df = df.dropna(subset=["날짜"])

    # 연/월/일 컬럼 생성
    df["연도"] = df["날짜"].dt.year
    df["월"] = df["날짜"].dt.month
    df["일"] = df["날짜"].dt.day

    return df

df = load_data()

# 월 선택
month = st.selectbox(
    "📅 월 선택",
    sorted(df["월"].unique())
)

# 해당 월의 가능한 일만 표시
available_days = sorted(
    df[df["월"] == month]["일"].unique()
)

# 일 선택
day = st.selectbox(
    "📌 일 선택",
    available_days
)

# 데이터 필터링
filtered_df = df[
    (df["월"] == month) &
    (df["일"] == day)
].sort_values("연도")

st.subheader(f"📊 {month}월 {day}일 연도별 기온 변화")

# 그래프 생성
fig = go.Figure()

# 최고기온
fig.add_trace(
    go.Scatter(
        x=filtered_df["연도"],
        y=filtered_df["최고기온(℃)"],
        mode="lines+markers",
        name="최고기온",
        line=dict(
            color="hotpink",
            width=3
        ),
        marker=dict(size=6)
    )
)

# 최저기온
fig.add_trace(
    go.Scatter(
        x=filtered_df["연도"],
        y=filtered_df["최저기온(℃)"],
        mode="lines+markers",
        name="최저기온",
        line=dict(
            color="#A7D8FF",
            width=3
        ),
        marker=dict(size=6)
    )
)

# 레이아웃 설정
fig.update_layout(
    template="plotly_white",
    height=650,
    hovermode="x unified",
    xaxis_title="연도",
    yaxis_title="기온 (℃)",
    legend_title="구분",
    title=f"{month}월 {day}일 서울 기온 변화"
)

# 그래프 출력
st.plotly_chart(
    fig,
    use_container_width=True
)

# 데이터 보기
with st.expander("📄 데이터 보기"):
    st.dataframe(
        filtered_df[
            ["연도", "평균기온(℃)", "최저기온(℃)", "최고기온(℃)"]
        ].reset_index(drop=True),
        use_container_width=True
    )
