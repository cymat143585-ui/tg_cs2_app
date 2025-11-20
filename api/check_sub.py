from flask import Flask, request, jsonify
import sqlite3
import requests
import os

app = Flask(__name__)

# Твой токен и канал
BOT_TOKEN = "8194199013:AAH9O-axpQHceYD3VGRsEukwoSYtGLPDqf8"
CHANNEL_ID = "@skin_master_gdd"
DB_FILE = "crystals.db"


# ---------------------------
# ИНИЦИАЛИЗАЦИЯ БАЗЫ ДАННЫХ
# ---------------------------
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


# ---------------------------
# ФУНКЦИИ ДЛЯ РАБОТЫ С БД
# ---------------------------
def get_crystals(user_id: int):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT crystals FROM users WHERE id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0


def add_crystals(user_id: int, amount: int):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    current = get_crystals(user_id)

    if current == 0:  # пользователь нет в БД
        c.execute("INSERT INTO users (id, crystals) VALUES (?, ?)", (user_id, amount))
    else:
        c.execute("UPDATE users SET crystals = ? WHERE id = ?", (current + amount, user_id))

    conn.commit()
    conn.close()
    return get_crystals(user_id)


# ---------------------------
# ПРОВЕРКА ПОДПИСКИ В TELEGRAM
# ---------------------------
def is_subscribed(user_id: int) -> bool:
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/getChatMember"
    params = {"chat_id": CHANNEL_ID, "user_id": user_id}

    try:
        r = requests.get(url, params=params, timeout=5)
        data = r.json()
    except Exception:
        return False

    if not data.get("ok"):
        return False

    status = data["result"]["status"]
    return status in ["member", "administrator", "creator"]


# ---------------------------
# API: ПРОВЕРКА ПОДПИСКИ
# ---------------------------
@app.route("/check_sub", methods=["POST"])
def check_sub():
    data = request.json
    if not data:
        return jsonify({"error": "Нет JSON"}), 400

    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "Нет user_id"}), 400

    try:
        user_id = int(user_id)
    except:
        return jsonify({"error": "user_id должен быть числом"}), 400

    if is_subscribed(user_id):
        total = add_crystals(user_id, 300)
        return jsonify({
            "subscribed": True,
            "reward": 300,
            "total_crystals": total
        })
    else:
        return jsonify({"subscribed": False})


# ---------------------------
# ГЛАВНАЯ СТРАНИЦА (ТЕСТ)
# ---------------------------
@app.route("/")
def home():
    return "Flask сервер работает!"


# Запуск локально (Render игнорирует этот блок)
if __name__ == "__main__":
    app.run(debug=True)

