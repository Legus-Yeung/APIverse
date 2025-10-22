# Go User Authentication Server

This is a Go implementation of the user authentication and account management server, equivalent to the FastAPI version.

## Features

- User registration and login with JWT authentication
- Account creation, management, and operations
- Deposit, withdraw, and transfer functionality
- Account closure
- File-based data persistence (users.json, accounts.json)

## Prerequisites

- Go 1.21 or later

## Installation

1. Navigate to the go_server directory:
```bash
cd go_server
```

2. Install dependencies:
```bash
go mod tidy
```

## Running the Server

```bash
go run main.go
```

The server will start on `http://127.0.0.1:5000`

## API Endpoints

### Authentication
- `POST /register` - Register a new user
- `POST /login` - Login and get JWT token
- `GET /protected` - Protected endpoint (requires Bearer token)

### Account Management
- `POST /accounts/create` - Create a new account
- `GET /accounts/my-account` - Get current user's account
- `POST /accounts/deposit` - Deposit money
- `POST /accounts/withdraw` - Withdraw money
- `POST /accounts/transfer` - Transfer money to another account
- `POST /accounts/close` - Close account

## Usage Example

1. Register a user:
```bash
curl -X POST http://127.0.0.1:5000/register \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'
```

2. Login:
```bash
curl -X POST http://127.0.0.1:5000/login \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'
```

3. Use the token for protected endpoints:
```bash
curl -X GET http://127.0.0.1:5000/protected \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

## Dependencies

- `github.com/golang-jwt/jwt/v5` - JWT token handling
- `github.com/gorilla/mux` - HTTP router
- `golang.org/x/crypto` - Password hashing with bcrypt
