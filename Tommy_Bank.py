import json
import tkinter as tk
from tkinter import messagebox

def save_user_data(data, filename="user_data.json"):
    """Saves user data to a JSON file."""
    with open(filename, "w") as f:
        json.dump(data, f)

def load_user_data(filename="user_data.json"):
    """Loads user data from a JSON file."""
    try:
        with open(filename, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}  # Return an empty dictionary if the file doesn't exist

class BankApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bank Application")
        self.users = load_user_data()
        self.current_user = None

        self.main_menu()

    def main_menu(self):
        self.clear_window()

        tk.Label(self.root, text="Welcome to the Bank", font=("Arial", 18)).pack(pady=10)

        tk.Button(self.root, text="Create Account", command=self.create_account_window).pack(pady=5)
        tk.Button(self.root, text="Log In", command=self.login_window).pack(pady=5)
        tk.Button(self.root, text="Exit", command=self.root.quit).pack(pady=5)

    def create_account_window(self):
        self.clear_window()

        tk.Label(self.root, text="Create Account", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        def create_account():
            username = username_entry.get()
            password = password_entry.get()
            if username in self.users:
                messagebox.showerror("Error", "Username already exists.")
            elif not username or not password:
                messagebox.showerror("Error", "Fields cannot be empty.")
            else:
                self.users[username] = {"password": password, "balance": 0.0}
                save_user_data(self.users)
                messagebox.showinfo("Success", "Account created successfully!")
                self.main_menu()

        tk.Button(self.root, text="Create Account", command=create_account).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=5)

    def login_window(self):
        self.clear_window()

        tk.Label(self.root, text="Log In", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Username").pack()
        username_entry = tk.Entry(self.root)
        username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        password_entry = tk.Entry(self.root, show="*")
        password_entry.pack()

        def login():
            username = username_entry.get()
            password = password_entry.get()
            if username not in self.users:
                messagebox.showerror("Error", "Username not found.")
            elif self.users[username]["password"] != password:
                messagebox.showerror("Error", "Incorrect password.")
            else:
                self.current_user = username
                balance = self.users[username]["balance"]
                messagebox.showinfo("Success", f"Login successful! Your current balance is: ${balance:.2f}")
                self.account_menu()

        tk.Button(self.root, text="Log In", command=login).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_menu).pack(pady=5)

    def account_menu(self):
        self.clear_window()

        tk.Label(self.root, text=f"Welcome, {self.current_user}", font=("Arial", 16)).pack(pady=10)

        tk.Button(self.root, text="Check Balance", command=self.check_balance).pack(pady=5)
        tk.Button(self.root, text="Add Money", command=self.add_money_window).pack(pady=5)
        tk.Button(self.root, text="Withdraw Money", command=self.withdraw_money_window).pack(pady=5)
        tk.Button(self.root, text="Log Out", command=self.logout).pack(pady=10)

    def check_balance(self):
        balance = self.users[self.current_user]["balance"]
        messagebox.showinfo("Balance", f"Your balance is: ${balance:.2f}")

    def add_money_window(self):
        self.clear_window()

        tk.Label(self.root, text="Add Money", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Amount").pack()
        amount_entry = tk.Entry(self.root)
        amount_entry.pack()

        def add_money():
            try:
                amount = float(amount_entry.get())
                if amount > 0:
                    self.users[self.current_user]["balance"] += amount
                    save_user_data(self.users)
                    messagebox.showinfo("Success", f"Added ${amount:.2f} to your account.")
                    self.account_menu()
                else:
                    messagebox.showerror("Error", "Enter a positive amount.")
            except ValueError:
                messagebox.showerror("Error", "Invalid amount.")

        tk.Button(self.root, text="Add", command=add_money).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.account_menu).pack(pady=5)

    def withdraw_money_window(self):
        self.clear_window()

        tk.Label(self.root, text="Withdraw Money", font=("Arial", 16)).pack(pady=10)

        tk.Label(self.root, text="Amount").pack()
        amount_entry = tk.Entry(self.root)
        amount_entry.pack()

        def withdraw_money():
            try:
                amount = float(amount_entry.get())
                if 0 < amount <= self.users[self.current_user]["balance"]:
                    self.users[self.current_user]["balance"] -= amount
                    save_user_data(self.users)
                    messagebox.showinfo("Success", f"Withdrew ${amount:.2f} from your account.")
                    self.account_menu()
                else:
                    messagebox.showerror("Error", "Invalid amount or insufficient funds.")
            except ValueError:
                messagebox.showerror("Error", "Invalid amount.")

        tk.Button(self.root, text="Withdraw", command=withdraw_money).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.account_menu).pack(pady=5)

    def logout(self):
        self.current_user = None
        self.main_menu()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = BankApp(root)
    root.mainloop()
