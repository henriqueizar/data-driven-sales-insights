import streamlit as st
import pandas as pd
from processing import load_data, clean_data
from analysis import analyze_sales
import plotly.express as px

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon="📊",
    layout="wide"
)


# carregar dados
df = load_data("data/sales.xlsx")
df = clean_data(df)

metrics = analyze_sales(df)


# imports:
# kpis
total_revenue = metrics["kpis"]["total_revenue"]
total_profit = metrics["kpis"]["total_profit"]

#data for charts
quantity_by_product = metrics["charts"]["quantity_by_product"]
revenue_by_product = metrics["charts"]["revenue_by_product"]
profit_by_product = metrics["charts"]["profit_by_product"]
revenue_by_month = metrics["charts"]["revenue_by_month"]
revenue_by_city = metrics["charts"]["revenue_by_city"]

#insights
insights = metrics["insights"]

# title
st.title("Sales Insights Dashboard")

col1, col2 = st.columns(2)

col2.subheader("Sales by Product")
col2.bar_chart(quantity_by_product)

col1.subheader("Profit by Product")
col1.bar_chart(profit_by_product)

#st.line_chart(revenue_by_month) didnt work properly


revenue_by_month = revenue_by_month.reset_index()
revenue_by_month["month"] = revenue_by_month["month"].dt.strftime("%b")

fig = px.line(
    revenue_by_month,
    x="month",
    y="revenue",
    title="Revenue Over Time"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("Revenue Distribution")
col3, col4 = st.columns(2)



category_data = df.groupby("category")["revenue"].sum().reset_index()

fig = px.pie(
    category_data,
    names="category",
    values="revenue",
    title="Revenue Distribution by Category"
)

col3.plotly_chart(fig, use_container_width=True)

fig = px.pie(
    revenue_by_product.reset_index(),
    names="product",
    values="revenue",
    title="Revenue Distribution by Product"
)

col4.plotly_chart(fig, use_container_width=True)


# insights
st.subheader("Insights")
for insight in metrics["insights"]:
    st.write(f"- {insight}")

st.divider()

# dados
st.subheader("Cleaned Data")
st.dataframe(df)