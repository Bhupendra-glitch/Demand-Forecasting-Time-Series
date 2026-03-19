import pandas as pd
import numpy as np

def handle_missing(df, method="none"):
    df = df.copy()

    if method == "drop":
        df = df.dropna()

    elif method == "ffill":
        df = df.fillna(method="ffill")

    elif method == "bfill":
        df = df.fillna(method="bfill")

    elif method == "mean":
        num_cols = df.select_dtypes(include=np.number).columns
        df[num_cols] = df[num_cols].fillna(df[num_cols].mean())

    return df


def remove_outliers(df, col):
    q1 = df[col].quantile(0.25)
    q3 = df[col].quantile(0.75)
    iqr = q3 - q1

    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr

    return df[(df[col] >= lower) & (df[col] <= upper)]
