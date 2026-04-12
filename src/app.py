import streamlit as st
import pandas as pd
from processing import load_data, clean_data

from analysis import analyze_sales



# carregar dados
df = load_data("data/sales.xlsx")
df = clean_data(df)

metrics = analyze_sales(df)

total_revenue = metrics["total_revenue"]
total_profit = metrics["total_profit"]

# título
st.title("Sales Dashboard")

# métricas principais
col1, col2 = st.columns(2)

col1.metric("Total Revenue", f"{total_revenue:.2f}")
col2.metric("Total Profit", f"{total_profit:.2f}")

# gráfico por produto
st.subheader("Revenue by Product")
revenue_by_product = df.groupby("product")["revenue"].sum()
st.bar_chart(revenue_by_product)

# gráfico por cidade
st.subheader("Revenue by City")
revenue_by_city = df.groupby("city")["revenue"].sum()
st.bar_chart(revenue_by_city)

# tabela
st.subheader("Data")
st.dataframe(df)