import streamlit as st

# ----------------------------------
# LOGIN SYSTEM
# ----------------------------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.set_page_config(
        page_title="Login",
        page_icon="🔐",
        layout="centered"
    )

    st.title("🔐 Sales Analytics Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == "admin" and password == "admin123":
            st.session_state.logged_in = True
            st.success("Login Successful")
            st.rerun()
        else:
            st.error("Invalid Username or Password")

    st.stop()

import pandas as pd
import matplotlib.pyplot as plt
import os
import numpy as np

try:
    import plotly.express as px
except ImportError:
    px = None

try:
    from sklearn.linear_model import LinearRegression
except ImportError:
    LinearRegression = None

# ----------------------------------
# PAGE CONFIG
# ----------------------------------

st.set_page_config(
    page_title="Sales Performance Dashboard",
    page_icon="📊",
    layout="wide"
)

st.markdown(
    """
    <style>
    .stMetric {
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------------------
# LOAD DATA
# ----------------------------------

@st.cache_data
def load_data():

    file_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "data",
        "Sample - Superstore.csv"
    )

    df = pd.read_csv(
        file_path,
        encoding="latin1"
    )

    df["Order Date"] = pd.to_datetime(df["Order Date"])

    return df

df = load_data()

# ----------------------------------
# TITLE
# ----------------------------------

st.title("📊 Sales Performance Analytics Dashboard")
st.markdown("---")

# Executive Dashboard Tabs
summary_tab, analytics_tab, forecast_tab = st.tabs(
    ["📈 Executive Summary", "📊 Analytics", "🤖 Forecasting"]
)

# ----------------------------------
# SIDEBAR
# ----------------------------------

if st.sidebar.button("🚪 Logout"):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.header("Dashboard Filters")

selected_region = st.sidebar.multiselect(
    "Select Region",
    options=df["Region"].unique(),
    default=df["Region"].unique()
)

selected_category = st.sidebar.multiselect(
    "Select Category",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

selected_segment = st.sidebar.multiselect(
    "Select Segment",
    options=df["Segment"].unique(),
    default=df["Segment"].unique()
)

# ----------------------------------
# YEAR FILTER
# ----------------------------------
selected_year = st.sidebar.selectbox(
    "Select Year",
    sorted(df["Order Date"].dt.year.unique())
)

min_date = df["Order Date"].min()
max_date = df["Order Date"].max()

selected_dates = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date)
)

# ----------------------------------
# FILTER DATA
# ----------------------------------

filtered_df = df[
    (df["Region"].isin(selected_region))
    &
    (df["Category"].isin(selected_category))
    &
    (df["Segment"].isin(selected_segment))
    &
    (df["Order Date"].dt.year == selected_year)
]

if len(selected_dates) == 2:
    start_date, end_date = selected_dates
    filtered_df = filtered_df[
        (filtered_df["Order Date"] >= pd.to_datetime(start_date))
        &
        (filtered_df["Order Date"] <= pd.to_datetime(end_date))
    ]

# ----------------------------------
# KPI SECTION
# ----------------------------------

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_customers = filtered_df["Customer ID"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Sales",
    f"${total_sales:,.0f}"
)

col2.metric(
    "Total Profit",
    f"${total_profit:,.0f}"
)

col3.metric(
    "Orders",
    total_orders
)

col4.metric(
    "Customers",
    total_customers
)

st.info(
    "Interactive dashboard with filtering, forecasting, customer insights and downloadable reports."
)

st.markdown("---")

# ----------------------------------
# BUSINESS INSIGHTS
# ----------------------------------
st.subheader("📊 Business Insights")

if not filtered_df.empty:
    st.success(
        f"Top Region: {filtered_df.groupby('Region')['Sales'].sum().idxmax()}"
    )

    st.success(
        f"Top Category: {filtered_df.groupby('Category')['Sales'].sum().idxmax()}"
    )

st.markdown("---")

# ----------------------------------
# MONTHLY SALES TREND
# ----------------------------------

st.subheader("📈 Monthly Sales Trend")

filtered_df["Month"] = (
    filtered_df["Order Date"].dt.month
)

monthly_sales = (
    filtered_df.groupby("Month")["Sales"]
    .sum()
)

fig, ax = plt.subplots()

monthly_sales.plot(
    marker="o",
    ax=ax
)

ax.set_title("Monthly Sales Trend")
ax.set_xlabel("Month")
ax.set_ylabel("Sales")

st.pyplot(fig)

st.subheader("⚡ Interactive Monthly Sales Trend")

plotly_df = monthly_sales.reset_index()
plotly_df.columns = ["Month", "Sales"]

fig_plotly = px.line(
    plotly_df,
    x="Month",
    y="Sales",
    markers=True,
    title="Interactive Monthly Sales"
)

st.plotly_chart(fig_plotly, use_container_width=True)

# ----------------------------------
# REGION SALES
# ----------------------------------

st.subheader("🌎 Region Wise Sales")

region_sales = (
    filtered_df.groupby("Region")["Sales"]
    .sum()
)

fig, ax = plt.subplots()

region_sales.plot(
    kind="bar",
    ax=ax
)

ax.set_title("Region Wise Sales")

st.pyplot(fig)

# ----------------------------------
# CATEGORY SALES
# ----------------------------------

st.subheader("🛒 Category Wise Sales")

category_sales = (
    filtered_df.groupby("Category")["Sales"]
    .sum()
)

fig, ax = plt.subplots()

category_sales.plot(
    kind="bar",
    ax=ax
)

ax.set_title("Category Sales")

st.pyplot(fig)

# ----------------------------------
# PROFIT BY CATEGORY
# ----------------------------------
st.subheader("💹 Profit by Category")

profit_by_category = (
    filtered_df.groupby("Category")["Profit"]
    .sum()
)

fig, ax = plt.subplots()

profit_by_category.plot(
    kind="bar",
    ax=ax
)

ax.set_title("Profit by Category")

st.pyplot(fig)

# ----------------------------------
# CATEGORY DISTRIBUTION PIE CHART
# ----------------------------------
st.subheader("🥧 Category Distribution")

fig, ax = plt.subplots()

ax.pie(
    category_sales,
    labels=category_sales.index,
    autopct="%1.1f%%"
)

ax.set_title("Category Sales Distribution")

st.pyplot(fig)

# ----------------------------------
# TOP CUSTOMERS
# ----------------------------------

st.subheader("🏆 Top 10 Customers")

top_customers = (
    filtered_df.groupby("Customer Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.dataframe(top_customers)

st.subheader("👥 Customer Segmentation Analysis")

segment_analysis = (
    filtered_df.groupby("Segment")["Sales"]
    .sum()
    .reset_index()
)

fig_segment = px.pie(
    segment_analysis,
    names="Segment",
    values="Sales",
    title="Customer Segment Contribution"
)

st.plotly_chart(fig_segment, use_container_width=True)

# ----------------------------------
# TOP PRODUCTS
# ----------------------------------

st.subheader("📦 Top 10 Products")

top_products = (
    filtered_df.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.dataframe(top_products)

# ----------------------------------
# DOWNLOAD FILTERED DATA
# ----------------------------------

st.subheader("⬇ Download Report")

csv = filtered_df.to_csv(index=False)

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="sales_report.csv",
    mime="text/csv"
)

# ----------------------------------
# QUICK SUMMARY
# ----------------------------------
st.subheader("📈 Quick Summary")

st.write(f"Total Records: {len(filtered_df)}")
st.write(f"Average Sales: ${filtered_df['Sales'].mean():,.2f}")
st.write(f"Average Profit: ${filtered_df['Profit'].mean():,.2f}")

# ----------------------------------
# SALES FORECASTING
# ----------------------------------

st.subheader("🤖 Sales Forecasting")

forecast_df = monthly_sales.reset_index()
forecast_df.columns = ["Month", "Sales"]

if len(forecast_df) > 1:

    if LinearRegression is None:
        st.warning("scikit-learn is not installed. Run: pip install scikit-learn")
    else:
        X = np.array(forecast_df["Month"]).reshape(-1, 1)
        y = forecast_df["Sales"]

        model = LinearRegression()
        model.fit(X, y)

        next_month = np.array([[forecast_df["Month"].max() + 1]])

        prediction = model.predict(next_month)[0]

        st.metric(
            "Predicted Next Month Sales",
            f"${prediction:,.0f}"
        )

# ----------------------------------
# DATA PREVIEW
# ----------------------------------

st.subheader("📋 Dataset Preview")

st.dataframe(filtered_df.head(20))