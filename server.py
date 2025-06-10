import socket
import threading
import json
import os
from flask import Flask, request, jsonify, render_template, url_for, redirect, session, flash
import mysql.connector
import bcrypt

app = Flask(__name__)
app.secret_key = 'bardzo_bezpieczny_klucz'  # tylko na potrzeby testowe


@app.route('/')
def home():
    return login()


# LOGIN PAGE CONFIG
# DO NOT TOUCH WITHOUT KNOWING WHAT YOU DO

with open('config/credts/DB_credentials.json') as f:
    db_credentials = json.load(f)


def get_db_connection():
    return mysql.connector.connect(
        host=db_credentials['db_host'],
        port=db_credentials['db_port'],
        user=db_credentials['db_user'],
        password=db_credentials['db_password'],
        database=db_credentials['db_name']
    )


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Connect to the database
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        try:
            # Query the user by email
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()

            if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
                # Login successful
                session['user_id'] = user['id']
                session['role'] = user['role']
                flash('Zalogowano pomyślnie!', 'success')
                if user['role'] == 'Administrator':
                    return redirect(url_for('admin_panel'))
                else:
                    return redirect(url_for('index'))
            else:
                flash('Nieprawidłowy email lub hasło.', 'danger')
        finally:
            cursor.close()
            conn.close()

    return render_template('login_page.html')


