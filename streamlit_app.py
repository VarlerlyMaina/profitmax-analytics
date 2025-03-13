import streamlit as st
import pandas as pd
import requests

# Streamlit App Title
st.title("📊 Financial Risk & Pricing Optimization Tool")

# API URL (Flask Backend)
API_URL = "http://127.0.0.1:5000/pricing_optimization"

# Fetch data from Flask API
st.sidebar.header("🔄 Refresh Data")
if st.sidebar.button("Get Latest Pricing Data"):
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)

        # Display Data in a Table
        st.subheader("📋 Optimized Pricing Table")
        st.dataframe(df)

        # Visualize Pricing Optimization
        st.subheader("📈 Price vs Optimized Price")
        st.bar_chart(df.set_index("product")[["base_selling_price", "optimized_price"]])

        # Show Demand Sensitivity
        st.subheader("📉 Demand Sensitivity Impact")
        st.line_chart(df.set_index("product")[["demand_sensitivity"]])
    else:
        st.error("❌ Failed to fetch data from API")



