import hashlib
from flask import Flask, render_template, session, redirect, url_for, request, flash
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

# Параметры подключения к PostgreSQL — замените на свои данные
DB_HOST = "localhost"          # Например: "localhost" или IP-адрес сервера
DB_NAME = "Aryan Tours"        # Название вашей базы данных
DB_USER = "postgres"      # Имя пользователя базы данных
DB_PASS = "1"      # Пароль к базе данных

def get_db_connection():
    # Создайте соединение с вашей базой данных, подставляя свои параметры
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

# Передаем is_authenticated в шаблоны автоматически
@app.context_processor
def inject_user_status():
    return {'is_authenticated': 'true' if 'user_id' in session else 'false'}

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/about')
def about():
    return render_template('about.html')

# Остальные маршруты
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        password = request.form['password']

        if not (name and phone and email and password):
            flash("Все поля обязательны для заполнения")
            return redirect(url_for('register'))

        password_hash = generate_password_hash(password)

        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO users (name, phone, email, password_hash) VALUES (%s, %s, %s, %s)",
                (name, phone, email, password_hash)
            )
            conn.commit()
        except psycopg2.errors.UniqueViolation:
            conn.rollback()
            flash("Пользователь с таким email уже существует")
            cur.close()
            conn.close()
            return redirect(url_for('register'))
        cur.close()
        conn.close()
        flash("Регистрация прошла успешно, теперь можно войти")
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT id, password_hash FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user and check_password_hash(user[1], password):
            session['user_id'] = user[0]
            session['user_email'] = email
            return redirect(url_for('profile'))
        else:
            flash("Неверный email или пароль")
            return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user_id' in session:
        user_id = session['user_id']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT name, phone, email FROM users WHERE id=%s", (user_id,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        if user:
            name, phone, email = user
            return render_template('profile.html', name=name, phone=phone, email=email)
        else:
            flash("Пользователь не найден")
            return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

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