import pandas as pd
import numpy as np

# Make results reproducible
np.random.seed(42)

# Create 90 days of business data
dates = pd.date_range(
    start="2026-06-01",
    periods=90,
    freq="D"
    )

# Generate normal business metrics
traffic = np.random.normal(25000, 1800, 90).round()
orders = np.random.normal(1000, 80, 90).round()
conversion_rate = (orders / traffic * 100).round(2)

marketing_cost = np.random.normal(18000, 1200, 90).round()
average_order_value = np.random.normal(100, 8, 90).round(2)

revenue = (
    orders * average_order_value
).round()

refunds = np.random.normal(3500, 500, 90).round()

# Create DataFrame
df = pd.DataFrame({
    "Date": dates,
    "Revenue": revenue,
    "Orders": orders,
    "Conversion_Rate": conversion_rate,
    "Traffic": traffic,
    "Marketing_Cost": marketing_cost,
    "Refunds": refunds
    })


# Add artificial anomalies

# Day 60: traffic spike but conversion drops
df.loc[59, "Traffic"] *= 1.45
df.loc[59, "Conversion_Rate"] *= 0.70
df.loc[59, "Orders"] *= 1.05

# Day 70: revenue spike
df.loc[69, "Revenue"] *= 1.35
df.loc[69, "Orders"] *= 1.10

# Day 78: refund spike
df.loc[77, "Refunds"] *= 2.00

# Day 85: major traffic drop
df.loc[84, "Traffic"] *= 0.55
df.loc[84, "Orders"] *= 0.60
df.loc[84, "Revenue"] *= 0.60

# Round values
df["Revenue"] = df["Revenue"].round()
df["Orders"] = df["Orders"].round()
df["Traffic"] = df["Traffic"].round()
df["Marketing_Cost"] = df["Marketing_Cost"].round()
df["Refunds"] = df["Refunds"].round()

# Save as Excel
output_path = "data/business_metrics.xlsx"

df.to_excel(
    output_path,
    index=False
)

print("Dataset created successfully!")
print(f"Saved to: {output_path}")
print(f"Rows: {len(df)}")
print(f"Columns: {len(df.columns)}")