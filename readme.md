# Flask-FastAPI User Authentication & Banking System

This project provides both Flask and FastAPI implementations of a user authentication system with banking functionality.

## Project Structure

```
flask-fastapi-user-auth/
├── fastapi_server/
│   └── server.py          # FastAPI server with full banking functionality
├── flask_server/
│   └── server.py          # Flask server with basic authentication
├── client.py              # GUI client for banking operations
├── requirements.txt       # Python dependencies
└── readme.md             # This file
```

## Features

### Authentication
- User registration and login
- JWT token-based authentication
- Password hashing with bcrypt

### Banking Operations (FastAPI only)
- **Create Account**: Create a new bank account with initial balance
- **Deposit**: Add money to your account
- **Withdraw**: Remove money from your account (with balance validation)
- **Transfer**: Send money to another account
- **Close Account**: Close your account (requires zero balance)
- **Account Info**: View account details and balance

### Security Features
- Unique account numbers (10-digit UUID-based)
- Balance validation for withdrawals and transfers
- Account ownership verification
- Token expiration handling

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Running the Application

### FastAPI Server (Recommended)
```bash
cd fastapi_server
python server.py
```
Server runs on: http://127.0.0.1:5000

### Flask Server (Basic Authentication Only)
```bash
cd flask_server
python server.py
```
Server runs on: http://127.0.0.1:5000 (default Flask port)

### Client Application
```bash
python client.py
```

## API Endpoints

### Authentication Endpoints
- `POST /register` - Register a new user
- `POST /login` - Login and get JWT token
- `GET /protected` - Access protected resource

### Banking Endpoints (FastAPI only)
- `POST /accounts/create` - Create a new account
- `GET /accounts/my-account` - Get account information
- `POST /accounts/deposit` - Deposit money
- `POST /accounts/withdraw` - Withdraw money
- `POST /accounts/transfer` - Transfer money to another account
- `POST /accounts/close` - Close account

## Client Features

The GUI client provides:
- User registration and login
- Account creation with initial balance
- Deposit and withdrawal operations
- Money transfers between accounts
- Account closure
- Real-time balance updates
- Error handling and validation

## Data Storage

- User data: `users.json`
- Account data: `accounts.json` (FastAPI only)

Both files are created automatically when the servers start.

## Usage Example

1. Start the FastAPI server
2. Run the client application
3. Register a new user or login
4. Create an account with initial balance
5. Perform banking operations (deposit, withdraw, transfer)
6. View account information and balance

## Notes

- Each user can have only one active account
- Account numbers are unique 10-digit identifiers
- Transfers require valid recipient account numbers
- Accounts must have zero balance to be closed
- JWT tokens expire after 1 hour