import pandas as pd
import unicodedata
from thefuzz import process


def load_data(file_path: str) -> pd.DataFrame:
    df = pd.read_excel(file_path)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # column name standard
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
    df = df.dropna(subset=["date", "product", "quantity", "unit_price", "cost_per_unit", "city"])

  
    #fuzz matching - chooses the most similar string from the list:
    cities_list = ["Brasília", "Goiânia", "São Paulo", "Salvador"]
    categories_list = ["Beer", "Soda", "Water", "Juice", "Energy Drink"]
    products_list = ["Guaraná", "IPA", "Amstel","Indaiá", "Original","Cajuína", "Orange Juice", "Redbull", "Monster"]


    threshold = 60 #threshold for not matching random strings

    def clean_category(category):
        if pd.isna(category):
            return None
        match, score = process.extractOne(category, categories_list)
        return match if score >= threshold else None
    def clean_product(product):
        if pd.isna(product):
            return None
        match, score = process.extractOne(product, products_list)
        return match if score >= threshold else None
    
    def clean_city(city):
        if pd.isna(city):
            return None
        match, score = process.extractOne(city, cities_list)
        return match if score >= threshold else None

    df["city_clean"] = df["city"].apply(clean_city)
    df["category_clean"] = df["category"].apply(clean_category)
    df["product_clean"] = df["product"].apply(clean_product)

    #----------- replace original columns with cleaned ones
    df["city"] = df["city_clean"]
    df["category"] = df["category_clean"]
    df["product"] = df["product_clean"]

    df = df.drop(columns=["city_clean", "category_clean", "product_clean"])

    #new columns for better insights
    df["revenue"] = df["quantity"] * df["unit_price"]
    df["month"] = df["date"].dt.to_period("M")


    


    return df