import sqlite3
import telebot

# تهيئة البوت
API_TOKEN = '7679813979:AAGWex1J2x6mIabmBgKMXGhGuILrPN2wLGo'
bot = telebot.TeleBot(API_TOKEN)

# إنشاء قاعدة البيانات
def create_database():
    try:
        conn = sqlite3.connect('chess_game.db')
        cursor = conn.cursor()

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            date_joined TEXT DEFAULT CURRENT_TIMESTAMP,
            points INTEGER DEFAULT 0
        )
        ''')

        conn.commit()
    except sqlite3.Error as e:
        print(f"❌ خطأ في قاعدة البيانات: {e}")
    finally:
        conn.close()

# إضافة مستخدم جديد
def add_new_user(user_id, username, first_name, last_name):
    try:
        conn = sqlite3.connect('chess_game.db')
        cursor = conn.cursor()

        # التحقق من القيم الفارغة واستبدالها بقيم افتراضية
        username = username if username else "Unknown"
        first_name = first_name if first_name else "Guest"
        last_name = last_name if last_name else ""

        cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username, first_name, last_name, date_joined, points)
        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, 5)
        ''', (user_id, username, first_name, last_name))

        # طباعة رسالة لتأكيد الإدخال
        print(f"✔️ المستخدم {username} تم إضافته بنجاح إلى قاعدة البيانات.")

        conn.commit()
    except sqlite3.Error as e:
        print(f"❌ خطأ أثناء إضافة المستخدم: {e}")
    finally:
        conn.close()

# تحديث نقاط المستخدم
def update_user_points(user_id, points):
    try:
        conn = sqlite3.connect('chess_game.db')
        cursor = conn.cursor()

        cursor.execute('''
        UPDATE users
        SET points = ?
        WHERE user_id = ?
        ''', (points, user_id))

        conn.commit()
    except sqlite3.Error as e:
        print(f"❌ خطأ أثناء تحديث النقاط: {e}")
    finally:
        conn.close()

# استرجاع بيانات المستخدم
def get_user_data(user_id):
    try:
        conn = sqlite3.connect('chess_game.db')
        cursor = conn.cursor()

        cursor.execute('SELECT username, first_name, last_name, points FROM users WHERE user_id = ?', (user_id,))
        user_data = cursor.fetchone()

        conn.close()

        if user_data:
            return {
                'username': user_data[0],
                'first_name': user_data[1],
                'last_name': user_data[2],
                'points': user_data[3]
            }
        else:
            return None  # المستخدم غير موجود

    except sqlite3.Error as e:
        print(f"❌ خطأ أثناء جلب بيانات المستخدم: {e}")
        return None

# معالجة أمر البدء /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name

    print(f"📥 استقبال أمر البدء من {user_id}, {username}, {first_name}, {last_name})")
    add_new_user(user_id, username, first_name, last_name)
    bot.reply_to(message, f"🎉 أهلاً {first_name}! تم تسجيلك في لعبة الشطرنج وحصلت على 5 نقاط.")

# تشغيل البوت
if __name__ == "__main__":
    create_database()
    print("✅ البوت يعمل الآن...")
    bot.polling(none_stop=True, interval=0)
