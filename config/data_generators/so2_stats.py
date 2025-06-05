import random
import mysql.connector
import json

# Load database credentials
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

conn = get_db_connection()
cursor = conn.cursor(dictionary=True)
user_id = input("Enter user ID for which to generate SO2 stats: ")

# Topics for SO2
topics = [
    "Zarządzanie pamięcią",
    "System plików FAT 12/16"
]

# Insert random data for topics
for topic in topics:
    progress = random.randint(0, 100)
    overall_stat = random.choice(["Zaliczone przedmioty", "Nie zaliczone przedmioty"])
    completion_status = "Zaliczone" if progress > 50 else "Nie zaliczone"
    achievement_name = random.choice(["Achievement1", "Achievement2", "Achievement3"])
    achievement_progress = random.randint(0, 100)

    cursor.execute("""
        INSERT INTO so2_stats (user_id, topic_name, progress, overall_stat, completion_status, achievement_name, achievement_progress)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (user_id, topic, progress, overall_stat, completion_status, achievement_name, achievement_progress))

conn.commit()
cursor.close()
conn.close()