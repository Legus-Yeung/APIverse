from flask import Flask, request, jsonify
import json
import os
import bcrypt
import jwt
import datetime

app = Flask(__name__)
SECRET_KEY = "supersecretkey"
USERS_FILE = "users.json"

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password, hashed_password):
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def generate_token(username):
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

@app.route("/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    users = load_users()
    if username in users:
        return jsonify({"success": False, "message": "User already exists"}), 400

    users[username] = hash_password(password)
    save_users(users)

    return jsonify({"success": True, "message": "User registered successfully"}), 201

@app.route("/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    users = load_users()
    if username not in users or not check_password(password, users[username]):
        return jsonify({"success": False, "message": "Invalid credentials"}), 401

    token = generate_token(username)
    return jsonify({"success": True, "message": "Login successful", "token": token})

@app.route("/protected", methods=["GET"])
def protected():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"success": False, "message": "Token required"}), 401

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"success": True, "message": f"Hello, {decoded['username']}!"})
    except jwt.ExpiredSignatureError:
        return jsonify({"success": False, "message": "Token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"success": False, "message": "Invalid token"}), 401

if __name__ == "__main__":
    app.run(debug=True)
