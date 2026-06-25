def run_data_quality_checks(raw_rows, cleaned_data):
    """
    Run data quality checks on the cleaned NYC Taxi dataset.
    """

    cleaned_rows = len(cleaned_data)
    removed_rows = raw_rows - cleaned_rows

    print("\n" + "=" * 50)
    print("DATA QUALITY REPORT")
    print("=" * 50)

    print(f"Raw Rows:              {raw_rows:,}")
    print(f"Cleaned Rows:          {cleaned_rows:,}")
    print(f"Rows Removed:          {removed_rows:,}")

    required_columns = [
        "passenger_count",
        "trip_distance",
        "fare_amount",
        "total_amount",
    ]

    print("\nMissing Values")
    for column in required_columns:
        missing_count = cleaned_data[column].isna().sum()
        print(f"{column:<20} {missing_count}")

    negative_fares = (cleaned_data["fare_amount"] < 0).sum()
    negative_distances = (cleaned_data["trip_distance"] < 0).sum()
    duplicate_rows = cleaned_data.duplicated().sum()

    print("\nBusiness Rule Checks")
    print(f"Negative Fare Records:      {negative_fares}")
    print(f"Negative Distance Records:  {negative_distances}")
    print(f"Duplicate Records:          {duplicate_rows}")

    if negative_fares == 0 and negative_distances == 0 and duplicate_rows == 0:
        print("\nData Quality Status: PASSED")
    else:
        print("\nData Quality Status: FAILED")

    print("=" * 50)