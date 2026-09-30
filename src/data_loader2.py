import pandas as pd


def load_data(file_path):
    """
    Load business metrics from an Excel file.
    """

    df = pd.read_excel(file_path)

    # Convert Date column to datetime
    df["Date"] = pd.to_datetime(df["Date"])

    # Sort by date
    df = df.sort_values("Date")

    # Reset index
    df = df.reset_index(drop=True)

    return df


if __name__ == "__main__":

    file_path = "data/business_metrics.xlsx"

    df = load_data(file_path)

    print("Data loaded successfully!")
    print()

    print("Shape:")
    print(df.shape)

    print()

    print("Columns:")
    print(df.columns.tolist())

    print()

    print("First 5 rows:")
    print(df.head())