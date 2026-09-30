import pandas as pd

from monitor8 import create_monitoring_data
from context_analysis7 import analyze_business_context


def generate_report(df):
    """
    Generate a clean anomaly report from monitoring data.
    """

    monitoring_df = create_monitoring_data(df)

    report_rows = []

    for _, row in monitoring_df.iterrows():

        for metric in [
            "Revenue",
            "Orders",
            "Conversion_Rate",
            "Traffic",
            "Marketing_Cost",
            "Refunds"
        ]:

            is_anomaly = row[
                f"{metric}_Is_Anomaly"
            ]

            if is_anomaly:

                report_rows.append({
                    "Date": row["Date"],
                    "Metric": metric,
                    "Actual_Value": row[metric],
                    "Baseline": row[
                        f"{metric}_Baseline"
                    ],
                    "Change_Percent": row[
                        f"{metric}_Change_Percent"
                    ],
                    "Z_Score": row[
                        f"{metric}_Z_Score"
                    ],
                    "Severity": row[
                        f"{metric}_Severity"
                    ]
                })

    report_df = pd.DataFrame(report_rows)

    if report_df.empty:
        report_df["Business_Context"] = []
        return report_df

    # Add business context
    report_df["Business_Context"] = report_df.apply(
        lambda row: analyze_business_context(
            row,
            monitoring_df
        ),
        axis=1
    )

    return report_df


if __name__ == "__main__":

    # Load original business data
    df = pd.read_excel(
        "data/business_metrics.xlsx"
    )

    # Convert Date
    df["Date"] = pd.to_datetime(
        df["Date"]
    )

    # Generate anomaly report
    report_df = generate_report(df)

    # Save report
    report_df.to_csv(
        "reports/anomaly_report.csv",
        index=False
    )

    print("Anomaly report generated successfully.")

    print(f"Total anomalies: {len(report_df)}")

    print("Saved to: reports/anomaly_report.csv")