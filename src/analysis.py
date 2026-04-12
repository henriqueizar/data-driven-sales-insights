def analyze_sales(df):
    # main kpis
    total_revenue = df["revenue"].sum()
    total_profit = df["profit"].sum()

    # data for charts
    revenue_by_product = df.groupby("product")["revenue"].sum()
    profit_by_product = df.groupby("product")["profit"].sum()
    revenue_by_month = df.groupby("month")["revenue"].sum()
    revenue_by_city = df.groupby("city")["revenue"].sum()
    quantity_by_product = df.groupby("product")["quantity"].sum()

    # data for insights
    top_revenue_product = revenue_by_product.idxmax()
    top_revenue_share = revenue_by_product.max() / total_revenue

    top_profit_product = profit_by_product.idxmax()

    top_volume_product = quantity_by_product.idxmax()
    top_volume = quantity_by_product.max()

    top_city = revenue_by_city.idxmax()
    top_city_share = revenue_by_city.max() / total_revenue

    top_category = df.groupby("category")["revenue"].sum().idxmax()

    least_profitable_product = profit_by_product.idxmin()

    growth = revenue_by_month.pct_change().mean()

    # insight texts to print
    insights = []

    insights.append(f"Total revenue is **R${total_revenue:.2f}**, generating a total profit of **R${total_profit:.2f}**.")
    insights.append(f"**{top_revenue_product}** generates the highest revenue, accounting for **{top_revenue_share:.1%}** of total sales.")

    if top_revenue_product != top_profit_product:
        insights.append(f"However, **{top_profit_product}** is the **most profitable** product, indicating a gap between revenue and profitability.")
    else:
        insights.append(f"**{top_revenue_product}** is also the most profitable product.")

    insights.append(f"**{top_volume_product}** is the most sold product with **{top_volume}** units.")

    if top_volume_product != top_profit_product:
        insights.append(f"Despite high sales volume, **{top_volume_product}** is not the most profitable product, which is **{top_profit_product}**.")

    insights.append(f"**{top_city}** leads revenue generation, contributing **{top_city_share:.1%}** of total sales.")
    insights.append(f"**{top_category}** is the main category revenue driver.")
    insights.append(f"**{least_profitable_product}** is the least profitable product and requires attention.")
    if growth > 0:
        insights.append("Sales show an upward trend over time.")
    else:
        insights.append("Sales are declining or unstable over time.")

    #better to return structured data, for organization and future escalability
    return {
        "kpis": {
            "total_revenue": total_revenue,
            "total_profit": total_profit
        },
        "charts": {
            "revenue_by_product": revenue_by_product,
            "profit_by_product": profit_by_product,
            "revenue_by_month": revenue_by_month,
            "revenue_by_city": revenue_by_city,
            "quantity_by_product": quantity_by_product
        },
        "insights": insights
    }