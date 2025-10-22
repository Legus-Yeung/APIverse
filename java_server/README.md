# Java Spring Boot Banking Server

A Spring Boot REST API server that provides banking functionality with JWT authentication, similar to the FastAPI server but implemented in Java.

## Features

- **User Registration & Authentication**: Register new users and login with JWT tokens
- **Account Management**: Create, view, deposit, withdraw, transfer, and close accounts
- **JWT Security**: Secure endpoints with JSON Web Tokens
- **Password Hashing**: BCrypt password hashing for security
- **File-based Storage**: JSON file storage for users and accounts data
- **RESTful API**: Clean REST endpoints following Spring Boot conventions

## Prerequisites

- Java 17 or higher
- Maven 3.6 or higher

## Installation & Setup

1. **Clone or navigate to the java_server directory**
   ```bash
   cd java_server
   ```

2. **Install dependencies**
   ```bash
   mvn clean install
   ```

3. **Run the application**
   ```bash
   mvn spring-boot:run
   ```

   The server will start on `http://127.0.0.1:5000`

## API Endpoints

### Authentication Endpoints

#### Register User
- **POST** `/api/register`
- **Body**: `{"username": "string", "password": "string"}`
- **Response**: `{"success": true, "message": "User registered successfully"}`

#### Login
- **POST** `/api/login`
- **Body**: `{"username": "string", "password": "string"}`
- **Response**: `{"success": true, "message": "Login successful", "token": "jwt_token"}`

#### Protected Endpoint (Test)
- **GET** `/api/protected`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{"success": true, "message": "Hello, username!"}`

### Account Endpoints

All account endpoints require authentication via Bearer token.

#### Create Account
- **POST** `/api/accounts/create`
- **Headers**: `Authorization: Bearer <token>`
- **Body**: `{"initial_balance": 0.0}`
- **Response**: `{"success": true, "message": "Account created successfully", "data": {"account_number": "string", "balance": 0.0}}`

#### Get My Account
- **GET** `/api/accounts/my-account`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{"success": true, "account": {"account_number": "string", "balance": 0.0, "created_at": "string"}}`

#### Deposit Money
- **POST** `/api/accounts/deposit`
- **Headers**: `Authorization: Bearer <token>`
- **Body**: `{"amount": 100.0}`
- **Response**: `{"success": true, "message": "Deposited $100.00", "data": {"new_balance": 100.0}}`

#### Withdraw Money
- **POST** `/api/accounts/withdraw`
- **Headers**: `Authorization: Bearer <token>`
- **Body**: `{"amount": 50.0}`
- **Response**: `{"success": true, "message": "Withdrew $50.00", "data": {"new_balance": 50.0}}`

#### Transfer Money
- **POST** `/api/accounts/transfer`
- **Headers**: `Authorization: Bearer <token>`
- **Body**: `{"to_account_number": "string", "amount": 25.0}`
- **Response**: `{"success": true, "message": "Transferred $25.00 to account string", "data": {"new_balance": 25.0}}`

#### Close Account
- **POST** `/api/accounts/close`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: `{"success": true, "message": "Account closed successfully"}`

## Configuration

The application can be configured via `src/main/resources/application.properties`:

```properties
# Server Configuration
server.port=5000
server.address=127.0.0.1

# JWT Configuration
jwt.secret=supersecretkey
jwt.expiration=3600000

# File paths
app.users.file=users.json
app.accounts.file=accounts.json
```

## Data Storage

- **Users**: Stored in `users.json` with hashed passwords
- **Accounts**: Stored in `accounts.json` with account details
- Files are created automatically if they don't exist

## Error Handling

The API returns appropriate HTTP status codes and error messages:

- **400 Bad Request**: Invalid input data or business logic errors
- **401 Unauthorized**: Invalid or missing authentication
- **404 Not Found**: Resource not found (e.g., no active account)

## Testing with Client

This server is compatible with the provided Python client (`client.py`). To use it:

1. Update `client.py` to set `USING_FASTAPI = True` (the Java server uses similar response format)
2. Run the Java server
3. Run the Python client

## Project Structure

```
java_server/
├── src/main/java/com/example/banking/
│   ├── BankingApplication.java          # Main Spring Boot application
│   ├── config/
│   │   └── SecurityConfig.java         # Security configuration
│   ├── controller/
│   │   ├── AuthController.java         # Authentication endpoints
│   │   └── AccountController.java      # Account management endpoints
│   ├── model/
│   │   ├── User.java                   # User model
│   │   ├── Account.java                # Account model
│   │   ├── AccountCreate.java          # Account creation DTO
│   │   ├── AccountBalanceUpdate.java   # Balance update DTO
│   │   ├── AccountTransfer.java        # Transfer DTO
│   │   └── ApiResponse.java            # API response wrapper
│   └── service/
│       ├── JwtService.java             # JWT token handling
│       ├── PasswordService.java        # Password hashing
│       ├── UserService.java           # User management
│       └── AccountService.java         # Account business logic
├── src/main/resources/
│   └── application.properties         # Application configuration
└── pom.xml                            # Maven dependencies
```

## Dependencies

- **Spring Boot**: Web framework and dependency injection
- **Spring Security**: Authentication and authorization
- **JJWT**: JWT token handling
- **Jackson**: JSON processing
- **BCrypt**: Password hashing
- **Validation**: Input validation

## Development

To build and run in development mode:

```bash
# Clean and compile
mvn clean compile

# Run tests
mvn test

# Package application
mvn package

# Run with specific profile
mvn spring-boot:run -Dspring-boot.run.profiles=dev
```
