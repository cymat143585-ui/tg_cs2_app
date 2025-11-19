import sqlite3
import json
import requests
import os

BOT_TOKEN = "8194199013:AAH9O-axpQHceYD3VGRsEukwoSYtGLPDqf8"
CHANNEL_ID = "@skin_master_gdd"
DATA_FILE = "data.json"  # файл для хранения кристаллов
DB_FILE = "crystals.db"

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            crystals INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Получение кристаллов пользователя
def get_crystals(user_id):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT crystals FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0

# Добавление кристаллов пользователю
def add_crystals(user_id, amount):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    current = get_crystals(user_id)
    if current == 0:
        c.execute("INSERT INTO users (id, crystals) VALUES (?, ?)", (user_id, amount))
    else:
        c.execute("UPDATE users SET crystals = ? WHERE id = ?", (current + amount, user_id))
    conn.commit()
    conn.close()
    return get_crystals(user_id)

# Проверка подписки в Telegram
def is_subscribed(user_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember"
    params = {"chat_id": CHANNEL_ID, "user_id": user_id}
    r = requests.get(url, params=params)
    result = r.json()
    if result.get("ok") and result["result"]["status"] in ["member", "creator", "administrator"]:
        return True
    return False

# Эндпоинт проверки подписки
@app.route("/check_sub", methods=["POST"])
def check_sub():
    data = request.json
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "Нет user_id"}), 400

    if is_subscribed(user_id):
        total = add_crystals(user_id, 300)
        return jsonify({"subscribed": True, "reward": 300, "total_crystals": total})
    else:
        return jsonify({"subscribed": False})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
