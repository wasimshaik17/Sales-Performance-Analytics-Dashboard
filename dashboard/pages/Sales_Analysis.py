import streamlit as st
import pandas as pd
import plotly.express as px
import os
import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("🔐 Login Required")
    st.warning("Please login from the main dashboard.")
    st.stop()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("🔐 Please login from the main dashboard first.")
    st.stop()
st.set_page_config(
    page_title='Sales Analysis',
    page_icon='📊',
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

# FILTERS
st.sidebar.header('Filters')

selected_region = st.sidebar.multiselect(
    'Region',
    df['Region'].unique(),
    default=df['Region'].unique()
)

selected_category = st.sidebar.multiselect(
    'Category',
    df['Category'].unique(),
    default=df['Category'].unique()
)

filtered_df = df[
    (df['Region'].isin(selected_region)) &
    (df['Category'].isin(selected_category))
]

# Use filtered data throughout the dashboard
if not filtered_df.empty:
    df = filtered_df

st.title('📊 Sales Analysis Dashboard')
st.markdown('Detailed sales, profit, category, region and shipping performance analysis.')

# KPI SECTION
sales = df['Sales'].sum()
profit = df['Profit'].sum()
quantity = df['Quantity'].sum()
orders = df['Order ID'].nunique()

c1, c2, c3, c4 = st.columns(4)

c1.metric('💰 Total Sales', f'${sales:,.0f}')
c2.metric('📈 Total Profit', f'${profit:,.0f}')
c3.metric('📦 Quantity Sold', quantity)
c4.metric('🧾 Orders', orders)

st.markdown('---')

# PROFIT MARGIN
st.subheader('💹 Profit Margin Analysis')

profit_margin = ((profit / sales) * 100)

st.metric(
    'Overall Profit Margin',
    f'{profit_margin:.2f}%'
)

st.subheader('📊 Sales vs Profit Overview')

comparison_df = pd.DataFrame({
    'Metric': ['Sales', 'Profit'],
    'Value': [sales, profit]
})

fig_compare = px.bar(
    comparison_df,
    x='Metric',
    y='Value',
    title='Sales vs Profit'
)

st.plotly_chart(fig_compare, use_container_width=True)

# MONTHLY SALES
st.subheader('📈 Monthly Sales Trend')

monthly_sales = (
    df.resample('M', on='Order Date')['Sales']
    .sum()
    .reset_index()
)

fig_monthly = px.line(
    monthly_sales,
    x='Order Date',
    y='Sales',
    markers=True,
    title='Monthly Sales Trend'
)

st.plotly_chart(fig_monthly, use_container_width=True)

# REGION ANALYSIS
left, right = st.columns(2)

with left:
    st.subheader('🌍 Region Wise Sales')

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

    st.subheader('💰 Region Wise Profit')

    region_profit = (
        df.groupby('Region')['Profit']
        .sum()
        .reset_index()
    )

    fig_profit = px.bar(
        region_profit,
        x='Region',
        y='Profit',
        title='Profit by Region'
    )

    st.plotly_chart(fig_profit, use_container_width=True)

with right:
    st.subheader('🛒 Category Sales')

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

# SHIP MODE ANALYSIS
st.subheader('🚚 Ship Mode Performance')

ship_mode = (
    df.groupby('Ship Mode')['Sales']
    .sum()
    .reset_index()
)

fig_ship = px.bar(
    ship_mode,
    x='Ship Mode',
    y='Sales',
    color='Sales',
    title='Sales by Ship Mode'
)

st.plotly_chart(fig_ship, use_container_width=True)

# SUB-CATEGORY ANALYSIS
st.subheader('📦 Top Sub-Categories')

sub_category = (
    df.groupby('Sub-Category')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_sub = px.bar(
    sub_category,
    x='Sub-Category',
    y='Sales',
    title='Top 10 Sub-Categories'
)

st.plotly_chart(fig_sub, use_container_width=True)

# TOP PRODUCTS
st.subheader('🏆 Top 10 Products')

products = (
    df.groupby('Product Name')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

st.dataframe(products, use_container_width=True)

# DOWNLOAD REPORT
csv = df.to_csv(index=False)

st.download_button(
    '⬇ Download Sales Report',
    csv,
    'sales_analysis_report.csv',
    'text/csv'
)

st.subheader('📌 Key Business Insights')

best_region = df.groupby('Region')['Sales'].sum().idxmax()
best_category = df.groupby('Category')['Sales'].sum().idxmax()

st.info(f'Highest Sales Region: {best_region}')
st.info(f'Best Performing Category: {best_category}')

st.success('Sales Analysis Completed Successfully')
