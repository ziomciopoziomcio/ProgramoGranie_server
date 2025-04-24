import socket
import threading
import json
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello World!"


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


if __name__ == '__main__':
    app.run(debug=True)
