import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error

st.set_page_config(page_title="Model Comparison", layout="wide")

st.title("⚔️ Model Comparison")
st.markdown("Compare multiple forecasting models and find the best one 🏆")

# -------------------------------
# 📂 Upload File
# -------------------------------
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], key="compare")

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
    target_col = st.selectbox("Select Target Column", numeric_cols)

    # -------------------------------
    # 🧹 Preprocessing
    # -------------------------------
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")
    df = df.dropna(subset=[date_col])
    df = df.sort_values(by=date_col)

    ts = df.set_index(date_col)[target_col]

    # -------------------------------
    # ⚙️ Settings
    # -------------------------------
    st.sidebar.header("⚙️ Settings")

    split_ratio = st.sidebar.slider("Train Size (%)", 60, 90, 80)
    split_index = int(len(ts) * split_ratio / 100)

    train, test = ts[:split_index], ts[split_index:]

    forecast_steps = st.sidebar.slider("Forecast Horizon", 5, 50, 20)

    # -------------------------------
    # 🤖 Model Comparison
    # -------------------------------
    st.subheader("🤖 Running Models...")

    results = []

    try:
        # 🔹 Exponential Smoothing
        model_ets = ExponentialSmoothing(train).fit()
        pred_ets = model_ets.forecast(len(test))

        mae_ets = mean_absolute_error(test, pred_ets)
        rmse_ets = np.sqrt(mean_squared_error(test, pred_ets))

        results.append({
            "Model": "Exponential Smoothing",
            "MAE": mae_ets,
            "RMSE": rmse_ets
        })

        # 🔹 ARIMA
        model_arima = ARIMA(train, order=(1,1,1)).fit()
        pred_arima = model_arima.forecast(len(test))

        mae_arima = mean_absolute_error(test, pred_arima)
        rmse_arima = np.sqrt(mean_squared_error(test, pred_arima))

        results.append({
            "Model": "ARIMA (1,1,1)",
            "MAE": mae_arima,
            "RMSE": rmse_arima
        })

        # -------------------------------
        # 📊 Results Table
        # -------------------------------
        results_df = pd.DataFrame(results)

        st.subheader("📊 Model Performance")
        st.dataframe(results_df)

        # -------------------------------
        # 🏆 Best Model
        # -------------------------------
        best_model = results_df.loc[results_df["RMSE"].idxmin()]

        st.success(f"🏆 Best Model: {best_model['Model']}")

        # -------------------------------
        # 📈 Visualization
        # -------------------------------
        st.subheader("📈 Model Comparison Chart")

        fig = px.bar(
            results_df,
            x="Model",
            y="RMSE",
            color="Model",
            title="RMSE Comparison"
        )

        st.plotly_chart(fig, use_container_width=True)

        # -------------------------------
        # 🔮 Future Forecast (Best Model)
        # -------------------------------
        st.subheader("🔮 Future Forecast (Best Model)")

        if best_model["Model"] == "Exponential Smoothing":
            final_model = ExponentialSmoothing(ts).fit()
        else:
            final_model = ARIMA(ts, order=(1,1,1)).fit()

        future_forecast = final_model.forecast(forecast_steps)

        future_df = pd.DataFrame({
            "Step": range(1, forecast_steps + 1),
            "Forecast": future_forecast
        })

        fig2 = px.line(future_df, x="Step", y="Forecast", title="Future Forecast")
        st.plotly_chart(fig2, use_container_width=True)

        # -------------------------------
        # 📥 Download
        # -------------------------------
        csv = future_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            label="Download Forecast",
            data=csv,
            file_name="best_model_forecast.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error("❌ Error running models. Try different dataset.")

else:
    st.info("👆 Upload a dataset to compare models.")
    