import pandas as pd

def load_data(file, nrows=None):
    try:
        df = pd.read_csv(file, nrows=nrows)
        return df
    except Exception as e:
        raise Exception("Error loading file")


def detect_basic_info(df):
    return {
        "rows": df.shape[0],
        "cols": df.shape[1],
        "missing": int(df.isnull().sum().sum())
    }
