from flask import Flask, render_template_string, request, redirect, url_for, flash, session
import sqlite3

app = Flask(__name__)
app.secret_key = '1234abcd'  # Replace with a secure random key

# Function to initialize the database and create the users table
def init_sqlite_db():
    conn = sqlite3.connect('users.db')
    conn.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)')
    conn.close()

# Initialize the database
init_sqlite_db()

# Route for the login page
@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check the database for the user
        with sqlite3.connect('users.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
            user = cur.fetchone()

            if user:
                session['username'] = username
                flash('Login successful!', 'success')
                return redirect(url_for('home'))
            else:
                flash('Invalid username or password. Please try again.', 'danger')
                return redirect(url_for('login'))

    return render_template_string('''
        <!doctype html>
        <title>Login</title>
        <h2>Login</h2>
        <form method="post">
            <label for="username">Username:</label>
            <input type="text" name="username" id="username" required><br><br>
            <label for="password">Password:</label>
            <input type="password" name="password" id="password" required><br><br>
            <input type="submit" value="Login">
        </form>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                <ul>
                {% for category, message in messages %}
                    <li class="{{ category }}">{{ message }}</li>
                {% endfor %}
                </ul>
            {% endif %}
        {% endwith %}
    ''')

# Route for the home page (after login)
@app.route('/home/')
def home():
    if 'username' in session:
        return f"Hello, {session['username']}! Welcome to the Home Page."
    else:
        flash('You need to log in first.', 'warning')
        return redirect(url_for('login'))

# Route for logging out
@app.route('/logout/')
def logout():
    session.pop('username', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# Route to create a test user
@app.route('/create-user/')
def create_user():
    with sqlite3.connect('users.db') as conn:
        conn.execute("INSERT INTO users (username, password) VALUES ('testuser', 'testpassword')")
        conn.commit()
        flash('Test user created successfully. Username: testuser, Password: testpassword', 'success')
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
