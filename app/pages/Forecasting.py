import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error

st.set_page_config(page_title="Forecasting", layout="wide")

st.title("🤖 Demand Forecasting")
st.markdown("Train models and forecast future sales 📈")

# -------------------------------
# 📂 Upload File
# -------------------------------
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], key="forecast")

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
        st.error("❌ No numeric column found for forecasting")
        st.stop()

    date_col = st.selectbox("Select Date Column", date_cols if date_cols else df.columns)
    target_col = st.selectbox("Select Target (Sales)", numeric_cols)

    # -------------------------------
    # 🧹 Preprocessing
    # -------------------------------
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col])
    df = df.sort_values(by=date_col)

    ts = df.set_index(date_col)[target_col]

    # -------------------------------
    # ⚙️ Model Selection
    # -------------------------------
    st.sidebar.header("⚙️ Model Settings")

    model_name = st.sidebar.selectbox(
        "Choose Model",
        ["Exponential Smoothing", "ARIMA"]
    )

    forecast_steps = st.sidebar.slider("Forecast Horizon", 5, 60, 20)

    # -------------------------------
    # ✂️ Train/Test Split
    # -------------------------------
    split_ratio = st.sidebar.slider("Train Size (%)", 60, 90, 80)
    split_index = int(len(ts) * split_ratio / 100)

    train, test = ts[:split_index], ts[split_index:]

    # -------------------------------
    # 🤖 Model Training
    # -------------------------------
    st.subheader("🤖 Model Training & Forecasting")

    try:
        if model_name == "Exponential Smoothing":
            model = ExponentialSmoothing(train).fit()
            forecast = model.forecast(len(test) + forecast_steps)

        elif model_name == "ARIMA":
            p = st.sidebar.slider("p", 0, 5, 1)
            d = st.sidebar.slider("d", 0, 2, 1)
            q = st.sidebar.slider("q", 0, 5, 1)

            model = ARIMA(train, order=(p, d, q)).fit()
            forecast = model.forecast(len(test) + forecast_steps)

        # -------------------------------
        # 📊 Evaluation
        # -------------------------------
        pred_test = forecast[:len(test)]

        mae = mean_absolute_error(test, pred_test)
        rmse = np.sqrt(mean_squared_error(test, pred_test))

        col1, col2 = st.columns(2)
        col1.metric("MAE", f"{mae:.2f}")
        col2.metric("RMSE", f"{rmse:.2f}")

        # -------------------------------
        # 📈 Plot Results
        # -------------------------------
        st.subheader("📈 Forecast Results")

        fig = go.Figure()

        fig.add_trace(go.Scatter(x=train.index, y=train, name="Train"))
        fig.add_trace(go.Scatter(x=test.index, y=test, name="Test"))
        fig.add_trace(go.Scatter(x=test.index, y=pred_test, name="Predicted"))

        future_index = pd.date_range(
            start=test.index[-1],
            periods=forecast_steps + 1,
            freq="D"
        )[1:]

        fig.add_trace(go.Scatter(
            x=future_index,
            y=forecast[-forecast_steps:],
            name="Future Forecast"
        ))

        fig.update_layout(title="Forecast vs Actual", xaxis_title="Date", yaxis_title="Sales")

        st.plotly_chart(fig, use_container_width=True)

        # -------------------------------
        # 📥 Download Forecast
        # -------------------------------
        st.subheader("📥 Download Forecast")

        forecast_df = pd.DataFrame({
            "Date": future_index,
            "Forecast": forecast[-forecast_steps:]
        })

        csv = forecast_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Forecast CSV",
            data=csv,
            file_name="forecast.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error("❌ Model failed. Try different parameters or clean data.")

else:
    st.info("👆 Upload a CSV file to perform forecasting.")