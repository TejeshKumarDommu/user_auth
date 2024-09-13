from flask import Flask, render_template, request, redirect, jsonify, url_for
import jwt
import sqlite3
from functools import wraps
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'auth@role'

# Database connection
def connect_db():
    return sqlite3.connect('app.db')

# JWT token required decorator
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return redirect(url_for('login'))

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except:
            return redirect(url_for('login'))
        
        return f(data, *args, **kwargs)
    return decorated

@app.route('/')
def index():
    
    return render_template('main.html')

# Routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM roles WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            token = jwt.encode({
                'user_id': user[0],
                'role': user[3],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
            }, app.config['SECRET_KEY'], algorithm='HS256')

            resp = redirect(url_for('dashboard'))
            resp.set_cookie('token', token)
            return resp
        else:
            return "Invalid credentials, try again."

    return render_template('login.html')

@app.route('/register', methods=['POST'])
@token_required
def register(data):
    username = request.form['username']
    password = request.form['password']
    role = request.form['role']

    # Superadmin can only create Admins
    if data['role'] == 'Superadmin' and role != 'Admin':
        return "Superadmin can only create Admins", 403
    
    # Admins can only create Superusers and Users
    if data['role'] == 'Admin' and role not in ['Superuser', 'User']:
        return "Admins can only create Superusers and Users", 403

    conn = connect_db()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO roles (username, password, role, created_by) VALUES (?, ?, ?, ?)",
                       (username, password, role, data['user_id']))
        conn.commit()
    except sqlite3.IntegrityError:
        return "User already exists.", 400
    finally:
        conn.close()

    return redirect(url_for('dashboard'))


@app.route('/update_role/<int:user_id>', methods=['POST'])
@token_required
def update_role(data, user_id):
    # Only Superadmin can assign and manage roles
    if data['role'] != 'Superadmin':
        return "Access denied.", 403

    new_role = request.form['role']

    # Ensure valid roles are being assigned
    if new_role not in ['Admin', 'Superuser', 'User']:
        return "Invalid role.", 400

    conn = connect_db()
    cursor = conn.cursor()

    # Update the role of the specified user
    cursor.execute("UPDATE roles SET role=? WHERE id=?", (new_role, user_id))
    conn.commit()
    conn.close()

    return redirect(url_for('dashboard'))



@app.route('/dashboard')
@token_required
def dashboard(data):
    conn = connect_db()
    cursor = conn.cursor()
    
    # Exclude Superadmin from the list of users displayed
    if data['role'] == 'Superadmin':
        cursor.execute("SELECT id, username, created_by, role FROM roles WHERE role != 'Superadmin'")
    else:
        # For Admins, only show the users they created
        cursor.execute("SELECT id, username, created_by, role FROM roles WHERE created_by=?", (data['user_id'],))
    
    users = cursor.fetchall()
    conn.close()

    return render_template('dashboard.html', users=users, role=data['role'])


@app.route('/logout')
def logout():
    resp = redirect(url_for('login'))
    resp.set_cookie('token', '', expires=0)
    return resp

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(host="0.0.0.0", port =8000)
