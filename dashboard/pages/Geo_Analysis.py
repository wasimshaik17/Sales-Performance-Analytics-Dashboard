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
    page_title='Geo Analysis',
    page_icon='🌍',
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
    return df


df = load_data()

st.title('🌍 State & City Analysis Dashboard')
st.markdown('Geographical analysis of sales and profit performance.')

# KPI SECTION
sales = df['Sales'].sum()
profit = df['Profit'].sum()
states = df['State'].nunique()
cities = df['City'].nunique()

c1, c2, c3, c4 = st.columns(4)
c1.metric('💰 Total Sales', f'${sales:,.0f}')
c2.metric('📈 Total Profit', f'${profit:,.0f}')
c3.metric('🏛 States', states)
c4.metric('🏙 Cities', cities)

st.markdown('---')

# STATE SALES
st.subheader('🏛 Top States by Sales')

state_sales = (
    df.groupby('State')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
)

fig_state = px.bar(
    state_sales,
    x='State',
    y='Sales',
    title='Top 15 States by Sales'
)

st.plotly_chart(fig_state, use_container_width=True)

# STATE PROFIT
st.subheader('💹 Top States by Profit')

state_profit = (
    df.groupby('State')['Profit']
    .sum()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
)

fig_profit = px.bar(
    state_profit,
    x='State',
    y='Profit',
    title='Top 15 States by Profit'
)

st.plotly_chart(fig_profit, use_container_width=True)

# CITY SALES
st.subheader('🏙 Top Cities by Sales')

city_sales = (
    df.groupby('City')['Sales']
    .sum()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
)

fig_city = px.bar(
    city_sales,
    x='City',
    y='Sales',
    title='Top 15 Cities by Sales'
)

st.plotly_chart(fig_city, use_container_width=True)

# CITY PROFIT
st.subheader('📊 Top Cities by Profit')

city_profit = (
    df.groupby('City')['Profit']
    .sum()
    .sort_values(ascending=False)
    .head(15)
    .reset_index()
)

fig_city_profit = px.bar(
    city_profit,
    x='City',
    y='Profit',
    title='Top 15 Cities by Profit'
)

st.plotly_chart(fig_city_profit, use_container_width=True)

# TABLES
st.subheader('📋 State Sales Summary')
st.dataframe(state_sales, use_container_width=True)

csv = state_sales.to_csv(index=False)

st.download_button(
    '⬇ Download Geo Analysis Report',
    csv,
    'geo_analysis_report.csv',
    'text/csv'
)

st.success('Geo Analysis Completed Successfully')