from flask import Flask, request, jsonify,send_from_directory
import requests

app = Flask(__name__)
BOT_TOKEN = "8194199013:AAH9O-axpQHceYD3VGRsEukwoSYtGLPDqf8"  # замените на токен вашего бота
CHANNEL_ID = "@skin_master_gdd"  # замените на username вашего канала


@app.route("/")
def index():
    return send_from_directory(".", "index.html")

@app.route("/check_sub", methods=["POST"])
def check_sub():
    data = request.get_json()
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"subscribed": False, "error": "Нет user_id"}), 400

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember"
    params = {"chat_id": CHANNEL_ID, "user_id": user_id}

    try:
        r = requests.get(url, params=params)
        r.raise_for_status()
        result = r.json()
        if result.get("ok") and result["result"]["status"] in ["member", "creator", "administrator"]:
            return jsonify({"subscribed": True, "reward": 300})
        else:
            return jsonify({"subscribed": False, "result": result})
    except requests.exceptions.RequestException as e:
        return jsonify({"subscribed": False, "error": str(e)}), 500
    except Exception as e:
        return jsonify({"subscribed": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

