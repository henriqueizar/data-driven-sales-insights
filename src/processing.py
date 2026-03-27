import pandas as pd


def load_data(file_path: str) -> pd.DataFrame:
    df = pd.read_excel(file_path)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # name standard
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    def _fmt_date(date): #format date with different formats
        for fmt in ("%d/%m/%Y", "%d/%m/%y", "%Y-%m-%d", "%Y/%m/%d", "%d-%m-%Y"):
            try:
                return pd.to_datetime(date, format=fmt)
            except Exception:
                pass
        return pd.NaT #if no format matches, return "null"
    # data conversion ( tries different formats)
    df["date"] = df["date"].apply(_fmt_date)

    # remove invalid lines
    df = df.dropna(subset=["date", "product", "quantity", "unit_price", "city"])

    # padronizing texts
    df["product"] = df["product"].str.strip().str.lower()
    df["city"] = df["city"].str.strip().str.lower()
    # Capitalizing text
    df["product"] = df["product"].str.title()
    df["city"] = df["city"].str.title()
    df["category"] = df["category"].str.title()

    # converting data types
    df["quantity"] = df["quantity"].astype(int)
    df["unit_price"] = df["unit_price"].astype(float)
    return df