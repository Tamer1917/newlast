import sqlite3

def show_users():
    conn = sqlite3.connect('chess_game.db')
    cursor = conn.cursor()

    # جلب البيانات من جدول users
    cursor.execute('''
    SELECT 
        user_id,
        username,
        first_name,
        last_name, 
        date_joined, 
        points
    FROM 
        users
    ''')

    users = cursor.fetchall()

    # عرض البيانات
    for user in users:
        print(f"ID: {user[0]}, Username: {user[1]}, First Name: {user[2]}, Last Name: {user[3]}, Date Joined: {user[4]}, Points: {user[5]}")

    conn.close()

if __name__ == "__main__":
    show_users()
