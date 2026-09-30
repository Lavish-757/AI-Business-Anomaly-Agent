def analyze_business_context(
    row,
    df
):

    date = row["Date"]

    current_row = df[
        df["Date"] == date
    ]

    if current_row.empty:
        return ""

    current_row = current_row.iloc[0]

    messages = []

    # Traffic vs conversion
    if (
        "Traffic" in df.columns
        and "Conversion_Rate" in df.columns
    ):

        traffic_change = row.get(
            "Traffic_Change_Percent",
            0
        )

        conversion_change = row.get(
            "Conversion_Rate_Change_Percent",
            0
        )

        if (
            traffic_change > 20
            and conversion_change < -10
        ):

            messages.append("Traffic increased sharply while conversion rate declined.")

    # Revenue vs orders
    if (
        "Revenue_Change_Percent" in row
        and "Orders_Change_Percent" in row
    ):

        revenue_change = row[
            "Revenue_Change_Percent"
        ]

        orders_change = row[
            "Orders_Change_Percent"
        ]

        if (
            revenue_change > 20
            and orders_change < 10
        ):

            messages.append("Revenue increased significantly while order volume changed only slightly.")

    # Refunds
    if (
        "Refunds_Change_Percent" in row
    ):

        refunds_change = row[
            "Refunds_Change_Percent"
        ]

        if refunds_change > 30:

            messages.append("Refunds also increased significantly.")

    if not messages:
        return ( "No major cross-metric relationship was identified." )

    return " ".join(messages)


def add_business_context(
    report_df,
    monitoring_df
):

    report_df = report_df.copy()

    report_df["Business_Context"] = report_df.apply(
        lambda row: analyze_business_context(
            row,
            monitoring_df
        ),
        axis=1
    )

    return report_df