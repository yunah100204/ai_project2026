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

# 컬럼 확인용
st.sidebar.subheader("데이터 정보")
st.sidebar.write(df.shape)

# 실제 데이터에 맞게 수정
district_col = "자치구"
usage_col = "사용량"

district_usage = (
    df.groupby(district_col)[usage_col]
    .sum()
    .reset_index()
    .sort_values(
        usage_col,
        ascending=False
    )
)

selected_gu = st.sidebar.selectbox(
    "자치구 선택",
    district_usage[district_col]
)

selected_df = df[
    df[district_col] == selected_gu
]

st.subheader(f"📍 {selected_gu}")

fig = px.bar(
    selected_df,
    x="관리번호",
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
