# NestJS User Authentication Server

This is a NestJS implementation of the user authentication and account management server, equivalent to the FastAPI version.

## Features

- User registration and login with JWT authentication
- Account creation, management, and operations
- Deposit, withdraw, and transfer functionality
- Account closure
- File-based data persistence (users.json, accounts.json)
- TypeScript with decorators and dependency injection
- Built-in validation and error handling

## Prerequisites

- Node.js 18 or later
- npm or yarn

## Installation

1. Navigate to the nestjs_server directory:
```bash
cd nestjs_server
```

2. Install dependencies:
```bash
npm install
```

## Running the Server

### Development Mode
```bash
npm run start:dev
```

### Production Mode
```bash
npm run build
npm run start:prod
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

## Project Structure

```
src/
├── auth/
│   ├── auth.controller.ts
│   ├── auth.module.ts
│   ├── auth.service.ts
│   ├── jwt-auth.guard.ts
│   ├── jwt.strategy.ts
│   └── get-user.decorator.ts
├── account/
│   ├── account.controller.ts
│   ├── account.module.ts
│   └── account.service.ts
├── app.controller.ts
├── app.module.ts
├── app.service.ts
└── main.ts
```

## Key Dependencies

- `@nestjs/core` - NestJS core framework
- `@nestjs/jwt` - JWT authentication
- `@nestjs/passport` - Passport integration
- `passport-jwt` - JWT strategy for Passport
- `bcrypt` - Password hashing
- `class-validator` - Validation decorators
- `class-transformer` - Object transformation

## Development Commands

- `npm run start:dev` - Start in development mode with hot reload
- `npm run build` - Build the application
- `npm run start:prod` - Start in production mode
- `npm run test` - Run unit tests
- `npm run test:e2e` - Run end-to-end tests
- `npm run lint` - Run ESLint
