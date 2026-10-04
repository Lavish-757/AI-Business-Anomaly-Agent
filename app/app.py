import streamlit as st
import pandas as pd
import plotly.express as px
import os


# PAGE CONFIGURATION

st.set_page_config(
    page_title="AI Business Anomaly Agent",
    page_icon="🚨",
    layout="wide"
)


# LOAD DATA

@st.cache_data
def load_anomaly_report():

    file_path = "reports/anomaly_report.csv"

    if not os.path.exists(file_path):
        return pd.DataFrame()

    df = pd.read_csv(file_path)

    df["Date"] = pd.to_datetime(df["Date"])

    return df


@st.cache_data
def load_alert_history():

    file_path = "logs/alert_history.csv"

    if not os.path.exists(file_path):
        return pd.DataFrame()

    df = pd.read_csv(file_path)

    if not df.empty:
        df["Date"] = pd.to_datetime(df["Date"])

    return df


df = load_anomaly_report()
alert_history = load_alert_history()


# CHECK DATA

if df.empty:

    st.error(
        "No anomaly report found. "
        "Run report_generator9.py first."
    )

    st.stop()


# TITLE

st.title("🚨 AI Business Anomaly Agent")

st.markdown(
    """
    **Business monitoring dashboard** for detecting unusual
    changes in revenue, orders, traffic, conversion rate,
    marketing cost, and refunds.
    """
)


st.divider()


# KPI SECTION

total_anomalies = len(df)

critical_count = len(
    df[df["Severity"] == "Critical"]
)

high_count = len(
    df[df["Severity"] == "High"]
)

medium_count = len(
    df[df["Severity"] == "Medium"]
)


# EXECUTIVE SUMMARY

st.subheader("🏢 Executive Summary")


# Determine business status
if critical_count > 0:
    business_status = "🔴 Critical"
elif high_count > 0:
    business_status = "🟠 Attention Required"
elif medium_count > 0:
    business_status = "🟡 Monitor"
else:
    business_status = "🟢 Stable"


# Find most affected metric
if not df.empty:

    metric_counts = df["Metric"].value_counts()

    most_affected_metric = metric_counts.index[0]
    most_affected_count = metric_counts.iloc[0]

else:

    most_affected_metric = "None"
    most_affected_count = 0


# Highest severity
severity_priority = {
    "Critical": 4,
    "High": 3,
    "Medium": 2,
    "Low": 1
}


if not df.empty:

    highest_severity = max(
        df["Severity"],
        key=lambda x: severity_priority.get(x, 0)
    )

else:

    highest_severity = "None"


# Number of alerts sent
if not alert_history.empty:
    alerts_sent = len(alert_history)
else:
    alerts_sent = 0


# Summary columns
col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Business Status",
        business_status
    )


with col2:

    st.metric(
        "Highest Severity",
        highest_severity
    )


with col3:

    st.metric(
        "Most Affected Metric",
        most_affected_metric
    )


with col4:

    st.metric(
        "Alerts Sent",
        alerts_sent
    )


# KEY BUSINESS OBSERVATION

if not df.empty:

    latest_anomaly = df.sort_values(
        "Date",
        ascending=False
    ).iloc[0]

    st.markdown("### 💡 Key Business Observation")

    st.info(
        f"**{latest_anomaly['Metric']}** showed a "
        f"**{latest_anomaly['Change_Percent']:.2f}%** change "
        f"on **{latest_anomaly['Date'].date()}**. "
        f"{latest_anomaly['Business_Context']}"
    )


st.divider()

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Total Anomalies",
        total_anomalies
    )


with col2:
    st.metric(
        "Critical",
        critical_count
    )


with col3:
    st.metric(
        "High",
        high_count
    )


with col4:
    st.metric(
        "Medium",
        medium_count
    )


st.divider()


# FILTER SECTION

st.subheader("🔎 Filters")


col1, col2, col3 = st.columns(3)


# Metric filter
with col1:

    metrics = ["All"] + sorted(
        df["Metric"].dropna().unique().tolist()
    )

    selected_metric = st.selectbox(
        "Metric",
        metrics
    )


# Severity filter
with col2:

    severities = ["All"] + sorted(
        df["Severity"].dropna().unique().tolist()
    )

    selected_severity = st.selectbox(
        "Severity",
        severities
    )


# Date filter
with col3:

    min_date = df["Date"].min().date()
    max_date = df["Date"].max().date()

    selected_dates = st.date_input(
        "Date Range",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )


