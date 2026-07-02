import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine


st.set_page_config(
    page_title="NYC Taxi ETL Dashboard",
    layout="wide",
)

st.title("NYC Taxi ETL Dashboard")
st.caption("Data from PostgreSQL loaded by the Airflow ETL pipeline")


POSTGRES_USER = "taxi_user"
POSTGRES_PASSWORD = "taxi_password"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5435"
POSTGRES_DB = "taxi_db"


@st.cache_data
def load_data():
    connection_string = (
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    engine = create_engine(connection_string)

    query = """
        SELECT
            pickup_date,
            payment_type,
            passenger_count,
            trip_distance,
            fare_amount,
            tip_amount,
            total_amount
        FROM cleaned_taxi_trips
    """

    return pd.read_sql(query, engine)


taxi_data = load_data()

taxi_data["pickup_date"] = pd.to_datetime(taxi_data["pickup_date"])

total_trips = len(taxi_data)
total_revenue = taxi_data["total_amount"].sum()
average_fare = taxi_data["fare_amount"].mean()
average_distance = taxi_data["trip_distance"].mean()
average_tip = taxi_data["tip_amount"].mean()

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Total Trips", f"{total_trips:,}")
col2.metric("Total Revenue", f"${total_revenue:,.2f}")
col3.metric("Average Fare", f"${average_fare:,.2f}")
col4.metric("Average Distance", f"{average_distance:,.2f} mi")
col5.metric("Average Tip", f"${average_tip:,.2f}")

st.divider()

daily_summary = (
    taxi_data.groupby("pickup_date", as_index=False)
    .agg(
        total_trips=("pickup_date", "count"),
        total_revenue=("total_amount", "sum"),
        average_fare=("fare_amount", "mean"),
    )
)

payment_summary = (
    taxi_data.groupby("payment_type", as_index=False)
    .agg(
        total_trips=("payment_type", "count"),
        total_revenue=("total_amount", "sum"),
        average_fare=("fare_amount", "mean"),
        average_tip=("tip_amount", "mean"),
    )
)

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Daily Revenue")
    fig_daily_revenue = px.line(
        daily_summary,
        x="pickup_date",
        y="total_revenue",
        title="Revenue by Pickup Date",
    )
    st.plotly_chart(fig_daily_revenue, use_container_width=True)

with right_col:
    st.subheader("Daily Trips")
    fig_daily_trips = px.bar(
        daily_summary,
        x="pickup_date",
        y="total_trips",
        title="Trips by Pickup Date",
    )
    st.plotly_chart(fig_daily_trips, use_container_width=True)

left_col, right_col = st.columns(2)

with left_col:
    st.subheader("Revenue by Payment Type")
    fig_payment_revenue = px.bar(
        payment_summary,
        x="payment_type",
        y="total_revenue",
        title="Revenue by Payment Type",
    )
    st.plotly_chart(fig_payment_revenue, use_container_width=True)

with right_col:
    st.subheader("Trips by Payment Type")
    fig_payment_trips = px.pie(
        payment_summary,
        names="payment_type",
        values="total_trips",
        title="Trip Share by Payment Type",
    )
    st.plotly_chart(fig_payment_trips, use_container_width=True)

st.subheader("Sample Data")
st.dataframe(taxi_data.head(100))