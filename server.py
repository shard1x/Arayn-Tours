import hashlib
from flask import Flask, render_template, session, redirect, url_for, request, flash, jsonify
from flask_session import Session
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Секретный ключ для сессий (замените на свой собственный ключ)
app.secret_key = '9f0c4a7d2e7d4b8b9f0a6d7e8f0c4a7d2e7d4b8b9f0a6d7e8f0c4a7d2e7d4b8b'

# Конфигурация Flask-Session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Параметры подключения к PostgreSQL
DB_HOST = "localhost"
DB_NAME = "Aryan Tours"
DB_USER = "postgres"
DB_PASS = "1"

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

@app.route('/reviews')
def reviews():
    return render_template('reviews.html')

@app.route('/finland')
def finland():
    return render_template('finland.html')

@app.route('/sweden')
def sweden():
    return render_template('sweden.html')

@app.route('/norway')
def norway():
    return render_template('norway.html')

@app.route('/russia')
def russia():
    return render_template('russia.html')

@app.route('/denmark')
def denmark():
    return render_template('denmark.html')

@app.route('/germany')
def germany():
    return render_template('germany.html')

if __name__ == '__main__':
    app.run(debug=True)