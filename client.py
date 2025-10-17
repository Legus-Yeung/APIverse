import tkinter as tk
from tkinter import messagebox, ttk
import requests

BACKEND_URL = "http://127.0.0.1:5000"
USING_FASTAPI = True

token = None
current_account = None

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

def get_headers():
    """Get headers with authentication token"""
    if USING_FASTAPI:
        return {"Authorization": f"Bearer {token}"}
    else:
        return {"Authorization": token}

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
    global token, current_account
    username = entry_username.get()
    password = entry_password.get()

    response = requests.post(f"{BACKEND_URL}/login", json={"username": username, "password": password})

    if response.status_code in [200, 201]:
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
    response = requests.get(f"{BACKEND_URL}/protected", headers=get_headers())
    if response.status_code in [200, 201]:
        data = response.json()
        messagebox.showinfo("Response", data.get("message", "Access granted!"))
    else:
        error_msg = get_error_message(response)
        messagebox.showerror("Access Failed", error_msg)

def create_account():
    """Create a new account"""
    def create():
        try:
            initial_balance = float(initial_balance_entry.get())
            if initial_balance < 0:
                messagebox.showerror("Error", "Initial balance cannot be negative")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
            return
        
        response = requests.post(
            f"{BACKEND_URL}/accounts/create", 
            json={"initial_balance": initial_balance},
            headers=get_headers()
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            messagebox.showinfo("Success", f"Account created!\nAccount Number: {data['account_number']}\nBalance: ${data['balance']:.2f}")
            create_window.destroy()
            refresh_account_info()
        else:
            error_msg = get_error_message(response)
            messagebox.showerror("Error", error_msg)
    
    create_window = tk.Toplevel()
    create_window.title("Create Account")
    create_window.geometry("300x150")
    create_window.configure(padx=20, pady=20)
    
    tk.Label(create_window, text="Initial Balance:").pack(pady=5)
    initial_balance_entry = tk.Entry(create_window)
    initial_balance_entry.pack(pady=5)
    initial_balance_entry.insert(0, "0.00")
    
    tk.Button(create_window, text="Create Account", command=create).pack(pady=10)

def get_account_info():
    """Get current account information"""
    global current_account
    response = requests.get(f"{BACKEND_URL}/accounts/my-account", headers=get_headers())
    
    if response.status_code in [200, 201]:
        data = response.json()
        current_account = data['account']
        return current_account
    else:
        current_account = None
        return None

def refresh_account_info():
    """Refresh and display account information"""
    account = get_account_info()
    if account:
        account_info_label.config(text=f"Account: {account['account_number']}\nBalance: ${account['balance']:.2f}")
        for widget in account_operations_frame.winfo_children():
            widget.config(state='normal')
    else:
        account_info_label.config(text="No active account found")
        widgets = account_operations_frame.winfo_children()
        for i, widget in enumerate(widgets):
            if i == 0:
                widget.config(state='normal')
            else:
                widget.config(state='disabled')

def deposit():
    """Deposit money to account"""
    def perform_deposit():
        try:
            amount = float(amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
            return
        
        response = requests.post(
            f"{BACKEND_URL}/accounts/deposit", 
            json={"amount": amount},
            headers=get_headers()
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            messagebox.showinfo("Success", f"Deposited ${amount:.2f}\nNew Balance: ${data['new_balance']:.2f}")
            deposit_window.destroy()
            refresh_account_info()
        else:
            error_msg = get_error_message(response)
            messagebox.showerror("Error", error_msg)
    
    deposit_window = tk.Toplevel()
    deposit_window.title("Deposit Money")
    deposit_window.geometry("300x150")
    deposit_window.configure(padx=20, pady=20)
    
    tk.Label(deposit_window, text="Amount to Deposit:").pack(pady=5)
    amount_entry = tk.Entry(deposit_window)
    amount_entry.pack(pady=5)
    
    tk.Button(deposit_window, text="Deposit", command=perform_deposit).pack(pady=10)

def withdraw():
    """Withdraw money from account"""
    def perform_withdraw():
        try:
            amount = float(amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
            return
        
        response = requests.post(
            f"{BACKEND_URL}/accounts/withdraw", 
            json={"amount": amount},
            headers=get_headers()
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            messagebox.showinfo("Success", f"Withdrew ${amount:.2f}\nNew Balance: ${data['new_balance']:.2f}")
            withdraw_window.destroy()
            refresh_account_info()
        else:
            error_msg = get_error_message(response)
            messagebox.showerror("Error", error_msg)
    
    withdraw_window = tk.Toplevel()
    withdraw_window.title("Withdraw Money")
    withdraw_window.geometry("300x150")
    withdraw_window.configure(padx=20, pady=20)
    
    tk.Label(withdraw_window, text="Amount to Withdraw:").pack(pady=5)
    amount_entry = tk.Entry(withdraw_window)
    amount_entry.pack(pady=5)
    
    tk.Button(withdraw_window, text="Withdraw", command=perform_withdraw).pack(pady=10)

def transfer():
    """Transfer money to another account"""
    def perform_transfer():
        try:
            amount = float(amount_entry.get())
            if amount <= 0:
                messagebox.showerror("Error", "Amount must be positive")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
            return
        
        to_account = to_account_entry.get().strip()
        if not to_account:
            messagebox.showerror("Error", "Please enter recipient account number")
            return
        
        response = requests.post(
            f"{BACKEND_URL}/accounts/transfer", 
            json={"to_account_number": to_account, "amount": amount},
            headers=get_headers()
        )
        
        if response.status_code in [200, 201]:
            data = response.json()
            messagebox.showinfo("Success", f"Transferred ${amount:.2f} to account {to_account}\nNew Balance: ${data['new_balance']:.2f}")
            transfer_window.destroy()
            refresh_account_info()
        else:
            error_msg = get_error_message(response)
            messagebox.showerror("Error", error_msg)
    
    transfer_window = tk.Toplevel()
    transfer_window.title("Transfer Money")
    transfer_window.geometry("350x200")
    transfer_window.configure(padx=20, pady=20)
    
    tk.Label(transfer_window, text="Recipient Account Number:").pack(pady=5)
    to_account_entry = tk.Entry(transfer_window)
    to_account_entry.pack(pady=5)
    
    tk.Label(transfer_window, text="Amount to Transfer:").pack(pady=5)
    amount_entry = tk.Entry(transfer_window)
    amount_entry.pack(pady=5)
    
    tk.Button(transfer_window, text="Transfer", command=perform_transfer).pack(pady=10)

def close_account():
    """Close the current account"""
    if messagebox.askyesno("Confirm", "Are you sure you want to close your account? This action cannot be undone."):
        response = requests.post(f"{BACKEND_URL}/accounts/close", headers=get_headers())
        
        if response.status_code in [200, 201]:
            messagebox.showinfo("Success", "Account closed successfully")
            refresh_account_info()
        else:
            error_msg = get_error_message(response)
            messagebox.showerror("Error", error_msg)

def open_main_app():
    global account_info_label, account_operations_frame
    
    app = tk.Tk()
    app.title("Banking App")
    app.geometry("500x600")
    app.configure(padx=30, pady=30)

    tk.Label(app, text="Welcome! You are authenticated.", font=("Arial", 14)).pack(pady=20)
    
    account_frame = tk.Frame(app)
    account_frame.pack(fill="x", pady=10)
    
    tk.Label(account_frame, text="Account Information:", font=("Arial", 12, "bold")).pack()
    account_info_label = tk.Label(account_frame, text="Loading...", font=("Arial", 10))
    account_info_label.pack(pady=5)
    
    tk.Button(account_frame, text="Refresh Account Info", command=refresh_account_info).pack(pady=5)
    
    operations_frame = tk.Frame(app)
    operations_frame.pack(fill="x", pady=20)
    
    tk.Label(operations_frame, text="Account Operations:", font=("Arial", 12, "bold")).pack()
    
    account_operations_frame = tk.Frame(operations_frame)
    account_operations_frame.pack(pady=10)
    
    tk.Button(account_operations_frame, text="Create Account", command=create_account, width=15).grid(row=0, column=0, padx=5, pady=5)
    tk.Button(account_operations_frame, text="Deposit", command=deposit, width=15).grid(row=0, column=1, padx=5, pady=5)
    tk.Button(account_operations_frame, text="Withdraw", command=withdraw, width=15).grid(row=0, column=2, padx=5, pady=5)
    tk.Button(account_operations_frame, text="Transfer", command=transfer, width=15).grid(row=1, column=0, padx=5, pady=5)
    tk.Button(account_operations_frame, text="Close Account", command=close_account, width=15).grid(row=1, column=1, padx=5, pady=5)
    
    other_frame = tk.Frame(app)
    other_frame.pack(fill="x", pady=20)
    
    tk.Label(other_frame, text="Other Operations:", font=("Arial", 12, "bold")).pack()
    tk.Button(other_frame, text="Access Protected", command=access_protected, width=15).pack(pady=5)
    tk.Button(other_frame, text="Exit", command=app.quit, width=15).pack(pady=5)
    
    refresh_account_info()
    
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