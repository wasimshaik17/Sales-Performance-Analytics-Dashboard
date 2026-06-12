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
    page_title='RFM Analysis',
    page_icon='⭐',
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

st.title('⭐ RFM Customer Segmentation Dashboard')
st.markdown('Recency • Frequency • Monetary Analysis for customer segmentation.')

# REFERENCE DATE
snapshot_date = df['Order Date'].max() + pd.Timedelta(days=1)

# RFM CALCULATION
rfm = (
    df.groupby('Customer Name')
    .agg({
        'Order Date': lambda x: (snapshot_date - x.max()).days,
        'Order ID': 'nunique',
        'Sales': 'sum'
    })
)

rfm.columns = ['Recency', 'Frequency', 'Monetary']

# RFM SCORES
rfm['R_Score'] = pd.qcut(
    rfm['Recency'],
    4,
    labels=[4, 3, 2, 1]
)

rfm['F_Score'] = pd.qcut(
    rfm['Frequency'].rank(method='first'),
    4,
    labels=[1, 2, 3, 4]
)

rfm['M_Score'] = pd.qcut(
    rfm['Monetary'],
    4,
    labels=[1, 2, 3, 4]
)

rfm['RFM_Score'] = (
    rfm['R_Score'].astype(str)
    + rfm['F_Score'].astype(str)
    + rfm['M_Score'].astype(str)
)

# SEGMENTATION
rfm['Segment'] = 'Regular Customers'

rfm.loc[
    (rfm['R_Score'].astype(int) >= 4)
    &
    (rfm['F_Score'].astype(int) >= 4),
    'Segment'
] = 'Champions'

rfm.loc[
    (rfm['R_Score'].astype(int) >= 3)
    &
    (rfm['F_Score'].astype(int) >= 3),
    'Segment'
] = 'Loyal Customers'

rfm.loc[
    (rfm['R_Score'].astype(int) <= 2)
    &
    (rfm['F_Score'].astype(int) <= 2),
    'Segment'
] = 'At Risk'

# KPIs
c1, c2, c3, c4 = st.columns(4)

c1.metric('Customers', len(rfm))
c2.metric('Champions', (rfm['Segment'] == 'Champions').sum())
c3.metric('Loyal', (rfm['Segment'] == 'Loyal Customers').sum())
c4.metric('At Risk', (rfm['Segment'] == 'At Risk').sum())

st.markdown('---')

# SEGMENT DISTRIBUTION
st.subheader('📊 Customer Segment Distribution')

segment_count = (
    rfm['Segment']
    .value_counts()
    .reset_index()
)

segment_count.columns = ['Segment', 'Count']

fig = px.pie(
    segment_count,
    names='Segment',
    values='Count',
    title='RFM Segment Distribution'
)

st.plotly_chart(fig, use_container_width=True)

# MONETARY ANALYSIS
st.subheader('💰 Revenue Contribution by Segment')

segment_revenue = (
    rfm.groupby('Segment')['Monetary']
    .sum()
    .reset_index()
)

fig2 = px.bar(
    segment_revenue,
    x='Segment',
    y='Monetary',
    title='Revenue by Customer Segment'
)

st.plotly_chart(fig2, use_container_width=True)

# TOP CUSTOMERS
st.subheader('🏆 Top Customers by Monetary Value')

st.dataframe(
    rfm.sort_values(
        by='Monetary',
        ascending=False
    ).head(20),
    use_container_width=True
)

# RFM TABLE
st.subheader('📋 Complete RFM Table')

st.dataframe(
    rfm.reset_index(),
    use_container_width=True
)

# DOWNLOAD
csv = rfm.reset_index().to_csv(index=False)

st.download_button(
    '⬇ Download RFM Report',
    csv,
    'rfm_analysis.csv',
    'text/csv'
)

st.success('RFM Segmentation Completed Successfully')