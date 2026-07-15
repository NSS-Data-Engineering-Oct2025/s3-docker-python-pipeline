import os

import pandas as pd
import plotly.express as px
import streamlit as st
from sqlalchemy import create_engine


st.set_page_config(
    page_title="NYC Taxi ETL Dashboard",
    page_icon="🚕",
    layout="wide",
)

st.title("🚕 NYC Taxi ETL Dashboard")
st.caption("PostgreSQL data loaded by the Airflow ETL pipeline")


POSTGRES_USER = os.getenv("POSTGRES_USER", "taxi_user")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "taxi_password")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5435")
POSTGRES_DB = os.getenv("POSTGRES_DB", "taxi_db")


@st.cache_data(ttl=600)
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

    dataframe = pd.read_sql(query, engine)
    dataframe["pickup_date"] = pd.to_datetime(dataframe["pickup_date"])

    return dataframe


try:
    taxi_data = load_data()
except Exception as error:
    st.error(f"Could not load PostgreSQL data: {error}")
    st.stop()


st.sidebar.header("Dashboard Filters")

minimum_date = taxi_data["pickup_date"].min().date()
maximum_date = taxi_data["pickup_date"].max().date()

selected_dates = st.sidebar.date_input(
    "Pickup date range",
    value=(minimum_date, maximum_date),
    min_value=minimum_date,
    max_value=maximum_date,
)

payment_options = sorted(taxi_data["payment_type"].dropna().unique().tolist())

selected_payment_types = st.sidebar.multiselect(
    "Payment types",
    options=payment_options,
    default=payment_options,
)

passenger_options = sorted(
    taxi_data["passenger_count"].dropna().astype(int).unique().tolist()
)

selected_passenger_counts = st.sidebar.multiselect(
    "Passenger counts",
    options=passenger_options,
    default=passenger_options,
)

if st.sidebar.button("Refresh PostgreSQL Data"):
    st.cache_data.clear()
    st.rerun()


if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
else:
    start_date = end_date = selected_dates

filtered_data = taxi_data[
    (taxi_data["pickup_date"].dt.date >= start_date)
    & (taxi_data["pickup_date"].dt.date <= end_date)
    & (taxi_data["payment_type"].isin(selected_payment_types))
    & (
        taxi_data["passenger_count"]
        .fillna(-1)
        .astype(int)
        .isin(selected_passenger_counts)
    )
].copy()


if filtered_data.empty:
    st.warning("No records match the selected filters.")
    st.stop()


total_trips = len(filtered_data)
total_revenue = filtered_data["total_amount"].sum()
average_fare = filtered_data["fare_amount"].mean()
average_distance = filtered_data["trip_distance"].mean()
average_tip = filtered_data["tip_amount"].mean()

column_1, column_2, column_3, column_4, column_5 = st.columns(5)

column_1.metric("Total Trips", f"{total_trips:,}")
column_2.metric("Total Revenue", f"${total_revenue:,.2f}")
column_3.metric("Average Fare", f"${average_fare:,.2f}")
column_4.metric("Average Distance", f"{average_distance:,.2f} mi")
column_5.metric("Average Tip", f"${average_tip:,.2f}")

st.divider()

daily_summary = (
    filtered_data.groupby("pickup_date", as_index=False)
    .agg(
        total_trips=("pickup_date", "count"),
        total_revenue=("total_amount", "sum"),
        average_fare=("fare_amount", "mean"),
    )
)

payment_summary = (
    filtered_data.groupby("payment_type", as_index=False)
    .agg(
        total_trips=("payment_type", "count"),
        total_revenue=("total_amount", "sum"),
        average_fare=("fare_amount", "mean"),
        average_tip=("tip_amount", "mean"),
    )
)

left_column, right_column = st.columns(2)

with left_column:
    st.subheader("Daily Revenue")

    daily_revenue_chart = px.line(
        daily_summary,
        x="pickup_date",
        y="total_revenue",
        markers=True,
        title="Revenue by Pickup Date",
    )

    st.plotly_chart(daily_revenue_chart, use_container_width=True)

with right_column:
    st.subheader("Daily Trips")

    daily_trip_chart = px.bar(
        daily_summary,
        x="pickup_date",
        y="total_trips",
        title="Trips by Pickup Date",
    )

    st.plotly_chart(daily_trip_chart, use_container_width=True)

left_column, right_column = st.columns(2)

with left_column:
    st.subheader("Revenue by Payment Type")

    payment_revenue_chart = px.bar(
        payment_summary,
        x="payment_type",
        y="total_revenue",
        title="Revenue by Payment Type",
    )

    st.plotly_chart(payment_revenue_chart, use_container_width=True)

with right_column:
    st.subheader("Trips by Payment Type")

    payment_trip_chart = px.pie(
        payment_summary,
        names="payment_type",
        values="total_trips",
        title="Trip Share by Payment Type",
    )

    st.plotly_chart(payment_trip_chart, use_container_width=True)

left_column, right_column = st.columns(2)

with left_column:
    st.subheader("Fare Distribution")

    fare_chart = px.histogram(
        filtered_data,
        x="fare_amount",
        nbins=50,
        title="Fare Amount Distribution",
    )

    st.plotly_chart(fare_chart, use_container_width=True)

with right_column:
    st.subheader("Trip Distance Distribution")

    distance_chart = px.histogram(
        filtered_data,
        x="trip_distance",
        nbins=50,
        title="Trip Distance Distribution",
    )

    st.plotly_chart(distance_chart, use_container_width=True)

st.subheader("Filtered Data")

st.dataframe(
    filtered_data.head(500),
    use_container_width=True,
)

csv_data = filtered_data.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download Filtered Data as CSV",
    data=csv_data,
    file_name="filtered_nyc_taxi_data.csv",
    mime="text/csv",
)