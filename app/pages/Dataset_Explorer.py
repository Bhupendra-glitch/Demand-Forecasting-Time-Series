import streamlit as st
import pandas as pd

st.set_page_config(page_title="Dataset Explorer", layout="wide")

st.title("📊 Dataset Explorer")
st.markdown("Explore your dataset with filters, statistics, and downloads 🚀")

# -------------------------------
# 📂 Upload File
# -------------------------------
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], key="explorer")

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    # -------------------------------
    # 📊 Basic Info
    # -------------------------------
    st.subheader("📌 Dataset Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing Values", int(df.isnull().sum().sum()))

    # -------------------------------
    # 🔍 Column Selection
    # -------------------------------
    st.subheader("🔎 Select Columns to View")

    selected_columns = st.multiselect(
        "Choose columns",
        options=df.columns,
        default=df.columns[:5]
    )

    if selected_columns:
        df_display = df[selected_columns]
    else:
        df_display = df

    # -------------------------------
    # 🎯 Filters
    # -------------------------------
    st.subheader("🎯 Apply Filters")

    filter_column = st.selectbox("Select column to filter", df.columns)

    if df[filter_column].dtype == "object":
        selected_values = st.multiselect(
            f"Select values for {filter_column}",
            options=df[filter_column].unique()
        )
        if selected_values:
            df_display = df_display[df[filter_column].isin(selected_values)]

    else:
        min_val = float(df[filter_column].min())
        max_val = float(df[filter_column].max())

        selected_range = st.slider(
            f"Select range for {filter_column}",
            min_val,
            max_val,
            (min_val, max_val)
        )

        df_display = df_display[
            (df[filter_column] >= selected_range[0]) &
            (df[filter_column] <= selected_range[1])
        ]

    # -------------------------------
    # 📋 Data Display
    # -------------------------------
    st.subheader("📋 Filtered Data")
    st.dataframe(df_display, use_container_width=True)

    # -------------------------------
    # 📈 Summary Statistics
    # -------------------------------
    st.subheader("📈 Summary Statistics")
    st.write(df.describe())

    # -------------------------------
    # 🧹 Missing Values
    # -------------------------------
    st.subheader("🧹 Missing Values per Column")
    st.write(df.isnull().sum())

    # -------------------------------
    # 📊 Data Types
    # -------------------------------
    st.subheader("📊 Data Types")
    st.write(df.dtypes)

    # -------------------------------
    # 📥 Download Filtered Data
    # -------------------------------
    st.subheader("📥 Download Filtered Data")

    csv = df_display.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="Download CSV",
        data=csv,
        file_name="filtered_data.csv",
        mime="text/csv"
    )

else:
    st.info("👆 Upload a CSV file to explore your dataset.")