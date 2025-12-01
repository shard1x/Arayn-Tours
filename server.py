from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash # Импортируем функции для работы с паролями

app = Flask(__name__)
app.secret_key = '9f0c4a7d2e7d4b8b9f0a6d7e8f0c4a7d2e7d4b8b9f0a6d7e8f0c4a7d2e7d4b8b'

# Конфигурация базы данных
app.config['DB_HOST'] = 'localhost'
app.config['DB_NAME'] = 'Aryan Tours'
app.config['DB_USER'] = 'postgres'
app.config['DB_PASSWORD'] = '1'

ADMIN_USERNAME = "ADMIN"
ADMIN_EMAIL = "admin.ex@gmail.com"
ADMIN_PASSWORD = "ADMIN14"


def get_db_connection():
    conn = psycopg2.connect(
        host=app.config['DB_HOST'],
        database=app.config['DB_NAME'],
        user=app.config['DB_USER'],
        password=app.config['DB_PASSWORD'])
    return conn

def is_admin():
    return session.get('is_admin', False)

@app.route('/submit_application', methods=['POST'])
def submit_application():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute("INSERT INTO applications (name, email, phone) VALUES (%s, %s, %s)",
                        (name, email, phone))
            conn.commit()
            flash('Заявка успешно отправлена!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Ошибка отправки заявки: {str(e)}', 'error')
        finally:
            cur.close()
            conn.close()

        return render_template('choose_tour.html')

@app.route('/')
def home():
    user_id = session.get('user_id')
    is_admin_flag = is_admin()  # Передаем признак админа в шаблон
    return render_template('main.html', user_id=user_id, is_admin=is_admin_flag)

@app.route('/delete_review/<int:review_id>')
def delete_review(review_id):
    if is_admin(): #Проверяем, является ли пользователь админом
        conn = get_db_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM reviews WHERE id = %s", (review_id,))
            conn.commit()
            flash('Отзыв успешно удален!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Ошибка удаления отзыва: {str(e)}', 'error')
        finally:
            cur.close()
            conn.close()
    else:
        flash('У вас нет прав для удаления отзывов.', 'error')
    return redirect(url_for('reviews'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

@app.route('/choose_tour')
def choose_tour():
    return render_template('choose_tour.html')

@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        if 'user_id' in session and not is_admin():
            user_id = session['user_id']
            text = request.form['text']
            rating = int(request.form['rating'])
            try:
                cur.execute("INSERT INTO reviews (user_id, text, rating) VALUES (%s, %s, %s)",
                            (user_id, text, rating))
                conn.commit()
                flash('Отзыв успешно добавлен!', 'success')
            except Exception as e:
                conn.rollback()
                flash(f'Ошибка добавления отзыва: {str(e)}', 'error')
            finally:
                cur.close()
                conn.close()
                return redirect(url_for('reviews'))
        else:
            flash('Необходимо авторизоваться, чтобы оставить отзыв.', 'error')
            return redirect(url_for('login'))

    cur.execute("SELECT reviews.id, users.username, reviews.text, reviews.rating, reviews.date FROM reviews JOIN users ON reviews.user_id = users.id")
    reviews = cur.fetchall()
    cur.close()
    conn.close()

    is_admin_flag = is_admin() # Передаем признак админа шаблону
    return render_template('reviews.html', reviews=reviews, is_admin=is_admin_flag)

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
    return redirect(url_for('home'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = get_db_connection()
        cur = conn.cursor()

        if username == ADMIN_USERNAME:
            # Проверка данных администратора
            if password == ADMIN_PASSWORD:
                session['user_id'] = -1  # Условный ID для админа
                session['is_admin'] = True #  Устанавливаем флаг администратора
                return redirect(url_for('home'))
            else:
                error = "Неверный пароль администратора"
        else:
            # Проверка обычного пользователя
            cur.execute("SELECT id, password FROM users WHERE username = %s", (username,))
            user = cur.fetchone()

            if user and check_password_hash(user[1], password):
                session['user_id'] = user[0]
                session['is_admin'] = False
                return redirect(url_for('home'))
            else:
                error = "Неверные имя пользователя или пароль"

        cur.close()
        conn.close()

        return render_template('login.html', error=error)
    return render_template('login.html', error=None)

@app.route('/profile')
def profile():
    user_id = session.get('user_id')
    if user_id:
        return render_template('profile.html') #Если авторизован - переходим в профиль
    else:
        return redirect(url_for('login')) #Если не авторизован - на страницу логина

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

if __name__ == '__main__':
    app.run(debug=True)
