
from datetime import datetime

def transform_data(df):
    try:
        df_clean = df.copy()
        df_clean = df_clean.dropna()
        df_clean = df_clean.drop_duplicates()
        df_clean = df_clean[df_clean["title"] != "Unknown Product"]
        df_clean["price"] = (
            df_clean["price"]
            .str.replace("$", "", regex=False)
            .str.strip()
            .astype(float) * 16000
        )
        df_clean = df_clean[~df_clean["rating"].str.contains("Invalid", na=False)]
        df_clean["rating"] = df_clean["rating"].str.extract(r"(\d+\.\d+)").astype(float)
        df_clean["colors"] = (
        df_clean["colors"]
        .astype(str)
        .str.extract(r"(\d+)")
        .squeeze()
        .fillna(0)
        .astype("int64")
        )
        df_clean["size"] = df_clean["size"].str.replace("Size:", "", regex=False).str.strip()
        df_clean["gender"] = df_clean["gender"].str.replace("Gender:", "", regex=False).str.strip()

        df_clean["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        return df_clean

    except Exception as e:
        print(f"Transform error: {e}")
        return None
