import json
import requests
import os

BOT_TOKEN = "8194199013:AAH9O-axpQHceYD3VGRsEukwoSYtGLPDqf8"
CHANNEL_ID = "@skin_master_gdd"
DATA_FILE = "data.json"  # файл для хранения кристаллов

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def handler(request, response):
    try:
        data = json.loads(request.data)
        user_id = str(data.get("user_id"))
        if not user_id:
            return response.status(400).json({"subscribed": False, "error": "Нет user_id"})

        # Проверка подписки в Telegram
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember"
        params = {"chat_id": CHANNEL_ID, "user_id": user_id}
        r = requests.get(url, params=params)
        result = r.json()

        if result.get("ok") and result["result"]["status"] in ["member", "creator", "administrator"]:
            # Загрузка текущих кристаллов
            crystals_data = load_data()
            current = crystals_data.get(user_id, 0)
            crystals_data[user_id] = current + 300  # добавляем 300 кристаллов
            save_data(crystals_data)

            return response.status(200).json({
                "subscribed": True,
                "reward": 300,
                "total_crystals": crystals_data[user_id]
            })
        else:
            return response.status(200).json({"subscribed": False, "result": result})

    except Exception as e:
        return response.status(500).json({"subscribed": False, "error": str(e)})
