import sqlite3
from hashlib import sha256

def hash_password(password):
    return sha256(password.encode()).hexdigest()

conn = sqlite3.connect('users.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
)
''')

# Insert users with hashed passwords using Python, not SQL
cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
               ('John Doe', 'john@example.com', hash_password('password123')))

cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
               ('Jane Smith', 'jane@example.com', hash_password('secret456')))

cursor.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
               ('Bob Johnson', 'bob@example.com', hash_password('qwerty789')))

conn.commit()
conn.close()

print("Database initialized with hashed sample data")
