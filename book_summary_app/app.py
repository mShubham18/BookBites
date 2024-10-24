from flask import Flask, render_template, redirect, url_for, request, session
from utils.user_management import register_user, user_exists, verify_user
from utils.book_management import get_genres_and_books

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a strong secret key

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']

        if user_exists(email, phone):
            return "User already exists", 400  # Handle user exists case

        register_user(name, email, password, phone)
        return redirect(url_for('login'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if verify_user(email, password):
            session['logged_in'] = True
            session['email'] = email
            return redirect(url_for('genre_selection'))

        return "Invalid credentials", 400  # Handle invalid login

    return render_template('login.html')

@app.route('/genre_selection', methods=['GET', 'POST'])
def genre_selection():
    if 'logged_in' not in session:
        return redirect(url_for('login'))

    genres = get_genres_and_books()
    selected_genre = None
    selected_book = None

    if request.method == 'POST':
        selected_genre = request.form['genre']
        selected_book = request.form['book']

    return render_template('genre_selection.html', genres=genres)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)