from flask import Flask, render_template, session, redirect, url_for

app = Flask(__name__)
app.secret_key = '9f0c4a7d2e7d4b8b9f0a6d7e8f0c4a7d2e7d4b8b9f0a6d7e8f0c4a7d2e7d4b8b'

@app.route('/')
def home():
    return render_template('main.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/about')
def about():
    return render_template('about.html')

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

@app.route('/denmark')
def denmark():
    return render_template('denmark.html')

@app.route('/germany')
def germany():
    return render_template('germany.html')

# Маршрут для профиля
@app.route('/profile')
def profile():
    if 'user_id' in session:
        return render_template('profile.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)