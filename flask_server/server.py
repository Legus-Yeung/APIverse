from flask import Flask, request, jsonify
import json
import os
import bcrypt
import jwt
import datetime
import uuid
from typing import Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict

app = Flask(__name__)
SECRET_KEY = "supersecretkeythatislongenoughtomeetjwtsecurityrequirements256bits"
USERS_FILE = "users.json"
ACCOUNTS_FILE = "accounts.json"

# Initialize data files
if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

if not os.path.exists(ACCOUNTS_FILE):
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump({}, f)

@dataclass
class Account:
    account_number: str
    username: str
    balance: float
    created_at: str

@dataclass
class AccountCreate:
    initial_balance: float

@dataclass
class AccountBalanceUpdate:
    amount: float

@dataclass
class AccountTransfer:
    to_account_number: str
    amount: float

def load_users() -> Dict[str, str]:
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users: Dict[str, str]) -> None:
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def load_accounts() -> Dict[str, Dict[str, Any]]:
    with open(ACCOUNTS_FILE, "r") as f:
        return json.load(f)

def save_accounts(accounts: Dict[str, Dict[str, Any]]) -> None:
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump(accounts, f, indent=4)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def check_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed_password.encode())

def generate_token(username: str) -> str:
    payload = {
        "username": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token: str) -> Optional[str]:
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return decoded["username"]
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None

def generate_account_number() -> str:
    return str(uuid.uuid4().int)[:10]

def get_user_account(username: str) -> Optional[Account]:
    accounts = load_accounts()
    for account_data in accounts.values():
        if account_data["username"] == username:
            return Account(**account_data)
    return None

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

    username = verify_token(token)
    if not username:
        return jsonify({"success": False, "message": "Invalid token"}), 401

    return jsonify({"success": True, "message": f"Hello, {username}!"})

# Banking endpoints
@app.route("/accounts/create", methods=["POST"])
def create_account():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"success": False, "message": "Token required"}), 401

    username = verify_token(token)
    if not username:
        return jsonify({"success": False, "message": "Invalid token"}), 401

    data = request.json
    initial_balance = data.get("initial_balance", 0.0)
    
    if initial_balance < 0:
        return jsonify({"success": False, "message": "Initial balance cannot be negative"}), 400

    # Check if user already has an account
    if get_user_account(username):
        return jsonify({"success": False, "message": "User already has an account"}), 400

    account_number = generate_account_number()
    account = Account(
        account_number=account_number,
        username=username,
        balance=initial_balance,
        created_at=datetime.datetime.utcnow().isoformat()
    )

    accounts = load_accounts()
    accounts[account_number] = asdict(account)
    save_accounts(accounts)

    return jsonify({
        "success": True, 
        "message": "Account created successfully",
        "data": {
            "account_number": account_number,
            "balance": initial_balance
        }
    })

@app.route("/accounts/my-account", methods=["GET"])
def get_my_account():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"success": False, "message": "Token required"}), 401

    username = verify_token(token)
    if not username:
        return jsonify({"success": False, "message": "Invalid token"}), 401

    account = get_user_account(username)
    if not account:
        return jsonify({"success": False, "message": "Account not found"}), 404

    return jsonify({"success": True, "data": asdict(account)})

@app.route("/accounts/deposit", methods=["POST"])
def deposit():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"success": False, "message": "Token required"}), 401

    username = verify_token(token)
    if not username:
        return jsonify({"success": False, "message": "Invalid token"}), 401

    data = request.json
    amount = data.get("amount", 0.0)
    
    if amount <= 0:
        return jsonify({"success": False, "message": "Amount must be positive"}), 400

    account = get_user_account(username)
    if not account:
        return jsonify({"success": False, "message": "Account not found"}), 404

    account.balance += amount
    accounts = load_accounts()
    accounts[account.account_number] = asdict(account)
    save_accounts(accounts)

    return jsonify({
        "success": True,
        "message": f"Deposited ${amount:.2f}",
        "data": {"new_balance": account.balance}
    })

@app.route("/accounts/withdraw", methods=["POST"])
def withdraw():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"success": False, "message": "Token required"}), 401

    username = verify_token(token)
    if not username:
        return jsonify({"success": False, "message": "Invalid token"}), 401

    data = request.json
    amount = data.get("amount", 0.0)
    
    if amount <= 0:
        return jsonify({"success": False, "message": "Amount must be positive"}), 400

    account = get_user_account(username)
    if not account:
        return jsonify({"success": False, "message": "Account not found"}), 404

    if account.balance < amount:
        return jsonify({"success": False, "message": "Insufficient funds"}), 400

    account.balance -= amount
    accounts = load_accounts()
    accounts[account.account_number] = asdict(account)
    save_accounts(accounts)

    return jsonify({
        "success": True,
        "message": f"Withdrew ${amount:.2f}",
        "data": {"new_balance": account.balance}
    })

@app.route("/accounts/transfer", methods=["POST"])
def transfer():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"success": False, "message": "Token required"}), 401

    username = verify_token(token)
    if not username:
        return jsonify({"success": False, "message": "Invalid token"}), 401

    data = request.json
    to_account_number = data.get("to_account_number")
    amount = data.get("amount", 0.0)
    
    if amount <= 0:
        return jsonify({"success": False, "message": "Amount must be positive"}), 400

    if not to_account_number:
        return jsonify({"success": False, "message": "Recipient account number required"}), 400

    accounts = load_accounts()
    
    # Get sender account
    sender_account = get_user_account(username)
    if not sender_account:
        return jsonify({"success": False, "message": "Account not found"}), 404

    # Get recipient account
    if to_account_number not in accounts:
        return jsonify({"success": False, "message": "Recipient account not found"}), 404

    if sender_account.balance < amount:
        return jsonify({"success": False, "message": "Insufficient funds"}), 400

    # Perform transfer
    sender_account.balance -= amount
    recipient_account_data = accounts[to_account_number]
    recipient_account_data["balance"] += amount

    # Save changes
    accounts[sender_account.account_number] = asdict(sender_account)
    accounts[to_account_number] = recipient_account_data
    save_accounts(accounts)

    return jsonify({
        "success": True,
        "message": f"Transferred ${amount:.2f} to account {to_account_number}",
        "data": {"new_balance": sender_account.balance}
    })

@app.route("/accounts/close", methods=["POST"])
def close_account():
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"success": False, "message": "Token required"}), 401

    username = verify_token(token)
    if not username:
        return jsonify({"success": False, "message": "Invalid token"}), 401

    account = get_user_account(username)
    if not account:
        return jsonify({"success": False, "message": "Account not found"}), 404

    if account.balance > 0:
        return jsonify({"success": False, "message": "Account must have zero balance to be closed"}), 400

    accounts = load_accounts()
    del accounts[account.account_number]
    save_accounts(accounts)

    return jsonify({"success": True, "message": "Account closed successfully"})

if __name__ == "__main__":
    app.run(debug=True)
