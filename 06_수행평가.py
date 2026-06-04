import streamlit as st
import pandas as pd
import plotly.express as px
import zipfile

st.set_page_config(
    page_title="서울 공공와이파이 분석",
    page_icon="📶",
    layout="wide"
)

st.title("📶 서울 공공와이파이 사용량 분석")

@st.cache_data
def load_data():
    with zipfile.ZipFile(
        "서울특별시_공공와이파이 AP별 사용량_10_13_2021.zip"
    ) as z:

        csv_file = [f for f in z.namelist() if "공공장소" in f][0]

        with z.open(csv_file) as f:
            df = pd.read_csv(
                f,
                encoding="cp949"
            )

    df.columns = df.columns.str.strip()

    return df

df = load_data()

# 실제 컬럼명 확인
district_col = "자치구"

# 사용량 컬럼 자동 탐색
usage_col = None
for col in df.columns:
    if "이용량" in col or "사용량" in col:
        usage_col = col
        break

if usage_col is None:
    st.error("사용량 컬럼을 찾을 수 없습니다.")
    st.write("현재 컬럼:", df.columns.tolist())
    st.stop()

# 숫자형 변환
df[usage_col] = pd.to_numeric(
    df[usage_col],
    errors="coerce"
)

# 자치구별 집계
district_usage = (
    df.groupby(district_col)[usage_col]
    .sum()
    .reset_index()
    .sort_values(
        usage_col,
        ascending=False
    )
)

# 사이드바
st.sidebar.subheader("데이터 정보")
st.sidebar.write(f"데이터 크기: {df.shape}")

selected_gu = st.sidebar.selectbox(
    "자치구 선택",
    district_usage[district_col].tolist()
)

# 선택 자치구 데이터
selected_df = df[
    df[district_col] == selected_gu
]

st.subheader(f"📍 {selected_gu} AP별 사용량")

fig = px.bar(
    selected_df,
    x="관리번호",
    y=usage_col,
    title=f"{selected_gu} AP별 사용량"
)

fig.update_layout(
    xaxis_tickangle=-45,
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# TOP10 자치구
st.subheader("🏆 사용량 TOP10 자치구")

top10 = district_usage.head(10).sort_values(
    usage_col,
    ascending=True
)

fig2 = px.bar(
    top10,
    x=usage_col,
    y=district_col,
    orientation="h",
    text_auto=".2s",
    title="사용량 TOP10 자치구"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.dataframe(
    top10,
    use_container_width=True
)

# 통계
st.subheader("📊 전체 통계")

col1, col2 = st.columns(2)

with col1:
    st.metric(
        "전체 사용량(GB)",
        f"{district_usage[usage_col].sum():,.0f}"
    )

with col2:
    st.metric(
        "자치구 수",
        district_usage.shape[0]
    )
