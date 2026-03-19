import streamlit as st

def show_kpi_metrics(total, avg, max_val, min_val):
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💰 Total Sales", f"{total:,.2f}")
    col2.metric("📊 Avg Sales", f"{avg:,.2f}")
    col3.metric("📈 Max Sales", f"{max_val:,.2f}")
    col4.metric("📉 Min Sales", f"{min_val:,.2f}")


def show_basic_metrics(df):
    col1, col2, col3 = st.columns(3)

    col1.metric("Rows", df.shape[0])
    col2.metric("Columns", df.shape[1])
    col3.metric("Missing", int(df.isnull().sum().sum()))