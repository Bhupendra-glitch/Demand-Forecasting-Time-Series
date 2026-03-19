import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from statsmodels.tsa.holtwinters import ExponentialSmoothing

st.set_page_config(page_title="Live Forecast", layout="wide")

st.title("📊 Live Forecast Simulator")
st.markdown("Interactively forecast future demand based on your data 🔮")

# -------------------------------
# 📂 Upload Dataset
# -------------------------------
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], key="live_forecast")

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
        st.error("❌ No numeric column available")
        st.stop()

    date_col = st.selectbox("Select Date Column", date_cols if date_cols else df.columns)
    target_col = st.selectbox("Select Sales Column", numeric_cols)

    # -------------------------------
    # 🧹 Preprocessing
    # -------------------------------
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col])
    df = df.sort_values(by=date_col)

    ts = df.set_index(date_col)[target_col]

    # -------------------------------
    # ⚙️ User Controls
    # -------------------------------
    st.sidebar.header("⚙️ Forecast Settings")

    forecast_days = st.sidebar.slider("Forecast Days", 7, 90, 30)
    seasonal = st.sidebar.checkbox("Use Seasonality", value=False)

    # -------------------------------
    # 🤖 Model Training
    # -------------------------------
    try:
        if seasonal and len(ts) > 30:
            model = ExponentialSmoothing(ts, seasonal="add", seasonal_periods=7).fit()
        else:
            model = ExponentialSmoothing(ts).fit()

        forecast = model.forecast(forecast_days)

        # -------------------------------
        # 📅 Future Dates
        # -------------------------------
        last_date = ts.index[-1]

        future_dates = pd.date_range(
            start=last_date,
            periods=forecast_days + 1,
            freq="D"
        )[1:]

        # -------------------------------
        # 📊 Plot Forecast
        # -------------------------------
        st.subheader("📈 Forecast Visualization")

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=ts.index,
            y=ts,
            name="Historical Data"
        ))

        fig.add_trace(go.Scatter(
            x=future_dates,
            y=forecast,
            name="Forecast",
            line=dict(dash="dash")
        ))

        fig.update_layout(
            title="Live Forecast",
            xaxis_title="Date",
            yaxis_title="Sales"
        )

        st.plotly_chart(fig, use_container_width=True)

        # -------------------------------
        # 📊 Forecast Summary
        # -------------------------------
        st.subheader("📊 Forecast Summary")

        col1, col2, col3 = st.columns(3)

        col1.metric("Avg Forecast", f"{forecast.mean():.2f}")
        col2.metric("Max Forecast", f"{forecast.max():.2f}")
        col3.metric("Min Forecast", f"{forecast.min():.2f}")

        # -------------------------------
        # 📥 Download Forecast
        # -------------------------------
        st.subheader("📥 Download Forecast Data")

        forecast_df = pd.DataFrame({
            "Date": future_dates,
            "Forecast": forecast
        })

        csv = forecast_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Forecast CSV",
            data=csv,
            file_name="live_forecast.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error("❌ Forecasting failed. Please check your dataset.")

else:
    st.info("👆 Upload a dataset to generate live forecast.")