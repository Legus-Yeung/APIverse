import tkinter as tk
from tkinter import messagebox
import requests

BACKEND_URL = "http://127.0.0.1:5000"
USING_FASTAPI = True

def get_error_message(response):
    """Extract error message from either FastAPI or Flask response"""
    try:
        json_response = response.json()
        if "detail" in json_response:
            return json_response["detail"]
        elif "message" in json_response:
            return json_response["message"]
        return "An error occurred"
    except:
        return "Unknown error occurred"

def register():
    username = entry_username.get()
    password = entry_password.get()
    
    response = requests.post(f"{BACKEND_URL}/register", json={"username": username, "password": password})

    if response.status_code in [200, 201]:
        messagebox.showinfo("Registration", "User registered successfully!")
    else:
        error_msg = get_error_message(response)
        messagebox.showerror("Registration Failed", error_msg)

def login():
    global token
    username = entry_username.get()
    password = entry_password.get()

    response = requests.post(f"{BACKEND_URL}/login", json={"username": username, "password": password})

    if response.status_code == 200:
        data = response.json()
        token = data.get("token")
        if token:
            messagebox.showinfo("Login Success", "Welcome!")
            root.destroy()
            open_main_app()
        else:
            messagebox.showerror("Login Failed", "No token received")
    else:
        error_msg = get_error_message(response)
        messagebox.showerror("Login Failed", error_msg)

def access_protected():
    if USING_FASTAPI:
        headers = {"Authorization": f"Bearer {token}"}
    else:
        headers = {"Authorization": token}
    
    response = requests.get(f"{BACKEND_URL}/protected", headers=headers)
    if response.status_code == 200:
        data = response.json()
        messagebox.showinfo("Response", data.get("message", "Access granted!"))
    else:
        error_msg = get_error_message(response)
        messagebox.showerror("Access Failed", error_msg)

def open_main_app():
    app = tk.Tk()
    app.title("Main App")
    app.geometry("400x300")
    app.configure(padx=30, pady=30)

    tk.Label(app, text="Welcome! You are authenticated.", font=("Arial", 14)).pack(pady=20)
    tk.Button(app, text="Access Protected", command=access_protected, width=15).pack(pady=10)
    tk.Button(app, text="Exit", command=app.quit, width=15).pack(pady=10)

    app.mainloop()

root = tk.Tk()
root.title("Login/Register")
root.geometry("300x200")
root.configure(padx=20, pady=20)

tk.Label(root, text="Username:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
tk.Label(root, text="Password:").grid(row=1, column=0, padx=5, pady=5, sticky="e")

entry_username = tk.Entry(root)
entry_password = tk.Entry(root, show="*")

entry_username.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
entry_password.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

button_frame = tk.Frame(root)
button_frame.grid(row=2, column=0, columnspan=2, pady=10)

tk.Button(button_frame, text="Register", command=register, width=10).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Login", command=login, width=10).pack(side=tk.LEFT, padx=5)

root.grid_columnconfigure(1, weight=1)

root.mainloop()
