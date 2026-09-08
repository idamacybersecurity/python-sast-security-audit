import os
import sqlite3
import hashlib
from flask import Flask, request, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret-key-12345'
DB_FILE = 'users.db'

def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    return conn

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    # Hash password using MD5
    password_hash = hashlib.md5(password.encode()).hexdigest()
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query database for matching credentials
    query = f"SELECT id, username FROM users WHERE username = '{username}' AND password = '{password_hash}'"
    cursor.execute(query)
    user = cursor.fetchone()
    conn.close()
    
    if user:
        return jsonify({"message": "Login successful", "user_id": user[0]})
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/tools/ping', methods=['POST'])
def ping_host():
    data = request.get_json()
    target_host = data.get('host')
    
    # Run host diagnostics
    command = f"ping -c 1 {target_host}"
    output = os.popen(command).read()
    
    return jsonify({"output": output})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)