# end of login page config

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Get form data
        first_name = request.form.get('imie')
        last_name = request.form.get('nazwisko')
        index_number = request.form.get('indeks')  # Optional for students
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        degree = request.form.get('stopien-naukowy')

        if not first_name or not last_name or not email or not password or not role:
            flash('Wszystkie wymagane pola muszą być wypełnione.', 'danger')
            return render_template('register_page.html')

        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("""
                INSERT INTO users (first_name, last_name, index_number, email, password_hash, role, degree)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (first_name, last_name, index_number, email, password_hash, role, degree))
            conn.commit()
            flash('Rejestracja zakończona sukcesem!', 'success')
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            flash(f'Błąd podczas rejestracji: {err}', 'danger')
        finally:
            cursor.close()
            conn.close()

    return render_template('register_page.html')


@app.route('/index')
def index():
    user_id = session.get('user_id')
    if not user_id:
        flash('Musisz być zalogowany, aby zobaczyć tę stronę.', 'danger')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Pobierz dane użytkownika
        cursor.execute("SELECT first_name, last_name FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            flash('Nie znaleziono użytkownika.', 'danger')
            return redirect(url_for('login'))
    finally:
        cursor.close()
        conn.close()

    return render_template('main_menu_page.html', first_name=user['first_name'], last_name=user['last_name'])


@app.route('/index/game')
def game():
    return render_template('game_page.html')


@app.route('/index/pp1')
def pp1_stats():
    user_id = session.get('user_id')
    if not user_id:
        flash('Musisz być zalogowany, aby zobaczyć statystyki.', 'danger')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch statistics for the user
        cursor.execute("""
            SELECT topic_name, progress, overall_stat, completion_status, achievement_name, achievement_progress
            FROM pp1_stats
            WHERE user_id = %s
        """, (user_id,))
        stats = cursor.fetchall()

        # Count completed topics
        total_completed_topics = sum(1 for stat in stats if stat["completion_status"] == "Zaliczone")

        # Group achievements by name and calculate their progress
        achievement_count = {}
        achievement_total_progress = {}
        for stat in stats:
            achievement_name = stat["achievement_name"]
            achievement_progress = stat["achievement_progress"]
            if achievement_name not in achievement_count:
                achievement_count[achievement_name] = 0
                achievement_total_progress[achievement_name] = 0
            achievement_count[achievement_name] += 1
            achievement_total_progress[achievement_name] += achievement_progress

        # Convert achievement progress to percentage and format as string
        achievement_percentage = {}
        for achievement_name in achievement_total_progress:
            max_progress = achievement_count[achievement_name] * 100
            percentage = round(
                (achievement_total_progress[achievement_name] / max_progress) * 100, 2
            ) if max_progress > 0 else 0
            achievement_percentage[achievement_name] = f"{percentage}%"

        # Calculate completion percentage
        total_topics = len(stats)
        completion_percentage = round((total_completed_topics / total_topics) * 100, 2) if total_topics > 0 else 0

        # Calculate additional statistics
        average_progress = round(sum(stat["progress"] for stat in stats) / total_topics, 2) if total_topics > 0 else 0
        best_topic_progress = max(stat["progress"] for stat in stats) if stats else 0
        topics_above_50 = sum(1 for stat in stats if stat["progress"] > 50)

        overall_stats = {
            "completed_topics": total_completed_topics,
            "total_topics": total_topics,
            "completion_percentage": completion_percentage,
            "achievements": achievement_percentage,
            "average_progress": average_progress,
            "best_topic_progress": best_topic_progress,
            "topics_above_50": topics_above_50,
            "achievement_count": len(achievement_count),
        }
    finally:
        cursor.close()
        conn.close()

    return render_template('pp1_stats_page.html', stats=stats, overall_stats=overall_stats)


@app.route('/index/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        flash('Musisz być zalogowany, aby zobaczyć profil.', 'danger')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Pobierz dane użytkownika
        cursor.execute("SELECT first_name, last_name FROM users WHERE id = %s", (user_id,))
        user = cursor.fetchone()
        if not user:
            flash('Nie znaleziono użytkownika.', 'danger')
            return redirect(url_for('login'))

        first_name = user['first_name']
        last_name = user['last_name']

        subjects = ['pp1', 'pp2', 'so2']
        subject_achievements = {}

        for subject in subjects:
            cursor.execute(f"""
                SELECT achievement_name, achievement_progress
                FROM {subject}_stats
                WHERE user_id = %s
            """, (user_id,))
            rows = cursor.fetchall()

            # Group achievements and calculate percentages
            achievement_progress = {}
            for row in rows:
                name = row['achievement_name']
                progress = row['achievement_progress']
                if name not in achievement_progress:
                    achievement_progress[name] = {'total_progress': 0, 'count': 0}
                achievement_progress[name]['total_progress'] += progress
                achievement_progress[name]['count'] += 1

            # Calculate percentage for each achievement
            for name, data in achievement_progress.items():
                max_progress = data['count'] * 100
                data['percentage'] = (data['total_progress'] / max_progress) * 100 if max_progress > 0 else 0

            # Find the achievement with the highest percentage
            if achievement_progress:
                best_achievement = max(achievement_progress.items(), key=lambda x: x[1]['percentage'])
                achievement_images = {
                    'Achievement1': f'ach_{subject}_gold.png',
                    'Achievement2': f'ach_{subject}_silver.png',
                    'Achievement3': f'ach_{subject}_bronze.png',
                }
                best_achievement_image = achievement_images.get(best_achievement[0], 'default.png')
            else:
                best_achievement_image = 'default.png'

            subject_achievements[subject] = {'image_path': best_achievement_image}

            cursor.execute("""
                        SELECT a.name AS achievement_name, s.unlock_status
                        FROM achievements_stats s
                        JOIN achievements a ON s.ID_ach = a.id
                        WHERE s.user_ID = %s
                    """, (user_id,))
            achievements = cursor.fetchall()

            # Prepare data for the template
            for achievement in achievements:
                achievement['image_path'] = f"assets/stats_assets/{achievement['achievement_name']}.png"
                achievement['progress_percentage'] = f"{achievement['unlock_status']}/2"

    finally:
        cursor.close()
        conn.close()

    return render_template(
        'profile_page.html',
        first_name=first_name,
        last_name=last_name,
        subject_achievements=subject_achievements,
        achievements=achievements
    )

@app.route('/index/pp2')
def pp2_stats():
    user_id = session.get('user_id')
    if not user_id:
        flash('Musisz być zalogowany, aby zobaczyć statystyki.', 'danger')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch statistics for the user
        cursor.execute("""
            SELECT topic_name, progress, completion_status, achievement_name, achievement_progress
            FROM pp2_stats
            WHERE user_id = %s
        """, (user_id,))
        stats = cursor.fetchall()

        # Count completed topics
        total_completed_topics = sum(1 for stat in stats if stat["completion_status"] == "Zaliczone")

        # Group achievements by name and calculate their progress
        achievement_count = {}
        achievement_total_progress = {}
        for stat in stats:
            achievement_name = stat["achievement_name"]
            achievement_progress = stat["achievement_progress"]
            if achievement_name not in achievement_count:
                achievement_count[achievement_name] = 0
                achievement_total_progress[achievement_name] = 0
            achievement_count[achievement_name] += 1
            achievement_total_progress[achievement_name] += achievement_progress

        # Convert achievement progress to percentage and format as string
        achievement_percentage = {}
        for achievement_name in achievement_total_progress:
            max_progress = achievement_count[achievement_name] * 100
            percentage = round(
                (achievement_total_progress[achievement_name] / max_progress) * 100, 2
            ) if max_progress > 0 else 0
            achievement_percentage[achievement_name] = f"{percentage}%"

        # Calculate completion percentage
        total_topics = len(stats)
        completion_percentage = round((total_completed_topics / total_topics) * 100, 2) if total_topics > 0 else 0

        # Calculate additional statistics
        average_progress = round(sum(stat["progress"] for stat in stats) / total_topics, 2) if total_topics > 0 else 0
        best_topic_progress = max(stat["progress"] for stat in stats) if stats else 0
        topics_above_50 = sum(1 for stat in stats if stat["progress"] > 50)

        overall_stats = {
            "completed_topics": total_completed_topics,
            "total_topics": total_topics,
            "completion_percentage": completion_percentage,
            "achievements": achievement_percentage,
            "average_progress": average_progress,
            "best_topic_progress": best_topic_progress,
            "topics_above_50": topics_above_50,
            "achievement_count": len(achievement_count),
        }
    finally:
        cursor.close()
        conn.close()

    return render_template('pp2_stats_page.html', stats=stats, overall_stats=overall_stats)


@app.route('/index/so2')
def so2_stats():
    user_id = session.get('user_id')
    if not user_id:
        flash('Musisz być zalogowany, aby zobaczyć statystyki.', 'danger')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Fetch statistics for the user
        cursor.execute("""
            SELECT topic_name, progress, completion_status, achievement_name, achievement_progress
            FROM so2_stats
            WHERE user_id = %s
        """, (user_id,))
        stats = cursor.fetchall()

        # Count completed topics
        total_completed_topics = sum(1 for stat in stats if stat["completion_status"] == "Zaliczone")

        # Group achievements by name and calculate their progress
        achievement_count = {}
        achievement_total_progress = {}
        for stat in stats:
            achievement_name = stat["achievement_name"]
            achievement_progress = stat["achievement_progress"]
            if achievement_name not in achievement_count:
                achievement_count[achievement_name] = 0
                achievement_total_progress[achievement_name] = 0
            achievement_count[achievement_name] += 1
            achievement_total_progress[achievement_name] += achievement_progress

        # Convert achievement progress to percentage and format as string
        achievement_percentage = {}
        for achievement_name in achievement_total_progress:
            max_progress = achievement_count[achievement_name] * 100
            percentage = round(
                (achievement_total_progress[achievement_name] / max_progress) * 100, 2
            ) if max_progress > 0 else 0
            achievement_percentage[achievement_name] = f"{percentage}%"
        # Calculate completion percentage
        total_topics = len(stats)
        completion_percentage = round((total_completed_topics / total_topics) * 100, 2) if total_topics > 0 else 0

        # Calculate additional statistics
        average_progress = round(sum(stat["progress"] for stat in stats) / total_topics, 2) if total_topics > 0 else 0
        best_topic_progress = max(stat["progress"] for stat in stats) if stats else 0
        topics_above_50 = sum(1 for stat in stats if stat["progress"] > 50)

        overall_stats = {
            "completed_topics": total_completed_topics,
            "total_topics": total_topics,
            "completion_percentage": completion_percentage,
            "achievements": achievement_percentage,
            "average_progress": average_progress,
            "best_topic_progress": best_topic_progress,
            "topics_above_50": topics_above_50,
            "achievement_count": len(achievement_count),
        }
    finally:
        cursor.close()
        conn.close()

    return render_template('so2_stats_page.html', stats=stats, overall_stats=overall_stats)


# FILE UPLOAD CONFIG
# DO NOT TOUCH WITHOUT PERMISSION OF: ziomciopoziomcio pozderki
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 24 * 1024 * 1024  # 24 MB limit
if os.path.exists(app.config['UPLOAD_FOLDER']) is False:
    os.makedirs(app.config['UPLOAD_FOLDER'])


@app.route('/index/challenge', methods=['GET', 'POST'])
def challenge():
    if request.method == 'POST':
        # Tymczasowo nie przetwarzaj plików, tylko odśwież stronę
        return redirect(url_for('challenge'))
    return render_template('challenge_page.html')


# end of that stressful situation...

@app.route('/game/flappy_bird', methods=['GET', 'POST'])
def flappy_bird():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Musisz być zalogowany, aby zagrać.'}), 401

    challenge_id = request.args.get('challenge_id', 1)  # Default challenge ID
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        # Sprawdź, czy wpis już istnieje
        cursor.execute("""
            SELECT lives_remaining
            FROM player_challenges
            WHERE user_id = %s AND challenge_id = %s
        """, (user_id, challenge_id))
        result = cursor.fetchone()

        if not result:
            # Jeśli wpis nie istnieje, wstaw domyślną wartość
            cursor.execute("""
                INSERT INTO player_challenges (user_id, challenge_id, lives_remaining)
                VALUES (%s, %s, 3)
            """, (user_id, challenge_id))
            conn.commit()
            lives_remaining = 3
        else:
            # Jeśli wpis istnieje, pobierz aktualną wartość
            lives_remaining = result['lives_remaining']

        if request.method == 'POST':
            # Zmniejsz liczbę żyć o 1
            cursor.execute("""
                UPDATE player_challenges
                SET lives_remaining = lives_remaining - 1
                WHERE user_id = %s AND challenge_id = %s AND lives_remaining > 0
            """, (user_id, challenge_id))
            conn.commit()

            # Pobierz zaktualizowaną liczbę żyć
            cursor.execute("""
                SELECT lives_remaining
                FROM player_challenges
                WHERE user_id = %s AND challenge_id = %s
            """, (user_id, challenge_id))
            result = cursor.fetchone()
            if not result:
                return jsonify({'error': 'Nie znaleziono wyzwania lub brak żyć.'}), 400
            return jsonify({'lives_remaining': result['lives_remaining']})

    finally:
        cursor.close()
        conn.close()

    return render_template('game/flappy_bird.html', lives_remaining=lives_remaining)

@app.route('/admin', methods=['GET', 'POST'])
def admin_panel():
    # Check if the user is an administrator
    if not session.get('role') == 'Administrator':
        flash('Nie masz uprawnień do tej strony.', 'danger')
        return redirect(url_for('index'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        if request.method == 'POST':
            # Add a new challenge
            description = request.form['challenge-description']
            cursor.execute("INSERT INTO challenges (description) VALUES (%s)", (description,))
            conn.commit()
            flash('Polecenie zostało dodane.', 'success')

        # Fetch all challenges
        cursor.execute("SELECT * FROM challenges ORDER BY created_at DESC")
        challenges = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    return render_template('admin_panel.html', challenges=challenges)


def generate_breadcrumb():
    path = request.path.strip('/').split('/')

    custom_labels = {
        'index': 'Menu główne',
        'profile': 'Profil użytkownika',
        'pp1': 'PP1 Statystyki',
        'pp2': 'PP2 Statystyki',
        'so2': 'SO2 Statystyki',
        'challenge': 'Wyzwanie',
        'game': 'Gra',
        'flappy_bird': 'Flappy Bird'
    }
    breadcrumb = [{'name': 'Menu główne', 'url': url_for('index')}]
    for i in range(len(path)):
        if path[i] and path[i] != 'index':  # Skip 'index'
            name = custom_labels.get(path[i], path[i].capitalize())
            breadcrumb.append({
                'name': name,
                'url': '/' + '/'.join(path[:i + 1])
            })
    return breadcrumb


@app.context_processor
def inject_breadcrumb():
    return {'breadcrumb': generate_breadcrumb()}


if __name__ == '__main__':
    app.run(debug=True)
