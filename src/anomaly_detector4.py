import pandas as pd


def calculate_baseline(
    df,
    metric,
    window=7
):
    """
    Calculate the rolling average baseline
    using previous observations.
    """

    baseline = (
        df[metric]
        .rolling(window=window)
        .mean()
        .shift(1)
    )

    return baseline


def calculate_change(
    df,
    metric,
    window=7
):
    """
    Calculate percentage change
    between current value and baseline.
    """

    baseline = calculate_baseline(
        df,
        metric,
        window
    )

    change_percent = (
        (df[metric] - baseline)
        / baseline
    ) * 100

    return baseline, change_percent


def calculate_z_score(
    df,
    metric,
    window=7
):
    """
    Calculate rolling Z-score using
    previous observations.
    """

    rolling_mean = (
        df[metric]
        .rolling(window=window)
        .mean()
        .shift(1)
    )

    rolling_std = (
        df[metric]
        .rolling(window=window)
        .std()
        .shift(1)
    )

    z_score = (
        (df[metric] - rolling_mean)
        / rolling_std
    )

    return z_score


def calculate_severity(
    change_percent,
    z_score
):
    """
    Assign severity based on
    percentage change and Z-score.
    """

    change = abs(change_percent)
    z = abs(z_score)

    if change >= 50 or z >= 4:
        return "Critical"

    elif change >= 30 or z >= 3:
        return "High"

    elif change >= 20 or z >= 2:
        return "Medium"

    else:
        return "Low"


def detect_anomalies(
    df,
    metric,
    threshold=20,
    z_threshold=2,
    window=7
):
    """
    Detect anomalies using both
    percentage change and Z-score.
    """

    result = df.copy()

    # Calculate baseline and percentage change
    baseline, change_percent = calculate_change(
        df,
        metric,
        window
    )

    # Calculate Z-score
    z_score = calculate_z_score(
        df,
        metric,
        window
    )

    # Store results
    result["Baseline"] = baseline
    result["Change_Percent"] = change_percent
    result["Z_Score"] = z_score

    # Percentage-change signal
    percentage_signal = (
        result["Change_Percent"].abs()
        >= threshold
    )

    # Z-score signal
    z_score_signal = (
        result["Z_Score"].abs()
        >= z_threshold
    )

    # Detect anomaly if either signal is triggered
    result["Is_Anomaly"] = (
        percentage_signal
        | z_score_signal
    )

    # Calculate severity
    result["Severity"] = result.apply(
        lambda row: calculate_severity(
            row["Change_Percent"],
            row["Z_Score"]
        ),
        axis=1
    )

    return result


if __name__ == "__main__":

    # Load data
    df = pd.read_excel(
        "data/business_metrics.xlsx"
    )

    # Convert Date column
    df["Date"] = pd.to_datetime(
        df["Date"]
    )

    # Metric-specific thresholds
    metrics = {
        "Revenue": 20,
        "Orders": 20,
        "Conversion_Rate": 15,
        "Traffic": 20,
        "Marketing_Cost": 20,
        "Refunds": 25
    }

    # Detect anomalies for each metric
    for metric, threshold in metrics.items():

        result = detect_anomalies(
            df,
            metric=metric,
            threshold=threshold,
            z_threshold=2,
            window=7
        )

        anomalies = result[
            result["Is_Anomaly"]
        ]

        print(
            f"\n===== {metric.upper()} ====="
        )

        print(
            anomalies[
                [
                    "Date",
                    metric,
                    "Baseline",
                    "Change_Percent",
                    "Z_Score",
                    "Severity"
                ]
            ].to_string(index=False)
        )