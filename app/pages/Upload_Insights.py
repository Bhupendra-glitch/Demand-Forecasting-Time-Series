import streamlit as st
import pandas as pd
import plotly.express as px
from utils.auto_insights import detect_columns, generate_insights

st.set_page_config(page_title="Upload & Insights", layout="wide")

st.title("📂 Upload & Auto Insights")
st.markdown("Upload any sales dataset and get instant insights 🚀")

# -------------------------------
# 📂 File Upload
# -------------------------------
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:

    # -------------------------------
    # 📊 Load Data
    # -------------------------------
    df = pd.read_csv(uploaded_file)

    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    # -------------------------------
    # 🧠 Auto Column Detection
    # -------------------------------
    try:
        date_col, sales_col = detect_columns(df)
        st.success(f"✅ Detected → Date: {date_col} | Sales: {sales_col}")
    except:
        st.warning("⚠️ Auto-detection failed. Please select manually.")
        date_col = st.selectbox("Select Date Column", df.columns)
        sales_col = st.selectbox("Select Sales Column", df.columns)

    # -------------------------------
    # 🧹 Data Processing
    # -------------------------------
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col])
    df = df.sort_values(by=date_col)

    # -------------------------------
    # 📊 KPI Metrics
    # -------------------------------
    st.subheader("📊 Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Sales", f"{df[sales_col].sum():,.2f}")
    col2.metric("Average Sales", f"{df[sales_col].mean():,.2f}")
    col3.metric("Max Sales", f"{df[sales_col].max():,.2f}")
    col4.metric("Min Sales", f"{df[sales_col].min():,.2f}")

    # -------------------------------
    # 📈 Sales Trend
    # -------------------------------
    st.subheader("📈 Sales Trend")

    fig = px.line(df, x=date_col, y=sales_col, title="Sales Over Time")
    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # 📅 Monthly Analysis
    # -------------------------------
    st.subheader("📅 Monthly Sales")

    df["Month"] = df[date_col].dt.to_period("M").astype(str)
    monthly_sales = df.groupby("Month")[sales_col].sum().reset_index()

    fig_month = px.bar(monthly_sales, x="Month", y=sales_col, title="Monthly Sales")
    st.plotly_chart(fig_month, use_container_width=True)

    # -------------------------------
    # 📆 Day-wise Pattern
    # -------------------------------
    st.subheader("📆 Day-wise Sales Pattern")

    df["Day"] = df[date_col].dt.day_name()
    day_sales = df.groupby("Day")[sales_col].mean().reindex(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    ).reset_index()

    fig_day = px.bar(day_sales, x="Day", y=sales_col, title="Average Sales by Day")
    st.plotly_chart(fig_day, use_container_width=True)

    # -------------------------------
    # 🔍 Data Quality Check
    # -------------------------------
    st.subheader("🧹 Data Quality Check")

    col1, col2 = st.columns(2)

    with col1:
        st.write("Missing Values:")
        st.write(df.isnull().sum())

    with col2:
        st.write("Dataset Shape:")
        st.write(df.shape)

    # -------------------------------
    # 🤖 Auto Insights
    # -------------------------------
    st.subheader("🤖 AI-Generated Insights")

    insights = generate_insights(df, date_col, sales_col)

    for insight in insights:
        st.info(insight)

    # -------------------------------
    # 📈 Quick Forecast (Bonus)
    # -------------------------------
    st.subheader("🔮 Quick Forecast (Next 10 Steps)")

    try:
        from statsmodels.tsa.holtwinters import ExponentialSmoothing

        model = ExponentialSmoothing(df[sales_col]).fit()
        forecast = model.forecast(10)

        forecast_df = pd.DataFrame({
            "Step": range(1, 11),
            "Forecast": forecast
        })

        fig_forecast = px.line(forecast_df, x="Step", y="Forecast", title="Future Forecast")
        st.plotly_chart(fig_forecast, use_container_width=True)

    except Exception as e:
        st.warning("Forecasting failed. Check data format.")

    # -------------------------------
    # 📥 Download Clean Data
    # -------------------------------
    st.subheader("📥 Download Data")

    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Processed Data",
        data=csv,
        file_name="processed_data.csv",
        mime="text/csv"
    )

else:
    st.info("👆 Upload a CSV file to begin analysis.")