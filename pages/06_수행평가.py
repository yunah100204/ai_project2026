import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="서울 공공와이파이 분석",
    page_icon="📶",
    layout="wide"
)

st.title("📶 서울 공공와이파이 사용량 분석")
st.markdown("---")

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv(
        "서울특별시_공공와이파이_AP별_사용량.csv",
        encoding="cp949"
    )

    # 컬럼명 공백 제거
    df.columns = df.columns.str.strip()

    return df

df = load_data()

# 실제 컬럼명 확인 후 수정 가능
district_col = "자치구"
usage_col = "사용량(GB)"

# 자치구별 집계
district_usage = (
    df.groupby(district_col)[usage_col]
    .sum()
    .reset_index()
    .sort_values(usage_col, ascending=False)
)

# 사이드바
st.sidebar.header("설정")

selected_gu = st.sidebar.selectbox(
    "자치구 선택",
    sorted(df[district_col].dropna().unique())
)

# 선택 자치구 데이터
selected_df = df[df[district_col] == selected_gu]

st.subheader(f"📍 {selected_gu} 와이파이 사용량")

fig = px.bar(
    selected_df,
    x="관리번호",
    y=usage_col,
    title=f"{selected_gu} AP별 사용량",
    labels={
        "관리번호": "AP 관리번호",
        usage_col: "사용량(GB)"
    }
)

fig.update_layout(
    height=500,
    xaxis_tickangle=-45
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

st.subheader("🏆 사용량 TOP 10 자치구")

top10 = district_usage.head(10)

fig2 = px.bar(
    top10,
    x=usage_col,
    y=district_col,
    orientation="h",
    text_auto=".2s",
    title="TOP 10 자치구"
)

fig2.update_layout(
    height=600,
    yaxis=dict(categoryorder="total ascending")
)

st.plotly_chart(fig2, use_container_width=True)

st.dataframe(
    top10.reset_index(drop=True),
    use_container_width=True
)

st.markdown("---")

st.metric(
    "전체 사용량(GB)",
    f"{district_usage[usage_col].sum():,.0f}"
)

st.metric(
    "전체 자치구 수",
    district_usage.shape[0]
)
