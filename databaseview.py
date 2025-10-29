import sqlite3

def view_database():
    conn = sqlite3.connect('trivia_data.db')
    cur = conn.cursor()
    cur.execute("SELECT name, level FROM players")
    rows = cur.fetchall()
    conn.close()

    print("=== OU Trivia Player Data ===")
    for row in rows:
        print(f"Name: {row[0]}, Level: {row[1]}")

view_database()