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
            return redirect('http://localhost:5002/login')

    try:
        cur.execute("""
            SELECT reviews.id, users.username, reviews.text, reviews.rating, reviews.date
            FROM reviews
            JOIN users ON reviews.user_id = users.id
            ORDER BY reviews.date DESC
        """)
        reviews_list = cur.fetchall()
    except Exception as e:
        reviews_list = []
        flash(f'Ошибка загрузки отзывов: {str(e)}', 'error')
    finally:
        cur.close()
        conn.close()

    return render_template('reviews.html', reviews=reviews_list, is_admin=is_admin())


@app.route('/edit_review/<int:review_id>', methods=['GET', 'POST'])
def edit_review(review_id):
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'GET':
        cur.execute("SELECT text, rating FROM reviews WHERE id = %s", (review_id,))
        review = cur.fetchone()

        if review:
            return render_template('edit_review.html', review_id=review_id, review=review)
        else:
            flash('Отзыв не найден.', 'error')
            return redirect(url_for('reviews'))

    elif request.method == 'POST':
        text = request.form['text']
        rating = int(request.form['rating'])

        try:
            cur.execute("UPDATE reviews SET text = %s, rating = %s WHERE id = %s", (text, rating, review_id))
            conn.commit()
            flash('Отзыв успешно обновлен!', 'success')
        except Exception as e:
            conn.rollback()
            flash(f'Ошибка обновления отзыва: {str(e)}', 'error')
        finally:
            cur.close()
            conn.close()
        return redirect(url_for('reviews'))


@app.route('/delete_review/<int:review_id>')
def delete_review(review_id):
    if is_admin():
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

if __name__ == '__main__':
    app.run(debug=True, port=5001)