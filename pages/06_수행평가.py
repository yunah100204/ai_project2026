@st.cache_data
def load_data():

    import os
    import zipfile
    import pandas as pd

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

                cols = df.columns.tolist()

                if (
                    "관리번호" in cols
                    and "자치구" in cols
                    and any("이용량" in c for c in cols)
                ):
                    return df

            except Exception:
                continue

    st.error("Valid data file not found in ZIP.")
    st.stop()
