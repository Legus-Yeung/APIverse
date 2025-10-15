from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from typing import Dict
import uvicorn
import bcrypt
import jwt
import datetime
import os
import json

app = FastAPI()
SECRET_KEY = "supersecretkey"
USERS_FILE = "users.json"

if not os.path.exists(USERS_FILE):
    with open(USERS_FILE, "w") as f:
        json.dump({}, f)

class User(BaseModel):
    username: str
    password: str

security = HTTPBearer()

def load_users():
    with open(USERS_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=4)

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

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=5000)
