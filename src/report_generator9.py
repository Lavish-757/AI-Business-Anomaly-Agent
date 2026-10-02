import pandas as pd

from monitor8 import create_monitoring_data
from context_analysis7 import analyze_business_context
from email_alert import send_email_alert

from alert_history import (
    load_alert_history,
    alert_already_sent,
    record_alert
)

def generate_report(df):
    """
    Generate a clean anomaly report from monitoring data.
    """

    monitoring_df = create_monitoring_data(df)

    report_rows = []

    metrics = [
        "Revenue",
        "Orders",
        "Conversion_Rate",
        "Traffic",
        "Marketing_Cost",
        "Refunds"
    ]

    # Create anomaly report

    for _, row in monitoring_df.iterrows():

        for metric in metrics:

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

    contexts = []

    for _, anomaly_row in report_df.iterrows():

        date = anomaly_row["Date"]

        matching_rows = monitoring_df[
            monitoring_df["Date"] == date
        ]

        if matching_rows.empty:

            context = (
                "No business context available."
            )

        else:
            
            full_monitoring_row = (
                matching_rows.iloc[0].copy()
            )

            full_monitoring_row["Metric"] = (
                anomaly_row["Metric"]
            )

            full_monitoring_row["Change_Percent"] = (
                anomaly_row["Change_Percent"]
            )

            context = analyze_business_context(
                full_monitoring_row,
                monitoring_df
            )

        contexts.append(context)

    report_df["Business_Context"] = contexts

    return report_df


if __name__ == "__main__":

    df = pd.read_excel(
        "data/business_metrics.xlsx"
    )

    df["Date"] = pd.to_datetime(
        df["Date"]
    )

    report_df = generate_report(df)

    report_df.to_csv(
        "reports/anomaly_report.csv",
        index=False
    )

    print("Anomaly report generated successfully.")

    print(f"Total anomalies: {len(report_df)}")

    print("Saved to: reports/anomaly_report.csv")


    # Load previously sent alerts
    history_df = load_alert_history()


    # Send only new High / Critical alerts
    for _, row in report_df.iterrows():

        if row["Severity"] in ["High", "Critical"]:

            already_sent = alert_already_sent(
                date=row["Date"],
                metric=row["Metric"],
                severity=row["Severity"],
                history_df=history_df
            )

            if already_sent:
                print(
                    f"Skipping duplicate alert: "
                    f"{row['Metric']} - {row['Severity']}"
                )
                continue

            # Send email
            email_sent = send_email_alert(
                metric=row["Metric"],
                date=row["Date"],
                actual_value=row["Actual_Value"],
                baseline=row["Baseline"],
                change_percent=row["Change_Percent"],
                severity=row["Severity"],
                business_context=row["Business_Context"]
            )

            # Record only if email was successfully sent
            if email_sent:

                record_alert(
                    date=row["Date"],
                    metric=row["Metric"],
                    severity=row["Severity"],
                    change_percent=row["Change_Percent"]
                )

                # Update in-memory history
                history_df = pd.concat(
                    [
                        history_df,
                        pd.DataFrame([
                            {
                                "Date": str(row["Date"]),
                                "Metric": row["Metric"],
                                "Severity": row["Severity"],
                                "Change_Percent": row["Change_Percent"],
                                "Alert_Sent": "Yes"
                            }
                        ])
                    ],    
                    ignore_index=True
                )
                