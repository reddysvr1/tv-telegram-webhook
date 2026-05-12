from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = os.environ.get("BOT_TOKEN")
CHAT_IDS = os.environ.get("CHAT_IDS", "")

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json or {}

    message = data.get("message", "TradingView Alert")

    telegram_url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    chat_ids = [chat_id.strip() for chat_id in CHAT_IDS.split(",") if chat_id.strip()]

    if not chat_ids:
        return {"status": "error", "message": "No CHAT_IDS configured"}, 500

    results = []

    for chat_id in chat_ids:
        payload = {
            "chat_id": chat_id,
            "text": message
        }

        response = requests.post(telegram_url, json=payload)

        results.append({
            "chat_id": chat_id,
            "status_code": response.status_code,
            "response": response.text
        })

    return {
        "status": "ok",
        "sent_to": len(chat_ids),
        "results": results
    }, 200

@app.route('/')
def home():
    return "Webhook running!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
