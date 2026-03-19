import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Data Preprocessing", layout="wide")

st.title("🧹 Data Preprocessing")
st.markdown("Clean, transform, and prepare your data for analysis 🚀")

# -------------------------------
# 📂 Upload File
# -------------------------------
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], key="prep")

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("🔍 Original Data")
    st.dataframe(df.head())

    # -------------------------------
    # 📊 Missing Values
    # -------------------------------
    st.subheader("🧩 Missing Values")

    missing = df.isnull().sum()
    st.write(missing)

    # -------------------------------
    # 🛠️ Handle Missing Values
    # -------------------------------
    st.subheader("⚙️ Handle Missing Values")

    method = st.selectbox(
        "Choose method",
        ["None", "Drop Rows", "Forward Fill", "Backward Fill", "Fill with Mean"]
    )

    df_clean = df.copy()

    if method == "Drop Rows":
        df_clean = df_clean.dropna()

    elif method == "Forward Fill":
        df_clean = df_clean.fillna(method="ffill")

    elif method == "Backward Fill":
        df_clean = df_clean.fillna(method="bfill")

    elif method == "Fill with Mean":
        num_cols = df_clean.select_dtypes(include=np.number).columns
        df_clean[num_cols] = df_clean[num_cols].fillna(df_clean[num_cols].mean())

    st.success(f"Applied: {method}")

    # -------------------------------
    # 📊 After Cleaning
    # -------------------------------
    st.subheader("✅ Cleaned Data Preview")
    st.dataframe(df_clean.head())

    # -------------------------------
    # 📉 Outlier Detection
    # -------------------------------
    st.subheader("📉 Outlier Detection")

    numeric_cols = df_clean.select_dtypes(include=np.number).columns.tolist()

    if numeric_cols:
        col = st.selectbox("Select column", numeric_cols)

        q1 = df_clean[col].quantile(0.25)
        q3 = df_clean[col].quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = df_clean[(df_clean[col] < lower) | (df_clean[col] > upper)]

        st.write(f"Outliers detected: {len(outliers)}")

        # Option to remove outliers
        if st.checkbox("Remove Outliers"):
            df_clean = df_clean[(df_clean[col] >= lower) & (df_clean[col] <= upper)]
            st.success("Outliers removed")

    else:
        st.info("No numeric columns available")

    # -------------------------------
    # 🔄 Feature Engineering
    # -------------------------------
    st.subheader("🔄 Feature Engineering")

    date_cols = [c for c in df_clean.columns if "date" in c.lower()]

    if date_cols:
        date_col = st.selectbox("Select Date Column", date_cols)

        df_clean[date_col] = pd.to_datetime(df_clean[date_col], errors="coerce")

        if st.checkbox("Extract Date Features"):
            df_clean["Year"] = df_clean[date_col].dt.year
            df_clean["Month"] = df_clean[date_col].dt.month
            df_clean["Day"] = df_clean[date_col].dt.day
            df_clean["DayOfWeek"] = df_clean[date_col].dt.day_name()

            st.success("Date features added")

    # -------------------------------
    # 📊 Final Dataset Info
    # -------------------------------
    st.subheader("📊 Final Dataset Info")

    col1, col2 = st.columns(2)

    col1.write("Shape:", df_clean.shape)
    col2.write("Missing Values:", df_clean.isnull().sum().sum())

    # -------------------------------
    # 📥 Download Clean Data
    # -------------------------------
    st.subheader("📥 Download Cleaned Data")

    csv = df_clean.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="cleaned_data.csv",
        mime="text/csv"
    )

else:
    st.info("👆 Upload a CSV file to preprocess your data.")