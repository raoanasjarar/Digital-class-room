import tkinter as tk
from tkinter import ttk
from views.login import LoginWindow
from utils.database import connect_db, create_user_table, create_assignment_table

class DigitalClassroom(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Digital Classroom")
        self.geometry("1024x768")
        
        # Initialize database
        self.db_conn = connect_db('digital_classroom.db')
        create_user_table(self.db_conn)
        create_assignment_table(self.db_conn)
        
        # Start with login window
        self.login_window = LoginWindow(self)

        # Apply ttk styles
        self.style = ttk.Style()
        self.style.theme_use('clam') # You can experiment with 'clam', 'alt', 'default', 'classic'
        self.style.configure('TButton', font=('Arial', 12), padding=10)
        self.style.map('TButton', background=[('active', '#cce7ff')]) # Light blue on hover
        
    def switch_to_dashboard(self, user_type, username):
        self.login_window.destroy()

        if user_type == "admin":
            from views.admin.dashboard import AdminDashboard
            AdminDashboard(self, username)
        elif user_type == "teacher":
            from views.teacher.dashboard import TeacherDashboard
            TeacherDashboard(self, username)
        elif user_type == "student":
            from views.student.dashboard import StudentDashboard
            StudentDashboard(self, username)

if __name__ == "__main__":
    app = DigitalClassroom()
    app.mainloop()