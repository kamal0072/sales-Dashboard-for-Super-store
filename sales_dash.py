import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Sales Dashboard",
    page_icon=":bar_chart:",
    layout="wide",
)
st.title("Sales Dashboard")
st.markdown(
    """
        ----Sales Dashboard----
    """
)

# Load dataset
def load_data():
    df = pd.read_csv('Superstore.csv', encoding='latin-1')

    df["Order Date"] = pd.to_datetime(df["Order Date"])

    df["Year"] = df["Order Date"].dt.year

    df["Month"] = df["Order Date"].dt.month_name()

    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")


# Year Filter
years = sorted(df['Year'].unique())
selected_year = st.sidebar.multiselect(
    "Select Year",
    years,
    default=years
)

# Region Filter
regions = df['Region'].unique()
selected_region = st.sidebar.multiselect(
    "Region",
    regions,
    default=regions
)

# Category Filter
categories = df['Category'].unique()
selected_category = st.sidebar.multiselect(
    "Select Category",
    categories,
    default=categories[1]
)

# Apply Filters
filtered_df = df[
    (df['Year']).isin(selected_year) 
    &
    (df['Region']).isin(selected_region)
    &
    (df['Category']).isin(selected_category)
]

# KPI Cards
# Calculate KPIs
total_sales = filtered_df['Sales'].sum()
total_profit = filtered_df['Profit'].sum()
total_orders = filtered_df["Order ID"].nunique()
total_customers = filtered_df["Customer ID"].nunique()


# Display KPI Cards
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(
        "Total Sales",
        f"${total_sales:,.2f}"
    )


with col2:
    st.metric(
        "Total Profit",
        f"${total_profit:,.2f}"
    )

with col3:
    st.metric(
        "Orders",
        total_orders
    )

with col4:
    st.metric(
        "Customers",
        total_customers
    )

# Monthly Sales Trend
monthly_sales = (
    filtered_df
    .groupby("Month")
    ["Sales"]
    .sum()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(
    data=monthly_sales,
    x="Month",
    y="Sales",
    marker="o",
    ax=ax,
    # legend="full"
)
plt.xticks(rotation=45)
st.pyplot(fig)

# Sales by Category
category_sales = (
    filtered_df
    .groupby('Category')
    ['Sales']
    .sum()
    .reset_index()
)

fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(
    data=category_sales,
    x="Category",
    y="Sales",
    ax=ax
)

plt.xticks(rotation=45)
st.pyplot(fig)

# Two Charts Side By Side
# Two Charts Side By Side
col1,col2 = st.columns(2)

with col1:
    profit_data = (
        filtered_df
        .groupby('Category')['Profit']
        .sum().reset_index()
    )
    fig, ax = plt.subplots()
    sns.barplot(
        data=profit_data,
        x="Category",
        y="Profit",
        ax=ax
    )
    st.pyplot(fig)

# Sales by Region
with col2:
    region_data = (
        filtered_df
        .groupby('Region')['Sales']
        .sum()
        .reset_index()
    )
    fig, ax = plt.subplots()
    sns.barplot(
        data=region_data,
        x="Region",
        y="Sales",
        ax=ax
    )
    st.pyplot(fig)

# Top 10 Products
top_products = (
    filtered_df
    .groupby('Product Name')['Sales']
    .sum()
    .sort_values( ascending=False)
).head(10)

fig, ax = plt.subplots(figsize=(10,5))
sns.barplot(
    x=top_products.values,
    y=top_products.index,
    ax=ax,
)
st.pyplot(fig)

# # Sales vs Profit
fig, ax = plt.subplots(figsize=(10,5))
sns.scatterplot(
    data=filtered_df,
    x="Sales",
    y="Profit",
    hue="Category",
    ax=ax
)
st.pyplot(fig)

# # Correlation Heatmap
numeric_df = filtered_df.select_dtypes(
    include="number"
)
corr = numeric_df.corr()
fig, ax = plt.subplots(figsize=(8,6))

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    ax=ax
)
st.pyplot(fig)

# Data Table
st.subheader("Sales Data")
st.sidebar.subheader("Data Table")
rows = st.sidebar.slider(
    "Select Number of Rows",
    1,
    filtered_df.shape[0],
    filtered_df.shape[0]
)
st.dataframe(
    filtered_df.head(rows),
    width = "content"
)
st.sidebar.write(filtered_df.head(rows).shape)

# Download CSV button
csv = filtered_df.to_csv(index=False)
st.download_button(
    label="Download CSV",
    data=csv,
    file_name="sales_data.csv",
    mime="text/csv"
)
