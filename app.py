from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# Sample data (Replace with real pricing optimization logic)
pricing_data = {
    "Beer": {"optimal_price": 250, "profit_margin": 30, "demand_sensitivity": 0.8},
    "Whiskey": {"optimal_price": 1000, "profit_margin": 40, "demand_sensitivity": 0.6},
    "Gin": {"optimal_price": 800, "profit_margin": 35, "demand_sensitivity": 0.7},
}

@app.route("/")
def home():
    return "ProfitMax API is running!"

@app.route("/pricing_optimization", methods=["GET"])
def pricing_optimization():
    product = request.args.get("product")  # Get product from request
    if product in pricing_data:
        return jsonify(pricing_data[product])  # Return data for selected product
    else:
        return jsonify({"error": "Product not found"}), 404  # Handle unknown products

if __name__ == "__main__":
    from waitress import serve
    import os
    port = int(os.environ.get("PORT", 5000))
    serve(app, host="0.0.0.0", port=port)

