from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "ProfitMax API is running!"

@app.route("/pricing_optimization", methods=["GET"])
def pricing_optimization():
    return jsonify({"message": "Pricing optimization data will be here!"})

if __name__ == "__main__":
    from waitress import serve
    import os
    port = int(os.environ.get("PORT", 5000))
    serve(app, host="0.0.0.0", port=port)
