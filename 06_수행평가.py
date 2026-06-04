import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="서울 공공와이파이 분석",
    page_icon="📶",
    layout="wide"
)

st.title("📶 서울 공공와이파이 사용량 분석")

@st.cache_data
def load_data():
    df = pd.read_csv(
        "서울공공와이파이.csv",
        encoding="cp949",
        low_memory=False
    )

    df.columns = df.columns.str.strip()
    return df

df = load_data()

# 컬럼 자동 찾기
district_col = next(
    (c for c in df.columns if "자치구" in c),
    None
)

usage_col = next(
    (c for c in df.columns if "이용량" in c or "사용량" in c),
    None
)

id_col = next(
    (c for c in df.columns if "관리번호" in c),
    None
)

if district_col is None or usage_col is None:
    st.error(f"현재 컬럼: {df.columns.tolist()}")
    st.stop()

df[usage_col] = pd.to_numeric(
    df[usage_col],
    errors="coerce"
)

district_usage = (
    df.groupby(district_col)[usage_col]
      .sum()
      .reset_index()
      .sort_values(usage_col, ascending=False)
)

selected_gu = st.sidebar.selectbox(
    "자치구 선택",
    district_usage[district_col]
)

selected_df = df[
    df[district_col] == selected_gu
]

st.subheader(f"📍 {selected_gu}")

if id_col:
    fig = px.bar(
        selected_df,
        x=id_col,
        y=usage_col,
        title=f"{selected_gu} AP별 사용량"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.subheader("🏆 사용량 TOP10 자치구")

top10 = district_usage.head(10)

fig2 = px.bar(
    top10,
    x=usage_col,
    y=district_col,
    orientation="h",
    text_auto=True
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.dataframe(
    top10,
    use_container_width=True
)
