import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Business Insights", layout="wide")

st.title("🎯 Business Insights & Recommendations")
st.markdown("Turn your data into actionable business decisions 📊")

# -------------------------------
# 📂 Upload Dataset
# -------------------------------
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], key="insights")

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    # -------------------------------
    # 🧠 Column Selection
    # -------------------------------
    date_cols = [col for col in df.columns if "date" in col.lower()]
    numeric_cols = df.select_dtypes(include=np.number).columns.tolist()

    if not numeric_cols:
        st.error("❌ No numeric column found")
        st.stop()

    date_col = st.selectbox("Select Date Column", date_cols if date_cols else df.columns)
    sales_col = st.selectbox("Select Sales Column", numeric_cols)

    # -------------------------------
    # 🧹 Preprocessing
    # -------------------------------
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col])
    df = df.sort_values(by=date_col)

    # -------------------------------
    # 📊 KPI Metrics
    # -------------------------------
    st.subheader("📊 Business KPIs")

    col1, col2, col3, col4 = st.columns(4)

    total_sales = df[sales_col].sum()
    avg_sales = df[sales_col].mean()
    max_sales = df[sales_col].max()
    min_sales = df[sales_col].min()

    col1.metric("Total Sales", f"{total_sales:,.2f}")
    col2.metric("Average Sales", f"{avg_sales:,.2f}")
    col3.metric("Peak Sales", f"{max_sales:,.2f}")
    col4.metric("Lowest Sales", f"{min_sales:,.2f}")

    # -------------------------------
    # 📈 Trend Analysis
    # -------------------------------
    st.subheader("📈 Sales Trend")

    fig = px.line(df, x=date_col, y=sales_col, title="Sales Trend")
    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # 📅 Monthly Insights
    # -------------------------------
    df["Month"] = df[date_col].dt.to_period("M").astype(str)
    monthly_sales = df.groupby("Month")[sales_col].sum().reset_index()

    best_month = monthly_sales.loc[monthly_sales[sales_col].idxmax()]
    worst_month = monthly_sales.loc[monthly_sales[sales_col].idxmin()]

    st.subheader("📅 Monthly Performance")

    col1, col2 = st.columns(2)

    col1.success(f"📈 Best Month: {best_month['Month']} (Sales: {best_month[sales_col]:,.2f})")
    col2.error(f"📉 Worst Month: {worst_month['Month']} (Sales: {worst_month[sales_col]:,.2f})")

    fig_month = px.bar(monthly_sales, x="Month", y=sales_col, title="Monthly Sales")
    st.plotly_chart(fig_month, use_container_width=True)

    # -------------------------------
    # 📆 Day-wise Insights
    # -------------------------------
    df["Day"] = df[date_col].dt.day_name()
    day_sales = df.groupby("Day")[sales_col].mean().reindex(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    ).reset_index()

    best_day = day_sales.loc[day_sales[sales_col].idxmax()]
    worst_day = day_sales.loc[day_sales[sales_col].idxmin()]

    st.subheader("📆 Weekly Insights")

    col1, col2 = st.columns(2)

    col1.success(f"🔥 Best Day: {best_day['Day']}")
    col2.warning(f"⚠️ Weak Day: {worst_day['Day']}")

    fig_day = px.bar(day_sales, x="Day", y=sales_col, title="Average Sales by Day")
    st.plotly_chart(fig_day, use_container_width=True)

    # -------------------------------
    # 🤖 Smart Business Insights
    # -------------------------------
    st.subheader("🤖 Smart Recommendations")

    insights = []

    # Trend Insight
    if df[sales_col].iloc[-1] > df[sales_col].iloc[0]:
        insights.append("📈 Sales are increasing → Consider expanding inventory")
    else:
        insights.append("📉 Sales are declining → Review pricing or marketing strategy")

    # Monthly Insight
    insights.append(f"📅 Focus marketing campaigns in {best_month['Month']} for maximum impact")

    # Weekly Insight
    insights.append(f"🛒 Increase promotions on {worst_day['Day']} to boost sales")

    # Variability Insight
    if df[sales_col].std() > df[sales_col].mean() * 0.5:
        insights.append("⚠️ High sales variability → Improve demand planning")

    # Display Insights
    for insight in insights:
        st.info(insight)

    # -------------------------------
    # 📥 Export Insights
    # -------------------------------
    st.subheader("📥 Export Insights")

    insights_text = "\n".join(insights)

    st.download_button(
        label="Download Insights Report",
        data=insights_text,
        file_name="business_insights.txt",
        mime="text/plain"
    )

else:
    st.info("👆 Upload a dataset to generate business insights.")