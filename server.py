import sqlite3
import telebot
from flask import Flask, request, jsonify

# إعداد البوت
API_TOKEN = "7679813979:AAGWex1J2x6mIabmBgKMXGhGuILrPN2wLGo"
bot = telebot.TeleBot(API_TOKEN)

app = Flask(__name__)

# إنشاء قاعدة بيانات (قد لا يعمل على Vercel)
def create_database():
    conn = sqlite3.connect("chess_game.db")
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        first_name TEXT,
        last_name TEXT,
        date_joined TEXT DEFAULT CURRENT_TIMESTAMP,
        points INTEGER DEFAULT 0
    )
    """
    )
    conn.commit()
    conn.close()

# 🌍 صفحة اختبار للتأكد أن السيرفر يعمل
@app.route("/", methods=["GET"])
def home():
    return "Chess Bot Server is Running!"

# ✅ نقطة نهاية لإضافة المستخدم
@app.route("/add-user", methods=["POST"])
def add_user():
    data = request.json
    user_id = data.get("user_id")
    username = data.get("username", "Unknown")
    first_name = data.get("first_name", "Guest")
    last_name = data.get("last_name", "")

    conn = sqlite3.connect("chess_game.db")
    cursor = conn.cursor()
    cursor.execute(
        """
    INSERT OR IGNORE INTO users (user_id, username, first_name, last_name, date_joined, points)
    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, 0)
    """,
        (user_id, username, first_name, last_name),
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "User added successfully!"})

# ✅ نقطة نهاية لاسترجاع بيانات المستخدم
@app.route("/get-user-data", methods=["POST"])
def get_user_data():
    data = request.json
    user_id = data.get("user_id")

    conn = sqlite3.connect("chess_game.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT username, first_name, last_name, points FROM users WHERE user_id = ?", (user_id,)
    )
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        return jsonify(
            {
                "username": user_data[0],
                "first_name": user_data[1],
                "last_name": user_data[2],
                "points": user_data[3],
            }
        )
    else:
        return jsonify({"error": "User not found"}), 404

# ✅ نقطة نهاية لاستقبال Webhook من تليجرام
@app.route("/webhook", methods=["POST"])
def webhook():
    """استقبال التحديثات من تليجرام ومعالجتها"""
    json_update = request.get_json()
    bot.process_new_updates([telebot.types.Update.de_json(json_update)])
    return "", 200  # تأكيد الاستلام إلى تليجرام

# ✅ استجابة لرسائل تليجرام
@bot.message_handler(commands=["start"])
def handle_start(message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    conn = sqlite3.connect("chess_game.db")
    cursor = conn.cursor()
    cursor.execute(
        """
    INSERT OR IGNORE INTO users (user_id, username, first_name, last_name, date_joined, points)
    VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, 0)
    """,
        (user_id, username, first_name, last_name),
    )
    conn.commit()
    conn.close()

    bot.reply_to(message, "أهلاً وسهلاً بك في لعبة الشطرنج! 🎉")

# 🌍 تشغيل التطبيق
if __name__ == "__main__":
    create_database()  # إنشاء قاعدة البيانات
    app.run(host="0.0.0.0", port=8000)  # تشغيل Flask
