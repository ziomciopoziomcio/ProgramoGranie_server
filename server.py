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
                flash('Zalogowano pomyślnie!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Nieprawidłowy email lub hasło.', 'danger')
        finally:
            cursor.close()
            conn.close()

    return render_template('login_page.html')


# end of login page config

@app.route('/register')
def register():
    return render_template('register_page.html')

@app.route('/index')
def index():
    return render_template('main_menu_page.html')


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
        for stat in stats:
            achievement_name = stat["achievement_name"]
            achievement_progress = stat["achievement_progress"]
            if achievement_name not in achievement_count:
                achievement_count[achievement_name] = 0
            achievement_count[achievement_name] += achievement_progress

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
            "achievements": achievement_count,
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
    return render_template('profile_page.html')


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
        for stat in stats:
            achievement_name = stat["achievement_name"]
            achievement_progress = stat["achievement_progress"]
            if achievement_name not in achievement_count:
                achievement_count[achievement_name] = 0
            achievement_count[achievement_name] += achievement_progress

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
            "achievements": achievement_count,
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
        for stat in stats:
            achievement_name = stat["achievement_name"]
            achievement_progress = stat["achievement_progress"]
            if achievement_name not in achievement_count:
                achievement_count[achievement_name] = 0
            achievement_count[achievement_name] += achievement_progress

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
            "achievements": achievement_count,
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
        if 'file' not in request.files:
            return jsonify({'error': 'Nie wybrano pliku'}), 400
        files = request.files.getlist('file')  # Get all files with the key 'file'
        if not files:
            return jsonify({'error': 'Nie wybrano plików'}), 400

        uploaded_files = []
        for file in files:
            if file.filename == '':
                continue
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)
            uploaded_files.append(file.filename)

        if not uploaded_files:
            return jsonify({'error': 'Nie zapisano żadnych plików'}), 400

        return jsonify(uploaded_files)  # Return the list of uploaded files

    return render_template('challenge_page.html')

# end of that stressful situation...

@app.route('/game/flappy_bird')
def flappy_bird():
    return render_template('game/flappy_bird.html')

@app.route('/admin')
def admin_panel():
    return render_template('admin_panel.html')


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
