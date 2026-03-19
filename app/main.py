import streamlit as st

# -------------------------------
# ⚙️ Page Configuration
# -------------------------------
st.set_page_config(
    page_title="Demand Forecasting App",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------
# 🎯 Sidebar
# -------------------------------
st.sidebar.title("📊 Demand Forecasting")
st.sidebar.markdown("---")
st.sidebar.info("Navigate using the sidebar pages")

# -------------------------------
# 🏠 Main Page (Home)
# -------------------------------
st.title("📊 Demand Forecasting Dashboard")

st.markdown("""
Welcome to your **AI-powered Demand Forecasting System** 🚀

This application allows you to:

- 📂 Upload any sales dataset
- 🧠 Automatically generate insights
- 📊 Perform interactive EDA
- 🤖 Forecast future demand
- 🎯 Get business recommendations
""")

# -------------------------------
# 📊 KPI Section
# -------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("📂 Data Support", "Any CSV")
col2.metric("🤖 Models", "ARIMA / ETS")
col3.metric("⚡ Insights", "Auto Generated")

# -------------------------------
# 🔥 Features Section
# -------------------------------
st.markdown("---")
st.subheader("🔥 Key Features")

st.markdown("""
- **Upload & Auto Insights** → Instant analysis from any dataset  
- **EDA Dashboard** → Trends, seasonality & patterns  
- **Forecasting Models** → Predict future sales  
- **Business Insights** → Actionable recommendations  
- **Export Reports** → Download results  
""")

# -------------------------------
# 📌 How to Use
# -------------------------------
st.markdown("---")
st.subheader("📌 How to Use")

st.markdown("""
1. Go to **📂 Upload & Auto Insights**
2. Upload your dataset (CSV)
3. Explore generated insights
4. Move to **Forecasting** for predictions
""")

# -------------------------------
# ✅ Footer
# -------------------------------
st.success("✅ Ready to explore! Use the sidebar to navigate.")