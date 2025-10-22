# Multi-Backend User Authentication & Banking System

This project provides multiple backend implementations (Flask, FastAPI, Java Spring Boot, NestJS, and Go) of a user authentication system with banking functionality, all compatible with a single GUI client.

## Project Structure

```
flask-fastapi-user-auth/
├── fastapi_server/
│   └── server.py          # FastAPI server with full banking functionality
├── flask_server/
│   └── server.py          # Flask server with basic authentication
├── java_server/           # Java Spring Boot server with full banking functionality
│   ├── src/main/java/com/example/banking/
│   │   ├── controller/    # REST controllers
│   │   ├── service/       # Business logic services
│   │   ├── model/         # Data models
│   │   └── config/        # Security and JWT configuration
│   ├── pom.xml           # Maven dependencies
│   └── users.json        # User data storage
├── nestjs_server/         # NestJS TypeScript server with full banking functionality
│   ├── src/
│   │   ├── auth/         # Authentication module
│   │   ├── account/      # Account management module
│   │   └── main.ts       # Application entry point
│   ├── package.json      # Node.js dependencies
│   └── users.json        # User data storage
├── go_server/            # Go server with full banking functionality
│   ├── main.go          # Main application file
│   ├── go.mod           # Go module dependencies
│   └── users.json        # User data storage
├── client.py             # Universal GUI client for all backends
├── requirements.txt      # Python dependencies
└── readme.md            # This file
```

## Features

### Authentication
- User registration and login
- JWT token-based authentication
- Password hashing with bcrypt

### Banking Operations (All Backends)
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

### Python Backends (Flask & FastAPI)
1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Java Spring Boot Backend
1. Install Java 17 or higher
2. Install Maven 3.6 or higher
3. Navigate to the Java server directory:
```bash
cd java_server
mvn clean install
```

### Go Backend
1. Install Go 1.19 or higher
2. Navigate to the Go server directory:
```bash
cd go_server
go mod tidy
```

## Running the Application

### FastAPI Server (Python - Recommended)
```bash
cd fastapi_server
python server.py
```
Server runs on: http://127.0.0.1:5000

### Java Spring Boot Server (Java - Full Featured)
```bash
cd java_server
mvn spring-boot:run
```
Server runs on: http://127.0.0.1:5000

### NestJS Server (TypeScript - Full Featured)
```bash
cd nestjs_server
npm run start:dev
```
Server runs on: http://127.0.0.1:5000

### Go Server (Go - Full Featured)
```bash
cd go_server
go run main.go
```
Server runs on: http://127.0.0.1:5000

### Flask Server (Python - Full Featured)
```bash
cd flask_server
python server.py
```
Server runs on: http://127.0.0.1:5000 (default Flask port)

### Universal Client Application
```bash
python client.py
```
**Note**: The client automatically detects and works with any of the five backend servers.

## API Endpoints

### Authentication Endpoints
- `POST /register` - Register a new user
- `POST /login` - Login and get JWT token
- `GET /protected` - Access protected resource

### Banking Endpoints (All Backends)
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

### Python Backends (Flask & FastAPI)
- User data: `users.json`
- Account data: `accounts.json`

### Java Spring Boot Backend
- User data: `users.json` (BCrypt hashed passwords)
- Account data: `accounts.json`

### Go Backend
- User data: `users.json` (BCrypt hashed passwords)
- Account data: `accounts.json`

All data files are created automatically when the servers start.

## Usage Example

1. Start any backend server (FastAPI, Java Spring Boot, NestJS, Go, or Flask)
2. Run the client application
3. Register a new user or login
4. Create an account with initial balance (All backends support this)
5. Perform banking operations (deposit, withdraw, transfer)
6. View account information and balance

## Backend Comparison

| Feature | Flask | FastAPI | Java Spring Boot | NestJS | Go |
|---------|-------|---------|------------------|-------|---|
| Authentication | ✅ | ✅ | ✅ | ✅ | ✅ |
| Banking Operations | ✅ | ✅ | ✅ | ✅ | ✅ |
| JWT Tokens | ✅ | ✅ | ✅ | ✅ | ✅ |
| Password Hashing | ✅ | ✅ | ✅ (BCrypt) | ✅ (BCrypt) | ✅ (BCrypt) |
| Data Storage | JSON | JSON | JSON | JSON | JSON |
| Performance | Good | Excellent | Excellent | Excellent | Excellent |
| Type Safety | ✅ | ✅ | ✅ | ✅ | ✅ |
| Language | Python | Python | Java | TypeScript | Go |

## Notes

- Each user can have only one active account
- Account numbers are unique 10-digit identifiers
- Transfers require valid recipient account numbers
- Accounts must have zero balance to be closed
- JWT tokens expire after 1 hour
- The client automatically adapts to different backend response formats
- Java Spring Boot and NestJS use BCrypt for enhanced password security
- Choose your preferred technology stack: Python (Flask/FastAPI), Java (Spring Boot), TypeScript (NestJS), or Go