# APPLY FILTERS

filtered_df = df.copy()


if selected_metric != "All":

    filtered_df = filtered_df[
        filtered_df["Metric"] == selected_metric
    ]


if selected_severity != "All":

    filtered_df = filtered_df[
        filtered_df["Severity"] == selected_severity
    ]


if isinstance(selected_dates, tuple) and len(selected_dates) == 2:

    start_date = pd.Timestamp(selected_dates[0])
    end_date = pd.Timestamp(selected_dates[1])

    filtered_df = filtered_df[
        (filtered_df["Date"] >= start_date) &
        (filtered_df["Date"] <= end_date)
    ]


st.divider()


# ANOMALY TREND

st.subheader("📈 Anomaly Trend")


if not filtered_df.empty:

    trend_df = (
        filtered_df
        .groupby("Date")
        .size()
        .reset_index(name="Anomalies")
    )

    fig = px.line(
        trend_df,
        x="Date",
        y="Anomalies",
        markers=True,
        title="Number of Anomalies Over Time"
    )

    fig.update_layout(
        xaxis_title="Date",
        yaxis_title="Number of Anomalies"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

else:

    st.info("No anomalies match the selected filters.")


# SEVERITY DISTRIBUTION

st.subheader("📊 Severity Distribution")


if not filtered_df.empty:

    severity_df = (
        filtered_df["Severity"]
        .value_counts()
        .reset_index()
    )

    severity_df.columns = [
        "Severity",
        "Count"
    ]

    fig = px.bar(
        severity_df,
        x="Severity",
        y="Count",
        text="Count",
        title="Anomalies by Severity"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# IMPORTANT ALERTS

st.subheader("🚨 Important Alerts")


important_df = filtered_df[
    filtered_df["Severity"].isin(
        ["Critical", "High"]
    )
].copy()


if important_df.empty:

    st.success(
        "No High or Critical anomalies "
        "match the selected filters."
    )

else:

    important_df = important_df.sort_values(
        "Date",
        ascending=False
    )

    st.dataframe(
        important_df[
            [
                "Date",
                "Metric",
                "Actual_Value",
                "Baseline",
                "Change_Percent",
                "Z_Score",
                "Severity"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )


# BUSINESS CONTEXT

st.subheader("💡 Business Context")


if important_df.empty:

    st.info(
        "No important anomaly explanations available."
    )

else:

    for _, row in important_df.iterrows():

        title = (
            f"{row['Date'].date()} | "
            f"{row['Metric']} | "
            f"{row['Severity']}"
        )

        with st.expander(title):

            st.write(
                row["Business_Context"]
            )

            st.write(
                f"**Actual Value:** "
                f"{row['Actual_Value']:.2f}"
            )

            st.write(
                f"**Baseline:** "
                f"{row['Baseline']:.2f}"
            )

            st.write(
                f"**Change:** "
                f"{row['Change_Percent']:.2f}%"
            )

            st.write(
                f"**Z-Score:** "
                f"{row['Z_Score']:.2f}"
            )


# ALL ANOMALIES TABLE

st.subheader("📋 All Detected Anomalies")


display_columns = [
    "Date",
    "Metric",
    "Actual_Value",
    "Baseline",
    "Change_Percent",
    "Z_Score",
    "Severity",
    "Business_Context"
]


st.dataframe(
    filtered_df[display_columns],
    use_container_width=True,
    hide_index=True
)

# DOWNLOAD FILTERED REPORT

st.markdown("### 📥 Download Report")


download_df = filtered_df[display_columns].copy()


# Convert Date to readable format
download_df["Date"] = download_df["Date"].dt.strftime(
    "%Y-%m-%d"
)


csv_data = download_df.to_csv(
    index=False
)


st.download_button(
    label="📥 Download Filtered Report",
    data=csv_data,
    file_name="filtered_anomaly_report.csv",
    mime="text/csv"
)

# ALERT HISTORY

st.subheader("📧 Alert History")


if alert_history.empty:

    st.info(
        "No email alerts have been recorded yet."
    )

else:

    st.dataframe(
        alert_history.sort_values(
            "Date",
            ascending=False
        ),
        use_container_width=True,
        hide_index=True
    )


# FOOTER

st.divider()

st.caption(
    "AI Business Anomaly Agent | "
    "Python • Pandas • Plotly • Streamlit"
)
