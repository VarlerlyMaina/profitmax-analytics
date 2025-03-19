import streamlit as st
import pandas as pd
import requests
import plotly.express as px  # For interactive charts
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

# Define API URL
API_URL = API_URL = "https://profitmax-api.onrender.com/pricing_optimization"


# **Ensure Streamlit updates the product selection properly**
if "df" not in st.session_state:
    st.session_state.df = None

if "selected_product" not in st.session_state:
    st.session_state.selected_product = None

# **Fetch data from Flask API when button is clicked**
if st.sidebar.button("Get Latest Pricing Data"):
    response = requests.get(API_URL)
    if response.status_code == 200:
        data = response.json()
        st.session_state.df = pd.DataFrame(data)  # Store the fetched data in session state
        st.session_state.selected_product = None  # Reset product selection when fetching new data

# **Ensure we have data before proceeding**
if st.session_state.df is not None and not st.session_state.df.empty and "product" in st.session_state.df.columns:
    
    # **Product selection filter**
    selected_product = st.sidebar.selectbox("🔍 Select a Product:", st.session_state.df["product"].unique())

    # **Store selected product in session state**
    if selected_product != st.session_state.selected_product:
        st.session_state.selected_product = selected_product

    # **Filter the data for the selected product**
    filtered_df = st.session_state.df[st.session_state.df["product"] == st.session_state.selected_product].copy()

    # **Display Data in a Styled Table**
    st.subheader(f"📋 Optimized Pricing for {st.session_state.selected_product}")
    styled_df = filtered_df.style.set_table_styles(
        [{"selector": "th", "props": [("background-color", "#007bff"), ("color", "white")]}]
    ).set_properties(**{"text-align": "center"})
    st.dataframe(styled_df)

    # **Visualizing Pricing Optimization (Base vs Optimized Prices)**
    df_long = filtered_df.melt(id_vars=["product"], value_vars=["base_selling_price", "optimized_price"],
                               var_name="Price Type", value_name="Price")

    fig = px.bar(
        df_long,
        x="Price",
        y="product",
        color="Price Type",
        title=f"Base vs Optimized Price for {st.session_state.selected_product}",
        labels={"Price": "Price Value", "product": "Product"},
        barmode="group",
        height=500
    )
    st.plotly_chart(fig)

    # **Show Demand Sensitivity Curve**
    if not filtered_df.empty and "demand_sensitivity" in filtered_df.columns:
        filtered_df["demand_loss"] = (filtered_df["demand_sensitivity"] * filtered_df["optimized_price"]).round(2)
        fig2 = px.line(
            filtered_df,
            x="optimized_price",
            y="demand_loss",
            title=f"Demand Sensitivity Curve for {st.session_state.selected_product}",
            labels={"optimized_price": "Optimized Price", "demand_loss": "Demand Loss"},
            markers=True,
            line_shape="spline",
            height=500
        )
        st.plotly_chart(fig2)
    else:
        st.warning(f"⚠️ No demand sensitivity data available for {st.session_state.selected_product}.")

    # **Tax Impact Analysis**
    st.subheader("💰 Tax Impact Analysis")
    tax_rate = 0.16
    filtered_df["tax_amount"] = filtered_df["optimized_price"] * tax_rate
    filtered_df["final_price_after_tax"] = filtered_df["optimized_price"] + filtered_df["tax_amount"]
    st.dataframe(filtered_df[["product", "optimized_price", "tax_amount", "final_price_after_tax"]])

    # **Profitability Forecasting**
    if not filtered_df.empty and "optimized_price" in filtered_df.columns:
        st.subheader("📊 Profitability Forecast")
        filtered_df["expected_revenue"] = filtered_df["optimized_price"] * 1000
        fig3 = px.line(
            filtered_df,
            x="optimized_price",
            y="expected_revenue",
            title=f"Profitability Projection for {st.session_state.selected_product}",
            labels={"optimized_price": "Optimized Price", "expected_revenue": "Expected Revenue"},
            markers=True,
            line_shape="spline",
            height=500
        )
        st.plotly_chart(fig3)
    else:
        st.warning(f"⚠️ No pricing data available for {st.session_state.selected_product}.")

    # **Break-even Analysis**
    if not filtered_df.empty and "optimized_price" in filtered_df.columns:
        st.subheader("⚖️ Break-even Analysis")
        fixed_costs = 50000
        variable_cost = filtered_df["optimized_price"] * 0.3
        filtered_df["break_even_units"] = fixed_costs / (filtered_df["optimized_price"] - variable_cost)

        fig4 = px.bar(
            filtered_df,
            x="product",
            y="break_even_units",
            title=f"Break-even Analysis for {st.session_state.selected_product}",
            labels={"break_even_units": "Break-even Units"},
            color_discrete_sequence=["#FFA07A"],
            height=500
        )
        st.plotly_chart(fig4)
    else:
        st.warning(f"⚠️ No break-even data available for {st.session_state.selected_product}.")

else:
    st.warning("⚠️ No data available. Click 'Get Latest Pricing Data' to load data.")

