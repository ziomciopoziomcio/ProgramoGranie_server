import mysql.connector
import random
import json

with open('../credts/DB_credentials.json') as f:
    db_credentials = json.load(f)


def get_db_connection():
    return mysql.connector.connect(
        host=db_credentials['db_host'],
        port=db_credentials['db_port'],
        user=db_credentials['db_user'],
        password=db_credentials['db_password'],
        database=db_credentials['db_name']
    )

def generate_achievement_stats(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Fetch all achievement IDs from the achievements table
        cursor.execute("SELECT ID FROM achievements")
        achievement_ids = cursor.fetchall()

        # Insert random unlock status for each achievement
        for (achievement_id,) in achievement_ids:
            unlock_status = random.randint(0, 2)
            cursor.execute(
                "INSERT INTO achievements_stats (user_ID, ID_ach, unlock_status) VALUES (%s, %s, %s)",
                (user_id, achievement_id, unlock_status)
            )

        conn.commit()
        print("Achievement stats generated successfully.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    user_id = input("Enter user_ID: ")
    generate_achievement_stats(user_id)