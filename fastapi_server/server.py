from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Dict, Optional
import uvicorn
import bcrypt
import jwt
import datetime
import os
import json
import uuid

app = FastAPI()
SECRET_KEY = "supersecretkey"
USERS_FILE = "users.json"
ACCOUNTS_FILE = "accounts.json"

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

if not os.path.exists(ACCOUNTS_FILE):
    with open(ACCOUNTS_FILE, "w") as f:
        json.dump({}, f)

class User(BaseModel):
    username: str
    password: str

class AccountCreate(BaseModel):
    initial_balance: float = 0.0

class AccountBalanceUpdate(BaseModel):
    amount: float

class AccountTransfer(BaseModel):
    to_account_number: str
    amount: float

class Account(BaseModel):
    account_number: str
    username: str
    balance: float
    is_active: bool = True
    created_at: str

security = HTTPBearer()

def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

def load_accounts():
    with open(ACCOUNTS_FILE, "r") as f:
        return json.load(f)

def save_accounts(accounts):
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

def generate_account_number() -> str:
    """Generate a unique account number"""
    while True:
        account_number = str(uuid.uuid4().int)[:10]
        accounts = load_accounts()
        if account_number not in accounts:
            return account_number

async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.post("/register")
def register(user: User):
    users = load_users()
    if user.username in users:
        raise HTTPException(status_code=400, detail="User already exists")
    
    users[user.username] = hash_password(user.password)
    save_users(users)
    
    return {"success": True, "message": "User registered successfully"}

@app.post("/login")
def login(user: User):
    users = load_users()
    if user.username not in users or not check_password(user.password, users[user.username]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = generate_token(user.username)
    return {"success": True, "message": "Login successful", "token": token}

@app.get("/protected")
def protected(token: str = Depends(verify_token)):
    return {"success": True, "message": f"Hello, {token['username']}!"}

@app.post("/accounts/create")
def create_account(account_data: AccountCreate, token: str = Depends(verify_token)):
    username = token['username']
    accounts = load_accounts()
    
    for account_number, account in accounts.items():
        if account['username'] == username and account['is_active']:
            raise HTTPException(status_code=400, detail="User already has an active account")
    
    account_number = generate_account_number()
    new_account = {
        "account_number": account_number,
        "username": username,
        "balance": account_data.initial_balance,
        "is_active": True,
        "created_at": datetime.datetime.utcnow().isoformat()
    }
    
    accounts[account_number] = new_account
    save_accounts(accounts)
    
    return {
        "success": True, 
        "message": "Account created successfully",
        "account_number": account_number,
        "balance": account_data.initial_balance
    }

@app.get("/accounts/my-account")
def get_my_account(token: str = Depends(verify_token)):
    username = token['username']
    accounts = load_accounts()
    
    for account_number, account in accounts.items():
        if account['username'] == username and account['is_active']:
            return {
                "success": True,
                "account": {
                    "account_number": account['account_number'],
                    "balance": account['balance'],
                    "created_at": account['created_at']
                }
            }
    
    raise HTTPException(status_code=404, detail="No active account found")

@app.post("/accounts/deposit")
def deposit(amount_data: AccountBalanceUpdate, token: str = Depends(verify_token)):
    username = token['username']
    amount = amount_data.amount
    
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    accounts = load_accounts()
    
    for account_number, account in accounts.items():
        if account['username'] == username and account['is_active']:
            account['balance'] += amount
            save_accounts(accounts)
            return {
                "success": True,
                "message": f"Deposited ${amount:.2f}",
                "new_balance": account['balance']
            }
    
    raise HTTPException(status_code=404, detail="No active account found")

@app.post("/accounts/withdraw")
def withdraw(amount_data: AccountBalanceUpdate, token: str = Depends(verify_token)):
    username = token['username']
    amount = amount_data.amount
    
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    accounts = load_accounts()
    
    for account_number, account in accounts.items():
        if account['username'] == username and account['is_active']:
            if account['balance'] < amount:
                raise HTTPException(status_code=400, detail="Insufficient funds")
            
            account['balance'] -= amount
            save_accounts(accounts)
            return {
                "success": True,
                "message": f"Withdrew ${amount:.2f}",
                "new_balance": account['balance']
            }
    
    raise HTTPException(status_code=404, detail="No active account found")

@app.post("/accounts/transfer")
def transfer(transfer_data: AccountTransfer, token: str = Depends(verify_token)):
    username = token['username']
    to_account_number = transfer_data.to_account_number
    amount = transfer_data.amount
    
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be positive")
    
    accounts = load_accounts()
    
    sender_account = None
    sender_account_number = None
    for account_number, account in accounts.items():
        if account['username'] == username and account['is_active']:
            sender_account = account
            sender_account_number = account_number
            break
    
    if not sender_account:
        raise HTTPException(status_code=404, detail="No active account found")
    
    if to_account_number not in accounts:
        raise HTTPException(status_code=404, detail="Recipient account not found")
    
    recipient_account = accounts[to_account_number]
    if not recipient_account['is_active']:
        raise HTTPException(status_code=400, detail="Recipient account is not active")
    
    if sender_account['balance'] < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")
    
    sender_account['balance'] -= amount
    recipient_account['balance'] += amount
    save_accounts(accounts)
    
    return {
        "success": True,
        "message": f"Transferred ${amount:.2f} to account {to_account_number}",
        "new_balance": sender_account['balance']
    }

@app.post("/accounts/close")
def close_account(token: str = Depends(verify_token)):
    username = token['username']
    accounts = load_accounts()
    
    for account_number, account in accounts.items():
        if account['username'] == username and account['is_active']:
            if account['balance'] > 0:
                raise HTTPException(status_code=400, detail="Cannot close account with remaining balance. Please withdraw all funds first.")
            
            account['is_active'] = False
            save_accounts(accounts)
            return {
                "success": True,
                "message": "Account closed successfully"
            }
    
    raise HTTPException(status_code=404, detail="No active account found")

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
