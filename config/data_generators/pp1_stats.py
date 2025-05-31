import random
import mysql.connector
import json

# Connect to the database
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
user_id = input("Enter user ID for which to generate PP1 stats: ")

# Topics for PP1
topics = [
    "Wprowadzanie i wyświetlanie danych",
    "Instrukcje warunkowe, wyboru switch .. case",
    "Pętle, instrukcje iteracyjne",
    "Tablice jednowymiarowe",
    "Tablice jednowymiarowe - teksty",
    "Tablice wielowymiarowe",
    "Funkcje I, II",
    "Rekurencja",
    "Sortowanie",
    "Wskaźniki i tablice",
    "Teksty i napisy",
    "Zadania ogólnorozwojowe"
]

# Insert random data for topics
for topic in topics:
    progress = random.randint(0, 100)
    overall_stat = random.choice(["Zaliczone przedmioty", "Nie zaliczone przedmioty"])
    completion_status = "Zaliczone" if progress > 50 else "Nie zaliczone"
    achievement_name = random.choice(["Achievement1", "Achievement2", "Achievement3"])
    achievement_progress = random.randint(0, 100)

    cursor.execute("""
        INSERT INTO pp1_stats (user_id, topic_name, progress, overall_stat, completion_status, achievement_name, achievement_progress)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (user_id, topic, progress, overall_stat, completion_status, achievement_name, achievement_progress))

conn.commit()
cursor.close()
conn.close()