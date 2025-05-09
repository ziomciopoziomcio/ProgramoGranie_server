import socket
import threading
import json
from flask import Flask, request, jsonify, render_template, url_for

app = Flask(__name__)


@app.route('/')
def home():
    return login()


@app.route('/login')
def login():
    return render_template('login_page.html')

@app.route('/index')
def index():
    return render_template('main_menu_page.html')

@app.route('/index/game')
def game():
    return render_template('game_page.html')

@app.route('/index/pp1/stats')
def pp1_stats():
    return render_template('pp1_stats_page.html')

@app.route('/index/profile')
def profile():
    return render_template('profile_page.html')

@app.route('/index/pp2/stats')
def pp2_stats():
    return render_template('pp2_stats_page.html')

@app.route('/index/so2/stats')
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
        'pp1': 'PP1',
        'pp2': 'PP2',
        'so2': 'SO2',
        'stats': 'Statystyki',
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
