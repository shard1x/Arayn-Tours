import hashlib
from flask import Flask, render_template, session, redirect, url_for, request, flash, jsonify
from flask_session import Session
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Секретный ключ для сессий
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

@app.route('/reviews')
def reviews():
    return render_template('reviews.html')

@app.route('/choose_tour')
def choose_tour():
    return render_template('choose_tour.html')

@app.route('/finland')
def finland():
    return render_template('finland.html')

@app.route('/sweden')
def sweden():
    return render_template('sweden.html')

@app.route('/norway')
def norway():
    return render_template('norway.html')

@app.route('/karelia')
def russia():
    return render_template('karelia.html')

@app.route('/germany')
def germany():
    return render_template('germany.html')

@app.route('/submit_application', methods=['POST'])
def submit_application():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        try:
            conn = get_db_connection()
            cur = conn.cursor()

            # SQL-запрос для вставки данных в таблицу applications
            cur.execute("INSERT INTO applications (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))

            conn.commit()  # Подтверждаем изменения в базе данных
            cur.close()
            conn.close()

            flash('Заявка успешно отправлена!', 'success')  # Сообщение об успехе
            return redirect(url_for('choose_tour'))  # Перенаправляем на страницу choose_tour
        except Exception as e:
            print(f"Ошибка при работе с базой данных: {e}")
            flash('Произошла ошибка при отправке заявки.', 'error')
            return redirect(url_for('choose_tour'))

    return redirect(url_for('choose_tour'))  # Если метод не POST, перенаправляем

if __name__ == '__main__':
    app.run(debug=True)
