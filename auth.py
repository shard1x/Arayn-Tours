from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = '9f0c4a7d2e7d4b8b9f0a6d7e8f0c4a7d2e7d4b8b9f0a6d7e8f0c4a7d2e7d4b8b'

app.config['DB_HOST'] = 'localhost'
app.config['DB_NAME'] = 'Aryan Tours'
app.config['DB_USER'] = 'postgres'
app.config['DB_PASSWORD'] = '1'

CORS(app)

ADMIN_USERNAME = "ADMIN"
ADMIN_EMAIL = ""
ADMIN_PASSWORD = "ADMIN14"

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

def get_db_connection():
    conn = psycopg2.connect(
        host=app.config['DB_HOST'],
        database=app.config['DB_NAME'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD'])
    return conn

def is_admin():
    return session.get('is_admin', False)

@app.route('/')
def index():
    return redirect('http://localhost:5000/')

@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    if user_id == -1:  # админ
        # Передаем в шаблон флаг is_admin=True, чтобы показать другое сообщение
        return render_template('profile.html', is_admin=True)

    # Для обычного пользователя получаем данные из базы
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT username, email FROM users WHERE id = %s", (user_id,))
    user_row = cur.fetchone()
    cur.close()
    conn.close()
    if not user_row:
        return redirect(url_for('login'))

    user_data = {'username': user_row[0], 'email': user_row[1]}
    return render_template('profile.html', user=user_data, is_admin=False)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                        (username, email, hashed_password))
            conn.commit()
            cur.close()
            conn.close()
          #  flash('Регистрация прошла успешно!', 'success') # Отображаем сообщение об успехе
            return redirect(url_for('login', succes="Регистрация прошла успешно"))  # Перенаправляем на страницу входа
        except Exception as e:
            print(e)
            conn.rollback()
            cur.close()
            conn.close()
          #  flash('Ошибка регистрации', 'error') # Отображаем сообщение об ошибке
            return render_template('register.html', error="Ошибка регистрации")

    return render_template('register.html', error=None) #Отображаем страницу регистрации без ошибок

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('is_admin', None)
    return redirect('http://localhost:5000/')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()

        if username == ADMIN_USERNAME:
            if password == ADMIN_PASSWORD:
                session['user_id'] = -1
                session['is_admin'] = True
                print(
                    'admin redirect'
                )
                return redirect('http://localhost:5000/')
            else:
                error = "Неверный пароль администратора"
        else:
            cur.execute("SELECT id, password FROM users WHERE username = %s", (username,))
            user = cur.fetchone()

            if user and check_password_hash(user[1], password):
                session['user_id'] = user[0]
                session['is_admin'] = False
                print('user redirect')
                return redirect('http://localhost:5000/')
            else:
                error = "Неверные имя пользователя или пароль"

        cur.close()
        conn.close()

        return render_template('login.html', error=error)
    return render_template('login.html', error=None)

if __name__ == '__main__':
    app.run(debug=True, port=5002)