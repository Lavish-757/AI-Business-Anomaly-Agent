import pandas as pd
import streamlit as st
import plotly.express as px


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="AI Anomaly Agent",
    page_icon="🚨",
    layout="wide"
)


# -----------------------------
# Load Data
# -----------------------------

@st.cache_data
def load_data():

    df = pd.read_csv(
        "reports/anomaly_report.csv"
    )

    df["Date"] = pd.to_datetime(
        df["Date"]
    )

    return df


df = load_data()


# -----------------------------
# Title
# -----------------------------

st.title("🚨 AI Business Anomaly Agent")

st.write(
    "Monitor business metrics, detect anomalies, "
    "and understand their potential business impact."
)


# -----------------------------
# KPI Section
# -----------------------------

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


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Anomalies",
    total_anomalies
)

col2.metric(
    "Critical",
    critical_count
)

col3.metric(
    "High",
    high_count
)

col4.metric(
    "Medium",
    medium_count
)


st.divider()


# -----------------------------
# Filters
# -----------------------------

st.subheader("🔎 Filters")

col1, col2 = st.columns(2)

with col1:

    selected_metrics = st.multiselect(
        "Select Metric",
        options=sorted(df["Metric"].unique()),
        default=sorted(df["Metric"].unique())
    )


with col2:

    selected_severity = st.multiselect(
        "Select Severity",
        options=[
            "Critical",
            "High",
            "Medium",
            "Low"
        ],
        default=[
            "Critical",
            "High",
            "Medium"
        ]
    )


filtered_df = df[
    (df["Metric"].isin(selected_metrics))
    &
    (df["Severity"].isin(selected_severity))
]


# -----------------------------
# Anomaly Table
# -----------------------------

st.subheader("📋 Detected Anomalies")

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
    use_container_width=True
)


# -----------------------------
# Change % Chart
# -----------------------------

st.subheader("📈 Anomaly Changes")

fig = px.scatter(
    filtered_df,
    x="Date",
    y="Change_Percent",
    color="Metric",
    hover_data=[
        "Severity",
        "Actual_Value",
        "Baseline",
        "Z_Score"
    ],
    title="Percentage Change from Baseline"
)

fig.add_hline(
    y=20,
    line_dash="dash",
    annotation_text="20% threshold"
)

fig.add_hline(
    y=-20,
    line_dash="dash",
    annotation_text="-20% threshold"
)

st.plotly_chart(
    fig,
    use_container_width=True
)


# -----------------------------
# Business Context
# -----------------------------

st.subheader("🧠 Business Context")

if not filtered_df.empty:

    for _, row in filtered_df.iterrows():

        with st.expander(
            f"{row['Date'].date()} — "
            f"{row['Metric']} — "
            f"{row['Severity']}"
        ):

            st.write(
                row["Business_Context"]
            )

else:

    st.info(
        "No anomalies match the selected filters."
    )