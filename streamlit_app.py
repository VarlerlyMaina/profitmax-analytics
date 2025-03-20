import streamlit as st
import pandas as pd
import requests
import plotly.express as px
from PIL import Image  # Import Image module

# Load and display the logo
logo = Image.open("profitmax_logo.png")

# Professional-looking UI header
st.markdown(
    '<div style="background-color:#007bff;padding:20px;border-radius:10px;text-align:center;color:white;font-size:24px;font-weight:bold;">🚀 ProfitMax Analytics – Smart Pricing & Risk Optimization</div>',
    unsafe_allow_html=True
)

# Structured layout with columns for a clean design
col1, col2 = st.columns([1, 4])
with col1:
    st.image(logo, width=120)  # Display logo on the left
with col2:
    st.markdown("### Maximizing Profitability Through Data-Driven Pricing Strategies 💡")

# Sidebar with branding and filters
st.sidebar.markdown("## 🌟 ProfitMax Analytics")
st.sidebar.image(logo, width=100)
st.sidebar.markdown("### Unlock Smart Pricing Strategies")
st.sidebar.divider()
st.sidebar.header("🔄 Refresh Data")

# Define API URL (Make sure this is correct)
API_URL = "https://profitmax-analytics.onrender.com/pricing_optimization"

# Product selection
st.sidebar.markdown("## 🔍 Select a Product")
product = st.sidebar.selectbox("Choose a product:", ["Beer", "Whiskey", "Gin"])

# **Fetch data from Flask API**
if st.sidebar.button("Get Latest Pricing Data"):
    response = requests.get(f"{API_URL}?product={product}")
    if response.status_code == 200:
        data = response.json()
        st.session_state.product_data = data  # Store in session state
    else:
        st.error("🚨 Failed to fetch data from API. Please try again.")

# Ensure data is available before proceeding
if "product_data" in st.session_state:
    data = st.session_state.product_data

    # Display optimized pricing details
    st.markdown(f"<h2 style='color: #4CAF50;'>📈 Pricing Optimization for {product}</h2>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)

    col1.metric("💰 Optimal Price", f"Ksh {data['optimal_price']}")
    col2.metric("📊 Profit Margin", f"{data['profit_margin']}%")
    col3.metric("📉 Demand Sensitivity", f"{data['demand_sensitivity']}")

    # Create a DataFrame for visualization
    df = pd.DataFrame([{
        "Price Points": data["optimal_price"],
        "Profit Margin (%)": data["profit_margin"],
        "Demand Sensitivity": data["demand_sensitivity"]
    }])

    # Create an interactive line chart
    fig = px.line(df, x="Price Points", y="Profit Margin (%)", markers=True,
                  title=f"📊 Profit Margin Analysis for {product}")
    fig.update_traces(line=dict(color="green", width=3), marker=dict(size=8, color="red"))
    st.plotly_chart(fig, use_container_width=True)

    # Tax Impact Analysis
    st.subheader("💰 Tax Impact Analysis")
    tax_rate = 0.16
    df["Tax Amount"] = df["Price Points"] * tax_rate
    df["Final Price After Tax"] = df["Price Points"] + df["Tax Amount"]
    st.dataframe(df)

    # Profitability Forecasting
    st.subheader("📊 Profitability Forecast")
    df["Expected Revenue"] = df["Price Points"] * 1000
    fig2 = px.line(df, x="Price Points", y="Expected Revenue", title=f"📈 Revenue Projection for {product}",
                   labels={"Price Points": "Optimized Price", "Expected Revenue": "Expected Revenue"},
                   markers=True, line_shape="spline")
    st.plotly_chart(fig2)

    # Break-even Analysis
    st.subheader("⚖️ Break-even Analysis")
    fixed_costs = 50000
    variable_cost = df["Price Points"] * 0.3
    df["Break-even Units"] = fixed_costs / (df["Price Points"] - variable_cost)

    fig3 = px.bar(df, x="Price Points", y="Break-even Units", title=f"Break-even Analysis for {product}",
                  labels={"Break-even Units": "Break-even Units Needed"},
                  color_discrete_sequence=["#FFA07A"])
    st.plotly_chart(fig3)

else:
    st.warning("⚠️ No data available. Click 'Get Latest Pricing Data' to load data.")

# Footer
st.markdown("<br><hr><p style='text-align: center;'>🚀 Powered by ProfitMax Analytics</p>", unsafe_allow_html=True)
