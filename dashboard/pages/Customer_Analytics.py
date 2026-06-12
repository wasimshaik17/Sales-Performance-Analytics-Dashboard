import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("🔐 Please login from the main dashboard first.")
    st.stop()

import streamlit as st
import pandas as pd
import os
import plotly.express as px

st.set_page_config(page_title='Customer Analytics', page_icon='👥', layout='wide')

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

st.title('👥 Customer Analytics Dashboard')
st.markdown('Analyze customer behavior, sales contribution, and segmentation.')

# KPI SECTION
customer_count = df['Customer ID'].nunique()
order_count = df['Order ID'].nunique()
avg_order_value = df['Sales'].sum() / order_count

c1, c2, c3 = st.columns(3)

c1.metric('Customers', customer_count)
c2.metric('Orders', order_count)
c3.metric('Avg Order Value', f'${avg_order_value:,.2f}')

# TOP CUSTOMERS
st.subheader('🏆 Top 10 Customers by Sales')

top_customers = (
    df.groupby('Customer Name')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

st.dataframe(top_customers)

fig = px.bar(
    top_customers,
    x='Customer Name',
    y='Sales',
    title='Top Customers by Sales'
)

st.plotly_chart(fig, use_container_width=True)

# CUSTOMER SEGMENT ANALYSIS
st.subheader('📊 Customer Segment Analysis')

segment_sales = (
    df.groupby('Segment')['Sales']
    .sum()
    .reset_index()
)

fig2 = px.pie(
    segment_sales,
    names='Segment',
    values='Sales',
    title='Sales Contribution by Segment'
)

st.plotly_chart(fig2, use_container_width=True)

# CUSTOMER LIFETIME VALUE
st.subheader('💰 Customer Lifetime Value (CLV)')

clv = (
    df.groupby('Customer Name')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(20)
)

st.dataframe(clv)

# RFM PREVIEW
st.subheader('⭐ RFM Segmentation Preview')

rfm = (
    df.groupby('Customer Name')
    .agg({
        'Sales': 'sum',
        'Order ID': 'nunique'
    })
    .rename(columns={
        'Sales': 'Monetary',
        'Order ID': 'Frequency'
    })
)

rfm['Segment'] = 'Regular'
rfm.loc[rfm['Monetary'] > rfm['Monetary'].quantile(0.8), 'Segment'] = 'Champion'

st.dataframe(rfm.head(20))