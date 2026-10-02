import os
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv


# Load environment variables
load_dotenv()


EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")


def send_email_alert(
    metric,
    date,
    actual_value,
    baseline,
    change_percent,
    severity,
    business_context
):
    """
    Send an email alert for a High or Critical anomaly.
    """

    # Only send important alerts
    if severity not in ["High", "Critical"]:
        return False

    subject = (
        f"🚨 {severity} Business Anomaly - {metric}"
    )

    body = f"""
AI Business Anomaly Agent
=========================

Anomaly Detected

Date:
{date}

Metric:
{metric}

Severity:
{severity}

Actual Value:
{actual_value:.2f}

Baseline:
{baseline:.2f}

Change:
{change_percent:.2f}%

Business Context:
{business_context}

Please investigate this metric.
"""

    message = MIMEMultipart()

    message["From"] = EMAIL_SENDER
    message["To"] = EMAIL_RECEIVER
    message["Subject"] = subject

    message.attach(
        MIMEText(body, "plain")
    )

    try:

        with smtplib.SMTP(
            "smtp.gmail.com",
            587
        ) as server:

            server.starttls()

            server.login(
                EMAIL_SENDER,
                EMAIL_PASSWORD
            )

            server.send_message(
                message
            )

        print(
            f"Email sent: {metric} - {severity}"
        )

        return True

    except Exception as e:

        print(
            f"Email failed: {e}"
        )

        return False
