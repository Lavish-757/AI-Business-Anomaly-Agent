def analyze_business_context(row, df):
    """
    Generate a business-focused explanation for an anomaly.
    Uses cross-metric relationships when available,
    otherwise provides a metric-specific explanation.
    """

    messages = []

    # Get metric changes

    traffic_change = row.get(
        "Traffic_Change_Percent",
        0
    )

    conversion_change = row.get(
        "Conversion_Rate_Change_Percent",
        0
    )

    revenue_change = row.get(
        "Revenue_Change_Percent",
        0
    )

    orders_change = row.get(
        "Orders_Change_Percent",
        0
    )

    refunds_change = row.get(
        "Refunds_Change_Percent",
        0
    )

    marketing_change = row.get(
        "Marketing_Cost_Change_Percent",
        0
    )

    # Cross-metric relationships

    # Traffic increased + conversion declined
    if (
        traffic_change > 20
        and conversion_change < -10
    ):
        messages.append(
            "Traffic increased sharply while conversion rate declined, indicating "
            "that the additional traffic was not converting at the recent rate."
        )

    # Revenue increased + orders changed slightly
    if (
        revenue_change > 20
        and abs(orders_change) < 10
    ):
        messages.append(
            "Revenue increased significantly while order volume changed only slightly, "
            "which may indicate a change in average order value."
        )

    # Traffic decreased + conversion increased
    if (
        traffic_change < -20
        and conversion_change > 10
    ):
        messages.append(
            "Traffic declined significantly while conversion rate improved, suggesting "
            "that a smaller share of visitors may have been more likely to convert."
        )

    # Revenue decreased + orders decreased
    if (
        revenue_change < -20
        and orders_change < -15
    ):
        messages.append(
            "Revenue declined alongside lower order volume, indicating reduced sales activity."
        )

    # Refunds increased
    if refunds_change > 30:
        messages.append(
            "Refunds increased significantly and may require investigation."
        )

    # Marketing cost increased
    if marketing_change > 30:
        messages.append(
            "Marketing cost increased significantly. "
            "Review whether the additional spending was accompanied by higher traffic, orders, or revenue."
        )

    # If relationship exists

    if messages:
        return " ".join(messages)

    # Metric-specific explanations

    metric = row.get("Metric", "")

    change = row.get(
        "Change_Percent",
        0
    )

    direction = "increased" if change > 0 else "decreased"

    if metric == "Revenue":

        return (
            f"Revenue {direction} significantly compared with its recent baseline. "
            "Review order volume and conversion rate to understand the movement."
        )

    elif metric == "Orders":

        return (
            f"Order volume {direction} significantly compared with its recent baseline. "
            "Review traffic and conversion rate for potential contributing factors."
        )

    elif metric == "Conversion_Rate":

        return (
            f"Conversion rate {direction} significantly compared with its recent baseline. "
            "Review traffic quality and customer behavior for potential changes."
        )

    elif metric == "Traffic":

        return (
            f"Traffic {direction} significantly compared with its recent baseline. "
            "Review conversion rate and order volume to understand whether the traffic change is translating into business activity."
        )

    elif metric == "Marketing_Cost":

        return (
            f"Marketing cost {direction} significantly compared with its recent baseline. "
            "Review campaign performance and related changes in traffic, orders, and revenue."
        )

    elif metric == "Refunds":

        return (
            f"Refunds {direction} significantly compared with their recent baseline. "
            "Review product, order, and customer service issues for potential causes."
        )

    return (
        f"{metric} {direction} significantly compared with its recent baseline."
    )