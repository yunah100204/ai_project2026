import streamlit as st
import pandas as pd
import plotly.express as px
import zipfile
import os

st.set_page_config(
    page_title="Seoul Public WiFi Usage",
    page_icon="📶",
    layout="wide"
)

st.title("📶 Seoul Public WiFi Usage Analysis")

@st.cache_data
def load_data():

    zip_files = [f for f in os.listdir(".") if f.endswith(".zip")]

    if not zip_files:
        st.error("ZIP file not found.")
        st.stop()

    with zipfile.ZipFile(zip_files[0], "r") as z:

        for filename in z.namelist():

            try:
                df = pd.read_csv(
                    z.open(filename),
                    encoding="cp949"
                )

                if (
                    "관리번호" in df.columns
                    and "자치구" in df.columns
                ):
                    return df

            except Exception:
                continue

    st.error("No valid data found.")
    st.stop()

df = load_data()

usage_col = [c for c in df.columns if "이용량" in c][0]

df[usage_col] = pd.to_numeric(df[usage_col], errors="coerce")
df = df.dropna(subset=[usage_col])

districts = sorted(df["자치구"].dropna().unique())

selected_gu = st.selectbox(
    "Select District",
    districts
)

filtered = df[df["자치구"] == selected_gu]

fig = px.bar(
    filtered.sort_values(usage_col, ascending=False).head(30),
    x="관리번호",
    y=usage_col,
    title=f"{selected_gu} Top 30 AP Usage"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Top 10 Districts")

top10 = (
    df.groupby("자치구")[usage_col]
    .sum()
    .reset_index()
    .sort_values(usage_col, ascending=False)
    .head(10)
)

top10["Rank"] = range(1, len(top10) + 1)

st.dataframe(top10, use_container_width=True)

fig2 = px.bar(
    top10,
    x="자치구",
    y=usage_col,
    text_auto=True
)

st.plotly_chart(fig2, use_container_width=True)
