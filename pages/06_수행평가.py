import streamlit as st
import pandas as pd
import plotly.express as px
import zipfile
import io

st.set_page_config(
    page_title="Seoul Public WiFi Usage",
    page_icon="📶",
    layout="wide"
)

st.title("📶 Seoul Public WiFi Usage Analysis")


@st.cache_data
def load_data():
    zip_path = "서울특별시_공공와이파이 AP별 사용량_10_13_2021(1)(1).zip"

    with zipfile.ZipFile(zip_path, "r") as z:

        for filename in z.namelist():

            try:
                with z.open(filename) as f:
                    df = pd.read_csv(f, encoding="cp949")

                cols = list(df.columns)

                if (
                    "관리번호" in cols
                    and "자치구" in cols
                    and any("이용량" in c for c in cols)
                ):
                    return df

            except Exception:
                continue

    return None


df = load_data()

if df is None:
    st.error("데이터를 읽을 수 없습니다.")
    st.stop()

usage_col = [c for c in df.columns if "이용량" in c][0]

df[usage_col] = pd.to_numeric(df[usage_col], errors="coerce")
df = df.dropna(subset=[usage_col])

st.sidebar.header("Filter")

districts = sorted(df["자치구"].unique())

selected_gu = st.sidebar.selectbox(
    "자치구 선택",
    districts
)

filtered = df[df["자치구"] == selected_gu]

st.subheader(f"{selected_gu} AP 사용량")

fig = px.bar(
    filtered.sort_values(
        usage_col,
        ascending=False
    ).head(30),
    x="관리번호",
    y=usage_col,
    title=f"{selected_gu} Top 30 AP Usage"
)

fig.update_layout(
    xaxis_title="관리번호",
    yaxis_title="Usage (GB)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.divider()

st.subheader("🏆 사용량 TOP 10 자치구")

top10 = (
    df.groupby("자치구")[usage_col]
    .sum()
    .reset_index()
    .sort_values(
        usage_col,
        ascending=False
    )
    .head(10)
)

top10.insert(
    0,
    "순위",
    range(1, len(top10) + 1)
)

st.dataframe(
    top10,
    use_container_width=True
)

fig2 = px.bar(
    top10,
    x="자치구",
    y=usage_col,
    text_auto=".1f",
    title="Top 10 Districts"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)
