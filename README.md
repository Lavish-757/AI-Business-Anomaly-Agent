# 🚨 AI Business Anomaly Agent
🚀 **Live Demo:** https://ai-business-anomaly-agent-757.streamlit.app/

An automated business monitoring system that detects unusual changes in key business metrics, analyzes cross-metric relationships, generates business-focused explanations, and sends email alerts for High and Critical anomalies.

The project includes an interactive Streamlit dashboard for monitoring anomalies, investigating trends, and reviewing alert history.

---

## 📌 Project Overview

Businesses continuously generate metrics such as revenue, orders, traffic, conversion rate, marketing cost, and refunds.

Manually monitoring these metrics can make it difficult to identify unusual changes quickly.

This project automates the monitoring process by:

- Validating business data
- Establishing rolling baselines
- Detecting unusual metric changes
- Calculating statistical Z-scores
- Assigning anomaly severity
- Analyzing relationships between business metrics
- Generating business-context explanations
- Sending High/Critical email alerts
- Preventing duplicate alerts
- Maintaining alert history
- Providing an interactive Streamlit dashboard

---

## 🎯 Objectives

The main objectives of this project are:

1. Detect unusual business metric behavior automatically.
2. Identify the severity of detected anomalies.
3. Provide business-focused explanations instead of only numerical alerts.
4. Notify users about important anomalies through email.
5. Provide an interactive dashboard for monitoring and investigation.
6. Maintain a history of previously sent alerts.

---

## 🏗️ Project Architecture

```text
Business Metrics Excel File
          ↓
     Data Loading
          ↓
    Data Validation
          ↓
   Rolling Baseline
          ↓
 Anomaly Detection
    ↓          ↓
% Change     Z-Score
    ↓          ↓
      Severity
          ↓
  Business Context
          ↓
   Anomaly Report
      ↙       ↘
 Email Alert   Streamlit
      ↓        Dashboard
 Alert History
