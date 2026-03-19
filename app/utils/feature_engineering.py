import pandas as pd

def create_time_features(df, date_col):
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], errors="coerce")

    df["year"] = df[date_col].dt.year
    df["month"] = df[date_col].dt.month
    df["day"] = df[date_col].dt.day
    df["day_of_week"] = df[date_col].dt.day_name()

    return df


def create_lag_features(df, col, lags=[1, 7, 14]):
    df = df.copy()

    for lag in lags:
        df[f"lag_{lag}"] = df[col].shift(lag)

    return df


def rolling_features(df, col, windows=[3, 7]):
    df = df.copy()

    for w in windows:
        df[f"rolling_mean_{w}"] = df[col].rolling(w).mean()

    return df
