import streamlit as st

def render_sidebar():
    st.sidebar.title("📊 Demand Forecasting")
    st.sidebar.markdown("---")

    st.sidebar.markdown("### 🚀 Navigation")
    st.sidebar.info("Use the sidebar to explore different modules")

    st.sidebar.markdown("---")

    st.sidebar.markdown("### 📌 About")
    st.sidebar.write(
        "This app provides demand forecasting, insights, and analytics "
        "using time series techniques."
    )

    st.sidebar.markdown("---")
    st.sidebar.caption("Made with ❤️ using Streamlit")