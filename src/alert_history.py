import os
import pandas as pd


HISTORY_FILE = "logs/alert_history.csv"


def load_alert_history():
    """
    Load previously sent alerts.
    If the history file does not exist, create an empty history.
    """

    if os.path.exists(HISTORY_FILE):
        return pd.read_csv(HISTORY_FILE)

    return pd.DataFrame(
        columns=[
            "Date",
            "Metric",
            "Severity",
            "Change_Percent",
            "Alert_Sent"
        ]
    )


def alert_already_sent(date, metric, severity, history_df):
    """
    Check whether this alert has already been sent.
    """

    if history_df.empty:
        return False

    matching_alert = history_df[
        (history_df["Date"] == str(date)) &
        (history_df["Metric"] == metric) &
        (history_df["Severity"] == severity)
    ]

    return not matching_alert.empty


def record_alert(
    date,
    metric,
    severity,
    change_percent
):
    """
    Save a successfully sent alert to history.
    """

    os.makedirs("logs", exist_ok=True)

    new_alert = pd.DataFrame([
        {
            "Date": str(date),
            "Metric": metric,
            "Severity": severity,
            "Change_Percent": change_percent,
            "Alert_Sent": "Yes"
        }
    ])

    if os.path.exists(HISTORY_FILE):
        new_alert.to_csv(
            HISTORY_FILE,
            mode="a",
            header=False,
            index=False
        )
    else:
        new_alert.to_csv(
            HISTORY_FILE,
            index=False
        )