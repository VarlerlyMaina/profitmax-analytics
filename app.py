from flask import Flask, jsonify, request
import numpy as np
import pandas as pd
from scipy.optimize import minimize

app = Flask(__name__)

# Sample Pricing Data
pricing_data = {
    "product": ["Beer", "Whiskey", "Gin"],
    "cost_price": [100, 250, 150],
    "base_selling_price": [150, 400, 250],
    "demand_sensitivity": [-0.3, -0.4, -0.35]  # How demand drops with price increase
}

df = pd.DataFrame(pricing_data)

# Function to Optimize Pricing for Maximum Profit
def optimize_price(cost_price, base_price, demand_sensitivity):
    def profit_function(price):
        demand = 1000 * (1 + demand_sensitivity * (price - base_price) / base_price)
        revenue = price * demand
        cost = cost_price * demand
        return -(revenue - cost)  # Negative because we minimize in scipy

    result = minimize(profit_function, base_price, method="Nelder-Mead")
    return round(result.x[0], 2) if result.success else base_price

# Apply Optimization Model
df["optimized_price"] = df.apply(
    lambda row: optimize_price(row["cost_price"], row["base_selling_price"], row["demand_sensitivity"]), axis=1
)

@app.route("/pricing_optimization", methods=["GET"])
def get_pricing_recommendation():
    return jsonify(df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True)



