import streamlit as st
import pandas as pd
import plotly.express as px
import zipfile

st.set_page_config(
    page_title="Seoul Public WiFi Analysis",
    page_icon="📶",
    layout="wide"
)

st.title("📶 Seoul Public WiFi Usage Analysis")

@st.cache_data
def load_data():

    with zipfile.ZipFile(
        "서울특별시_공공와이파이 AP별 사용량_10_13_2021.zip"
    ) as z:

        csv_files = [
            f for f in z.namelist()
            if f.lower().endswith(".csv")
        ]

        if not csv_files:
            st.stop()

        df = None

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

selected_gu = st.sidebar.selectbox(
    "District",
    district_usage[district_col]
)

selected_df = df[
    df[district_col] == selected_gu
]

st.subheader(selected_gu)

if id_col is not None:

    fig = px.bar(
        selected_df,
        x=id_col,
        y=usage_col,
        title=f"{selected_gu} AP Usage"
    )

    fig.update_layout(
        height=500,
        xaxis_tickangle=-45
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.subheader("Top 10 Districts")

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
