import pandas as pd


def analyze_sales(df: pd.DataFrame):

    sales_by_product = (
    df.groupby("product")["revenue"]
    .sum()
    .sort_values(ascending=False)
    )
    sales_by_city = (
    df.groupby("city")["revenue"]
    .sum()
    .sort_values(ascending=False)
    )
    sales_by_month = (
    df.groupby("month")["revenue"]
    .sum()
    .sort_values()
    )
    sales_by_category = (
    df.groupby("category")["revenue"]
    .sum()
    .sort_values(ascending=False)
    )
    
    #top sales
    top_revenue = sales_by_product.idxmax()
    top_revenue_share = sales_by_product.max() / sales_by_product.sum()
    #new metrics: profit and margin
    df["profit"] = (df["unit_price"] - df["cost_per_unit"]) * df["quantity"]
    df["margin"] = (df["unit_price"] - df["cost_per_unit"]) / df["unit_price"]
    top_profit_product = df.groupby("product")["profit"].sum().idxmax()
    best_margin = df.groupby("product")["margin"].mean().idxmax()

    #top sales city
    top_city = sales_by_city.idxmax()

    #top sales category
    top_category = sales_by_category.idxmax()

    growth = sales_by_month.pct_change().mean()

    top_city_share = sales_by_city.max() / sales_by_city.sum()


    total_revenue = df["revenue"].sum()
    total_profit = df["profit"].sum()

    #volume insights
    top_volume_product = df.groupby("product")["quantity"].sum().idxmax()
    top_volume = df.groupby("product")["quantity"].sum().max()

    least_profitable = df.groupby("product")["profit"].sum().idxmin()


    print(f"Total revenue is {total_revenue:.2f}, generating a total profit of {total_profit:.2f}.")

    print(f"{top_revenue} generates the highest revenue, accounting for {top_revenue_share:.1%} of total sales.")

    if top_revenue != top_profit_product:
        print(f"However, {top_profit_product} is the most profitable product, indicating a gap between revenue and profitability.")
    else:
        print(f"{top_revenue} is also the most profitable product.")

    print(f"{top_volume_product} is the most sold product with {top_volume} units.")

    if top_volume_product != top_profit_product:
        print(f"Despite high sales volume, {top_volume_product} is not the most profitable product, which is {top_profit_product}")

    print(f"{top_city} leads revenue generation, contributing {top_city_share:.1%} of total sales.")
    print(f"{top_category} is the main category revenue driver.")

    print(f"{least_profitable} is the least profitable product, and requires attention.")

    if growth > 0:
        print("Sales show an upward trend over time.")
    else:
        print("Sales are declining or unstable over time.")

    return ;