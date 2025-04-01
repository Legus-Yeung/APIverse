# Flask/FastAPI User Authentication

This repository demonstrates user authentication implementation using both Flask and FastAPI frameworks, featuring a simple GUI client to test both servers. The project includes password hashing, JWT token authentication, and a shared user storage system.

## Features

- User registration and login functionality
- Password hashing using bcrypt
- JWT token-based authentication
- Shared JSON file-based user storage
- GUI client application using Tkinter
- Support for both Flask and FastAPI backends

## Project Structure

- `flask_server.py` - Flask implementation of the authentication server
- `fastapi_server.py` - FastAPI implementation of the authentication server
- `client.py` - Tkinter-based GUI client that works with both servers
- `requirements.txt` - Project dependencies
- `users.json` - JSON file storing user credentials (automatically created)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd flask-fastapi-user-auth
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Starting the Servers

You can run either the Flask server or the FastAPI server:

For Flask:
```bash
python flask_server.py
```
The Flask server will run on `http://127.0.0.1:5000`

For FastAPI:
```bash
python fastapi_server.py
```
The FastAPI server will also run on `http://127.0.0.1:5000`

### Running the Client

1. Open `client.py` and set the `USING_FASTAPI` variable to `True` for FastAPI server or `False` for Flask server
2. Run the client:
```bash
python client.py
```

## API Endpoints

Both servers implement the same endpoints:

### 1. Register User
- **Endpoint:** `/register`
- **Method:** POST
- **Body:**
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

### 2. Login
- **Endpoint:** `/login`
- **Method:** POST
- **Body:**
```json
{
    "username": "your_username",
    "password": "your_password"
}
```

### 3. Protected Route
- **Endpoint:** `/protected`
- **Method:** GET
- **Headers:** Authorization: Bearer <token> (FastAPI) or Authorization: <token> (Flask)

## Security Features

- Passwords are hashed using bcrypt before storage
- JWT tokens expire after 1 hour
- Protected routes require valid JWT tokens
- Password verification using secure comparison

## Dependencies

- FastAPI and Flask for server implementations
- bcrypt for password hashing
- JWT for token-based authentication
- Tkinter for GUI client
- Requests for HTTP client operations
- Uvicorn as ASGI server for FastAPI

## Notes

- This is a demonstration project and may need additional security measures for production use
- The `users.json` file is created automatically when first running either server
- Both servers share the same user database through `users.json`
- The client can switch between Flask and FastAPI servers by modifying the `USING_FASTAPI` flag