@st.cache_data
def load_data():

    with zipfile.ZipFile(
        "서울특별시_공공와이파이 AP별 사용량_10_13_2021.zip"
    ) as z:

        csv_files = [
            f for f in z.namelist()
            if f.endswith(".csv")
        ]

        if len(csv_files) == 0:
            st.error("ZIP 파일 안에 CSV 파일이 없습니다.")
            st.stop()

        with z.open(csv_files[0]) as f:
            df = pd.read_csv(
                f,
                encoding="cp949"
            )

    df.columns = df.columns.str.strip()

    return df
