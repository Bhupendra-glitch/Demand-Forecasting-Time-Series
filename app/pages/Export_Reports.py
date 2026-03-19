import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Export Reports", layout="wide")

st.title("📥 Export Reports")
st.markdown("Download your analysis, forecasts, and insights 📊")

# -------------------------------
# 📂 Upload Dataset
# -------------------------------
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], key="export")

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
    # 📊 Generate Summary
    # -------------------------------
    total_sales = df[sales_col].sum()
    avg_sales = df[sales_col].mean()
    max_sales = df[sales_col].max()
    min_sales = df[sales_col].min()

    summary = f"""
📊 Demand Forecasting Report
Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

-----------------------------
Total Sales: {total_sales:,.2f}
Average Sales: {avg_sales:,.2f}
Max Sales: {max_sales:,.2f}
Min Sales: {min_sales:,.2f}
"""

    # -------------------------------
    # 📈 Plot
    # -------------------------------
    fig = px.line(df, x=date_col, y=sales_col, title="Sales Trend")

    st.subheader("📈 Sales Trend")
    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------
    # 📥 Download Options
    # -------------------------------
    st.subheader("📥 Download Options")

    # 1️⃣ Download Raw Data
    csv_raw = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Raw Data",
        data=csv_raw,
        file_name="raw_data.csv",
        mime="text/csv"
    )

    # 2️⃣ Download Summary Report
    st.download_button(
        label="Download Summary Report (TXT)",
        data=summary,
        file_name="report.txt",
        mime="text/plain"
    )

    # 3️⃣ Download Chart Image (Workaround)
    st.info("To download chart: Right-click → Save Image")

    # -------------------------------
    # 📊 Forecast Export (Optional)
    # -------------------------------
    st.subheader("🔮 Forecast Export (Optional)")

    if st.button("Generate Simple Forecast"):

        from statsmodels.tsa.holtwinters import ExponentialSmoothing

        model = ExponentialSmoothing(df[sales_col]).fit()
        forecast = model.forecast(10)

        forecast_df = pd.DataFrame({
            "Step": range(1, 11),
            "Forecast": forecast
        })

        st.dataframe(forecast_df)

        csv_forecast = forecast_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Forecast CSV",
            data=csv_forecast,
            file_name="forecast.csv",
            mime="text/csv"
        )

else:
    st.info("👆 Upload a dataset to export reports.")