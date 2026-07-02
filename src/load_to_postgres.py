import pandas as pd
from sqlalchemy import create_engine


POSTGRES_USER = "taxi_user"
POSTGRES_PASSWORD = "taxi_password"
POSTGRES_HOST = "localhost"
POSTGRES_PORT = "5435"
POSTGRES_DB = "taxi_db"

PARQUET_FILE = "data/processed/cleaned_taxi_trips.parquet"


def load_cleaned_taxi_data_to_postgres():
    print("Reading cleaned taxi Parquet file...")
    taxi_data = pd.read_parquet(PARQUET_FILE)

    print(f"Rows to load: {len(taxi_data):,}")

    connection_string = (
        f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}"
        f"@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    )

    engine = create_engine(connection_string)

    print("Loading data into PostgreSQL table: cleaned_taxi_trips")

    taxi_data.to_sql(
        "cleaned_taxi_trips",
        engine,
        if_exists="replace",
        index=False,
        chunksize=10000,
    )

    print("Data loaded into PostgreSQL successfully.")


if __name__ == "__main__":
    load_cleaned_taxi_data_to_postgres()