import pandas as pd


def validate_data(df):

    print("===== DATA VALIDATION =====")

    # Check missing values
    print("\nMissing values:")
    print(df.isnull().sum())

    # Check duplicate rows
    print("\nDuplicate rows:")
    print(df.duplicated().sum())

    # Check date range
    print("\nDate range:")
    print(df["Date"].min(), "to", df["Date"].max())

    # Check negative values
    numeric_columns = [
        "Revenue",
        "Orders",
        "Conversion_Rate",
        "Traffic",
        "Marketing_Cost",
        "Refunds"
    ]

    print("\nNegative values:")

    for column in numeric_columns:
        negative_count = (df[column] < 0).sum()

        print(
            f"{column}: {negative_count}"
        )


if __name__ == "__main__":

    df = pd.read_excel(
        "data/business_metrics.xlsx"
    )

    df["Date"] = pd.to_datetime(df["Date"])

    validate_data(df)