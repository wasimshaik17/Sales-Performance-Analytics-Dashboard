import streamlit as st
import pandas as pd
import plotly.express as px
import os
import numpy as np
import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.warning("🔐 Please login from the main dashboard first.")
    st.stop()

try:
    from sklearn.linear_model import LinearRegression
except ImportError:
    LinearRegression = None

st.set_page_config(
    page_title='Sales Forecasting',
    page_icon='🤖',
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

st.title('🤖 Sales Forecasting Dashboard')
st.markdown('Machine Learning based sales trend analysis and future sales prediction.')

# PREPARE MONTHLY DATA
monthly_sales = (
    df.groupby(
        pd.Grouper(
            key='Order Date',
            freq='ME'
        )
    )['Sales']
    .sum()
    .reset_index()
)

monthly_sales['Month_Number'] = range(1, len(monthly_sales) + 1)

st.subheader('📈 Historical Monthly Sales')

fig = px.line(
    monthly_sales,
    x='Order Date',
    y='Sales',
    markers=True,
    title='Monthly Sales Trend'
)

st.plotly_chart(fig, use_container_width=True)

if LinearRegression is None:
    st.warning('Install scikit-learn using: pip install scikit-learn')
else:

    X = monthly_sales[['Month_Number']]
    y = monthly_sales['Sales']

    model = LinearRegression()
    model.fit(X, y)

    future_months = 6

    future_x = np.arange(
        len(monthly_sales) + 1,
        len(monthly_sales) + future_months + 1
    ).reshape(-1, 1)

    predictions = model.predict(future_x)

    future_dates = pd.date_range(
        monthly_sales['Order Date'].max(),
        periods=future_months + 1,
        freq='ME'
    )[1:]

    forecast_df = pd.DataFrame({
        'Order Date': future_dates,
        'Forecast Sales': predictions
    })

    st.subheader('🔮 Next 6 Months Forecast')

    st.dataframe(forecast_df, use_container_width=True)

    forecast_chart = px.line(
        forecast_df,
        x='Order Date',
        y='Forecast Sales',
        markers=True,
        title='Forecasted Sales'
    )

    st.plotly_chart(forecast_chart, use_container_width=True)

    st.metric(
        'Predicted Next Month Sales',
        f"${predictions[0]:,.0f}"
    )

    combined_actual = monthly_sales[['Order Date', 'Sales']].copy()
    combined_actual['Type'] = 'Actual'

    combined_forecast = forecast_df.rename(
        columns={'Forecast Sales': 'Sales'}
    )
    combined_forecast['Type'] = 'Forecast'

    combined = pd.concat(
        [combined_actual, combined_forecast],
        ignore_index=True
    )

    st.subheader('📊 Actual vs Forecast')

    combined_chart = px.line(
        combined,
        x='Order Date',
        y='Sales',
        color='Type',
        markers=True,
        title='Actual vs Forecast Sales'
    )

    st.plotly_chart(combined_chart, use_container_width=True)

st.info('This forecast uses Linear Regression for educational and portfolio purposes.')