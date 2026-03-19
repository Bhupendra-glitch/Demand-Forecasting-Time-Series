import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff

st.set_page_config(page_title="EDA Dashboard", layout="wide")

st.title("📈 Exploratory Data Analysis (EDA)")
st.markdown("Interactive dashboard to explore trends, patterns, and relationships 🚀")

# -------------------------------
# 📂 Upload File
# -------------------------------
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"], key="eda")

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("🔍 Data Preview")
    st.dataframe(df.head())

    # -------------------------------
    # 🔢 Select Columns
    # -------------------------------
    numeric_cols = df.select_dtypes(include='number').columns.tolist()
    cat_cols = df.select_dtypes(include='object').columns.tolist()

    st.sidebar.header("⚙️ Controls")

    selected_num = st.sidebar.selectbox("Select Numeric Column", numeric_cols)
    selected_cat = st.sidebar.selectbox("Select Categorical Column", cat_cols if cat_cols else ["None"])

    # -------------------------------
    # 📊 KPI Section
    # -------------------------------
    st.subheader("📊 Key Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Mean", f"{df[selected_num].mean():.2f}")
    col2.metric("Median", f"{df[selected_num].median():.2f}")
    col3.metric("Max", f"{df[selected_num].max():.2f}")
    col4.metric("Min", f"{df[selected_num].min():.2f}")

    # -------------------------------
    # 📈 Distribution Plot
    # -------------------------------
    st.subheader("📈 Distribution")

    fig_hist = px.histogram(df, x=selected_num, nbins=50, title="Histogram")
    st.plotly_chart(fig_hist, use_container_width=True)

    fig_box = px.box(df, y=selected_num, title="Box Plot")
    st.plotly_chart(fig_box, use_container_width=True)

    # -------------------------------
    # 🔗 Correlation Heatmap
    # -------------------------------
    st.subheader("🔗 Correlation Heatmap")

    if len(numeric_cols) > 1:
        corr = df[numeric_cols].corr()

        fig_corr = px.imshow(
            corr,
            text_auto=True,
            title="Correlation Matrix",
            aspect="auto"
        )
        st.plotly_chart(fig_corr, use_container_width=True)
    else:
        st.info("Not enough numeric columns for correlation.")

    # -------------------------------
    # 📊 Category-wise Analysis
    # -------------------------------
    if selected_cat != "None":
        st.subheader("📊 Category-wise Analysis")

        grouped = df.groupby(selected_cat)[selected_num].mean().reset_index()

        fig_bar = px.bar(
            grouped,
            x=selected_cat,
            y=selected_num,
            title=f"{selected_num} by {selected_cat}"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    # -------------------------------
    # 📈 Scatter Plot
    # -------------------------------
    st.subheader("📈 Scatter Plot")

    if len(numeric_cols) > 1:
        x_axis = st.selectbox("X-axis", numeric_cols, key="x")
        y_axis = st.selectbox("Y-axis", numeric_cols, key="y")

        fig_scatter = px.scatter(df, x=x_axis, y=y_axis, title="Scatter Plot")
        st.plotly_chart(fig_scatter, use_container_width=True)

    # -------------------------------
    # 📅 Time Series Analysis (if date exists)
    # -------------------------------
    st.subheader("📅 Time Series Analysis")

    date_cols = [col for col in df.columns if "date" in col.lower()]

    if date_cols:
        date_col = st.selectbox("Select Date Column", date_cols)
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

        ts_col = st.selectbox("Select Value Column", numeric_cols)

        df = df.sort_values(date_col)

        fig_ts = px.line(df, x=date_col, y=ts_col, title="Time Series Trend")
        st.plotly_chart(fig_ts, use_container_width=True)

    else:
        st.info("No date column detected for time series.")

else:
    st.info("👆 Upload a CSV file to start EDA.")