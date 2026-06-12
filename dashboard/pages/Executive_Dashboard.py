import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("🔐 Please login from the main dashboard first.")
    st.stop()

import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(
    page_title='Executive Dashboard',
    page_icon='📈',
    layout='wide'
)

@st.cache_data
def load_data():
    file_path = os.path.join(
        os.path.dirname(__file__),
        '..',
        '..',
        'data',
        'Sample - Superstore.csv'
    )

    df = pd.read_csv(file_path, encoding='latin1')
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    return df


df = load_data()

st.title('📈 Executive Business Dashboard')
st.markdown('High-level business performance overview for management and stakeholders.')

# KPI CARDS
sales = df['Sales'].sum()
profit = df['Profit'].sum()
orders = df['Order ID'].nunique()
customers = df['Customer ID'].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric('💰 Total Sales', f'${sales:,.0f}')
c2.metric('📈 Total Profit', f'${profit:,.0f}')
c3.metric('📦 Orders', orders)
c4.metric('👥 Customers', customers)

st.markdown('---')

# MONTHLY TREND
st.subheader('📊 Monthly Sales Trend')

df['Month-Year'] = df['Order Date'].dt.strftime('%Y-%m')
monthly_sales = df.groupby('Month-Year')['Sales'].sum().reset_index()

fig = px.line(
    monthly_sales,
    x='Month-Year',
    y='Sales',
    markers=True,
    title='Monthly Sales Performance'
)

st.plotly_chart(fig, use_container_width=True)

# REGION ANALYSIS
left, right = st.columns(2)

with left:
    st.subheader('🌍 Region Performance')

    region_sales = (
        df.groupby('Region')['Sales']
        .sum()
        .reset_index()
    )

    fig_region = px.bar(
        region_sales,
        x='Region',
        y='Sales',
        title='Sales by Region'
    )

    st.plotly_chart(fig_region, use_container_width=True)

with right:
    st.subheader('🛒 Category Performance')

    category_sales = (
        df.groupby('Category')['Sales']
        .sum()
        .reset_index()
    )

    fig_category = px.pie(
        category_sales,
        names='Category',
        values='Sales',
        title='Category Contribution'
    )

    st.plotly_chart(fig_category, use_container_width=True)

# EXECUTIVE INSIGHTS
st.subheader('🎯 Executive Insights')

best_region = df.groupby('Region')['Sales'].sum().idxmax()
best_category = df.groupby('Category')['Sales'].sum().idxmax()
best_customer = df.groupby('Customer Name')['Sales'].sum().idxmax()

st.success(f'Top Performing Region: {best_region}')
st.success(f'Top Selling Category: {best_category}')
st.success(f'Most Valuable Customer: {best_customer}')

# TOP PRODUCTS
st.subheader('🏆 Top 10 Products')

top_products = (
    df.groupby('Product Name')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

st.dataframe(top_products, use_container_width=True)

# DOWNLOAD REPORT
csv = df.to_csv(index=False)

st.download_button(
    label='⬇ Download Executive Report',
    data=csv,
    file_name='executive_report.csv',
    mime='text/csv'
)