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

    zip_path = "서울특별시_공공와이파이 AP별 사용량_10_13_2021.zip"

    with zipfile.ZipFile(zip_path, "r") as z:

        csv_files = [
            f for f in z.namelist()
            if f.lower().endswith(".csv")
        ]

        if not csv_files:
            st.error("ZIP 파일 안에 CSV 파일이 없습니다.")
            st.stop()

        df = None

        # 자치구 컬럼이 있는 CSV 자동 선택
        for csv_file in csv_files:
            try:
                with z.open(csv_file) as f:
                    temp = pd.read_csv(
                        f,
                        encoding="cp949",
                        low_memory=False
                    )

                temp.columns = temp.columns.str.strip()

                if "자치구" in temp.columns:
                    df = temp
                    break

            except Exception:
                continue

        # 못 찾으면 첫 번째 CSV 사용
        if df is None:
            with z.open(csv_files[0]) as f:
                df = pd.read_csv(
                    f,
                    encoding="cp949",
                    low_memory=False
                )

    df.columns = df.columns.str.strip()

    return df

df = load_data()

# 컬럼 자동 탐색
district_col = None
usage_col = None
id_col = None

for col in df.columns:
    if "자치구" in col:
        district_col = col

    if "관리번호" in col:
        id_col = col

    if ("이용량" in col) or ("사용량" in col):
        usage_col = col

if district_col is None:
    st.error("자치구 컬럼을 찾을 수 없습니다.")
    st.write(df.columns.tolist())
    st.stop()

if usage_col is None:
    st.error("사용량 컬럼을 찾을 수 없습니다.")
    st.write(df.columns.tolist())
    st.stop()

df[usage_col] = pd.to_numeric(
    df[usage_col],
    errors="coerce"
)

district_usage = (
    df.groupby(district_col)[usage_col]
    .sum()
    .reset_index()
    .sort_values(
        usage_col,
        ascending=False
    )
)

st.sidebar.header("설정")

selected_gu = st.sidebar.selectbox(
    "자치구 선택",
    district_usage[district_col].tolist()
)

selected_df = df[
    df[district_col] == selected_gu
]

st.subheader(f"📍 {selected_gu} 와이파이 사용량")

if id_col is not None:

    fig = px.bar(
        selected_df,
        x=id_col,
        y=usage_col,
        title=f"{selected_gu} AP별 사용량"
    )

    fig.update_layout(
        height=500,
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.markdown("---")

st.subheader("🏆 사용량 TOP 10 자치구")

top10 = (
    district_usage
    .head(10)
    .sort_values(
        usage_col,
        ascending=True
    )
)

fig2 = px.bar(
    top10,
    x=usage_col,
    y=district_col,
    orientation="h",
    text_auto=".2s",
    title="TOP 10 자치구"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.dataframe(
    top10,
    use_container_width=True
)

st.markdown("---")

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
