import pandas as pd

from anomaly_detector4 import detect_anomalies
from config5 import METRIC_RULES


def create_monitoring_data(df):
    """
    Run anomaly detection for all configured business metrics.
    """

    monitoring_df = df.copy()

    for metric, rules in METRIC_RULES.items():

        result = detect_anomalies(
            df,
            metric,
            threshold=rules["threshold"],
            z_threshold=rules["z_threshold"],
            window=7
        )

        monitoring_df[
            f"{metric}_Baseline"
        ] = result["Baseline"]

        monitoring_df[
            f"{metric}_Change_Percent"
        ] = result["Change_Percent"]

        monitoring_df[
            f"{metric}_Z_Score"
        ] = result["Z_Score"]

        monitoring_df[
            f"{metric}_Is_Anomaly"
        ] = result["Is_Anomaly"]

        monitoring_df[
            f"{metric}_Severity"
        ] = result["Severity"]

    return monitoring_df


if __name__ == "__main__":

    # Load business data
    df = pd.read_excel(
        "data/business_metrics.xlsx"
    )

    # Convert Date column
    df["Date"] = pd.to_datetime(
        df["Date"]
    )

    # Create monitoring data
    monitoring_df = create_monitoring_data(df)

    # Save result
    monitoring_df.to_csv(
        "reports/monitoring_data.csv",
        index=False
    )

    print("Monitoring completed successfully.")

    print(
        f"Rows processed: {len(monitoring_df)}"
    )

    print(
        "Saved to: reports/monitoring_data.csv"
    )
    