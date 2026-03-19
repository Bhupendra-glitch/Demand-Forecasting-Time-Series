import pandas as pd

# -------------------------------
# Column Detection
# -------------------------------
def detect_columns(df):
    cols = df.columns

    date_col = [c for c in cols if "date" in c.lower()]
    sales_col = [c for c in cols if "sales" in c.lower() or "revenue" in c.lower()]

    if not date_col or not sales_col:
        raise Exception("Columns not detected")

    return date_col[0], sales_col[0]


# -------------------------------
# Insight Generator
# -------------------------------
def generate_insights(df, date_col, sales_col):
    insights = []

    # Trend
    if df[sales_col].iloc[-1] > df[sales_col].iloc[0]:
        insights.append("📈 Sales show an increasing trend")
    else:
        insights.append("📉 Sales show a decreasing trend")

    # Average
    avg = df[sales_col].mean()
    insights.append(f"📊 Average sales: {round(avg,2)}")

    # Peak day
    df["day"] = pd.to_datetime(df[date_col]).dt.day_name()
    peak_day = df.groupby("day")[sales_col].mean().idxmax()

    insights.append(f"🔥 Highest sales usually occur on {peak_day}")

    # Variability
    if df[sales_col].std() > avg * 0.5:
        insights.append("⚠️ High fluctuation in sales detected")

    # Growth %
    growth = ((df[sales_col].iloc[-1] - df[sales_col].iloc[0]) / df[sales_col].iloc[0]) * 100
    insights.append(f"📈 Overall growth: {round(growth,2)}%")

    return insights