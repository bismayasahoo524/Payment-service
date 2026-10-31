
from flask import Flask, jsonify, request
import os
import uuid

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "application": "SRE Payment API",
        "status": "running"
    }), 200


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy"
    }), 200


@app.route("/payments", methods=["POST"])
def create_payment():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Request body is required"
        }), 400

    amount = data.get("amount")
    currency = data.get("currency")

    if amount is None or currency is None:
        return jsonify({
            "error": "Amount and currency are required"
        }), 400

    try:
        amount = float(amount)
    except (ValueError, TypeError):
        return jsonify({
            "error": "Amount must be a number"
        }), 400

    if amount <= 0:
        return jsonify({
            "error": "Amount must be greater than zero"
        }), 400

    payment_id = str(uuid.uuid4())

    return jsonify({
        "payment_id": payment_id,
        "amount": amount,
        "currency": currency,
        "status": "SUCCESS"
    }), 201


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port
    )