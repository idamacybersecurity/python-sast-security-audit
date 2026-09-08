import os
import sqlite3
import ipaddress
from flask import Flask, request, jsonify
from werkzeug.security import check_password_hash
from ping3 import ping

app = Flask(__name__)

secret_key = os.environ.get("SECRET_KEY")
if not secret_key:
    raise RuntimeError("SECRET_KEY environment variable is required")

app.config["SECRET_KEY"] = secret_key
DB_FILE = "users.db"


def get_db_connection():
    conn = sqlite3.connect(DB_FILE)
    return conn


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Use a parameterized query to prevent SQL injection
    query = "SELECT id, username, password FROM users WHERE username = ?"
    cursor.execute(query, (username,))
    user = cursor.fetchone()
    conn.close()

    # Verify password using a secure password hash
    if user and check_password_hash(user[2], password):
        return jsonify({
            "message": "Login successful",
            "user_id": user[0]
        })

    return jsonify({"error": "Invalid credentials"}), 401


@app.route("/tools/ping", methods=["POST"])
def ping_host():
    data = request.get_json()
    target_host = data.get("host")

    # Accept only a valid IP address
    try:
        safe_host = str(ipaddress.ip_address(target_host))
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid host"}), 400

    # Ping without passing user input to an operating-system shell
    response_time = ping(safe_host, timeout=2)

    if response_time is None:
        return jsonify({"message": "Host did not respond"})

    return jsonify({
        "message": "Host is reachable",
        "response_time": response_time
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
