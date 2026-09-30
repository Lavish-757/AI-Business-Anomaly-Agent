def get_direction(change_percent):

    if change_percent > 0:
        return "increased"

    elif change_percent < 0:
        return "decreased"

    return "remained stable"


def explain_anomaly(
    metric,
    change_percent,
    severity
):

    direction = get_direction(
        change_percent
    )

    change = abs(change_percent)

    if metric == "Revenue":

        return (
            f"Revenue {direction} by "
            f"{change:.1f}%, which is a "
            f"{severity.lower()}-severity movement "
            f"compared with the recent baseline."
        )

    elif metric == "Orders":

        return (
            f"Orders {direction} by "
            f"{change:.1f}%. This indicates "
            f"a significant change in order volume."
        )

    elif metric == "Conversion_Rate":

        return (
            f"Conversion rate {direction} by "
            f"{change:.1f}%. This may indicate "
            f"a change in traffic quality or "
            f"customer purchasing behavior."
        )

    elif metric == "Traffic":

        return (
            f"Traffic {direction} by "
            f"{change:.1f}%. This indicates "
            f"a significant change in visitor volume."
        )

    elif metric == "Marketing_Cost":

        return (
            f"Marketing cost {direction} by "
            f"{change:.1f}%. Review campaign spending "
            f"and marketing efficiency."
        )

    elif metric == "Refunds":

        return (
            f"Refunds {direction} by "
            f"{change:.1f}%. An increase may require "
            f"investigation into product, delivery, "
            f"or customer-service issues."
        )

    return (
        f"{metric} {direction} by "
        f"{change:.1f}%."
    )