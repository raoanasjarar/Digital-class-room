import hashlib
import tkinter as tk
from tkinter import ttk, messagebox
from utils.database import connect_db

class LoginWindow(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()
        
    def setup_ui(self):
        self.pack(expand=True, fill="both")

        login_frame = ttk.Frame(self, padding="20")
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        title_label = ttk.Label(login_frame, text="Digital Classroom Login", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        self.username_label = ttk.Label(login_frame, text="Username:")
        self.username_entry = ttk.Entry(login_frame)
        
        self.password_label = ttk.Label(login_frame, text="Password:")
        self.password_entry = ttk.Entry(login_frame, show="*")
        
        self.login_button = ttk.Button(login_frame, text="Login", command=self.login)
        
        # Grid layout
        self.username_label.grid(row=1, column=0, pady=5, padx=5, sticky="w")
        self.username_entry.grid(row=1, column=1, pady=5, padx=5, sticky="ew")
        self.password_label.grid(row=2, column=0, pady=5, padx=5, sticky="w")
        self.password_entry.grid(row=2, column=1, pady=5, padx=5, sticky="ew")
        self.login_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        login_frame.grid_columnconfigure(1, weight=1)
        
    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        print(f"Attempting login for username: {username}")
        print(f"Raw password entered: {password}")
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        print(f"Hashed password for comparison: {hashed_password}")
        
        # Connect to database and verify credentials
        conn = connect_db('digital_classroom.db')
        cursor = conn.cursor()
        cursor.execute('SELECT user_type FROM users WHERE username=? AND password=?',
                      (username, hashed_password))
        result = cursor.fetchone()
        print(f"Database query result: {result}")
        
        if result:
            self.destroy()
            self.parent.switch_to_dashboard(result[0], username)
        else:
            messagebox.showerror("Error", "Invalid credentials")