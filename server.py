import socket
import threading
import json
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


@app.route('/index/challenge')
def challenge():
    return render_template('challenge_page.html')


@app.route('/game/flappy_bird')
def flappy_bird():
    return render_template('game/flappy_bird.html')


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
