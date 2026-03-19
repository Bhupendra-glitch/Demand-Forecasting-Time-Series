import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA

# -------------------------------
# Exponential Smoothing
# -------------------------------
def ets_model(train, steps):
    model = ExponentialSmoothing(train).fit()
    forecast = model.forecast(steps)
    return forecast


# -------------------------------
# ARIMA
# -------------------------------
def arima_model(train, steps, order=(1,1,1)):
    model = ARIMA(train, order=order).fit()
    forecast = model.forecast(steps)
    return forecast


# -------------------------------
# Train-Test Split
# -------------------------------
def train_test_split(ts, ratio=0.8):
    split = int(len(ts) * ratio)
    return ts[:split], ts[split:]
