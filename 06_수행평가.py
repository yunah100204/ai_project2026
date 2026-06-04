import streamlit as st
import pandas as pd
import plotly.express as px
import zipfile
import io

st.set_page_config(
    page_title="Seoul Public WiFi Analysis",
    page_icon="📶",
    layout="wide"
)

st.title("📶 Seoul Public WiFi Usage Analysis")

ZIP_FILE = "서울특별시_공공와이파이 AP별 사용량_10_13_2021(1).zip"


@st.cache_data
def load_data():
    with zipfile.ZipFile(ZIP_FILE) as z:

        target_file = None

        for file in z.namelist():
            if "관리번호" not in file:
                target_file = file

        for file in z.namelist():
            data = z.read(file)

            try:
                df = pd.read_csv(io.BytesIO(data), encoding="cp949")

                if "자치구" in df.columns:
                    return df

            except Exception:
                continue

    return None


df = load_data()

if df is None:
    st.error("Data file could not be loaded.")
    st.stop()

df["AP별 이용량(GB)"] = pd.to_numeric(
    df["AP별 이용량(GB)"],
    errors="coerce"
)

# 자치구 선택
districts = sorted(df["자치구"].dropna().unique())

selected_gu = st.selectbox(
    "Select District",
    districts
)

filtered = df[df["자치구"] == selected_gu]

st.subheader(f"{selected_gu} WiFi Usage")

fig = px.bar(
    filtered.sort_values("AP별 이용량(GB)", ascending=False).head(30),
    x="관리번호",
    y="AP별 이용량(GB)",
    title=f"{selected_gu} Top AP Usage",
)

fig.update_layout(
    xaxis_title="AP ID",
    yaxis_title="Usage (GB)"
)

st.plotly_chart(fig, use_container_width=True)

# TOP10 자치구
st.subheader("Top 10 Districts by Total Usage")

top10 = (
    df.groupby("자치구")["AP별 이용량(GB)"]
    .sum()
    .reset_index()
    .sort_values("AP별 이용량(GB)", ascending=False)
    .head(10)
)

top10["Rank"] = range(1, len(top10) + 1)

st.dataframe(
    top10[["Rank", "자치구", "AP별 이용량(GB)"]],
    use_container_width=True
)

fig2 = px.bar(
    top10,
    x="자치구",
    y="AP별 이용량(GB)",
    title="Top 10 Districts"
)

st.plotly_chart(fig2, use_container_width=True)
