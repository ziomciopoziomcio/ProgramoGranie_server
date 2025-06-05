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
    return render_template('pp1_stats_page.html')


@app.route('/index/profile')
def profile():
    return render_template('profile_page.html')


@app.route('/index/pp2')
def pp2_stats():
    return render_template('pp2_stats_page.html')


@app.route('/index/so2')
def so2_stats():
    return render_template('so2_stats_page.html')

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
