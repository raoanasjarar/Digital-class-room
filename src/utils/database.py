import sqlite3
import hashlib

def connect_db(db_name):
    conn = sqlite3.connect(db_name)
    return conn

def create_user_table(conn):
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                user_type TEXT NOT NULL
            )
        ''')
    with conn:
        cursor = conn.cursor()
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'user_type' not in columns:
            conn.execute("ALTER TABLE users ADD COLUMN user_type TEXT NOT NULL DEFAULT 'student'")
    print("User table created or already exists.")

def get_users(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, password, user_type FROM users')
    return cursor.fetchall()

def create_assignment_table(conn):
    with conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT,
                status TEXT NOT NULL
            )
        ''')

def add_user(conn, username, password, user_type):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    with conn:
        conn.execute('''
            INSERT INTO users (username, password, user_type)
            VALUES (?, ?, ?)
        ''', (username, hashed_password, user_type))

def update_user(conn, user_id, username, password, user_type):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    with conn:
        conn.execute('''
            UPDATE users
            SET username = ?, password = ?, user_type = ?
            WHERE id = ?
        ''', (username, hashed_password, user_type))

def get_users(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    return cursor.fetchall()

def add_assignment(conn, title, description, due_date, status):
    with conn:
        conn.execute('''
            INSERT INTO assignments (title, description, due_date, status)
            VALUES (?, ?, ?, ?)
        ''', (title, description, due_date, status))

def get_assignments(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM assignments')
    return cursor.fetchall()

def get_assignment_by_id(conn, assignment_id):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM assignments WHERE id = ?', (assignment_id,))
    return cursor.fetchone()

def update_assignment(conn, assignment_id, title, description, due_date, status):
    with conn:
        conn.execute('''
            UPDATE assignments
            SET title = ?, description = ?, due_date = ?, status = ?
            WHERE id = ?
        ''', (title, description, due_date, status, assignment_id))

def delete_assignment(conn, assignment_id):
    with conn:
        conn.execute('DELETE FROM assignments WHERE id = ?', (assignment_id,))

def update_user_type(conn, username, user_type):
    with conn:
        conn.execute('''
            UPDATE users
            SET user_type = ?
            WHERE username = ?
        ''', (user_type, username))