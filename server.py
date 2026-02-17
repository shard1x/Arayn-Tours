from flask import Flask, render_template, request, redirect, url_for, session, flash
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = '9f0c4a7d2e7d4b8b9f0a6d7e8f0c4a7d2e7d4b8b9f0a6d7e8f0c4a7d2e7d4b8b'

app.config['DB_HOST'] = 'localhost'
app.config['DB_NAME'] = 'Aryan Tours'
app.config['DB_USER'] = 'postgres'
app.config['DB_PASSWORD'] = '1'

ADMIN_USERNAME = "ADMIN"
ADMIN_EMAIL = ""
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
    is_admin_flag = is_admin()
    return render_template('main.html', user_id=user_id, is_admin=is_admin_flag)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contacts')
def contacts():
    return render_template('contacts.html')

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

if __name__ == '__main__':
    app.run(debug=True, port=5000)