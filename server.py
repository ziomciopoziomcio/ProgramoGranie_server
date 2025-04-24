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
    return render_template('templates/login_page.html')

@app.route('/index')
def index():
    return render_template('templates/main_menu_page.html')


if __name__ == '__main__':
    app.run(debug=True)
