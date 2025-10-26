import tkinter as tk
from tkinter import ttk
from utils.database import connect_db, get_assignments

class StudentDashboard(ttk.Frame):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.pack(expand=True, fill="both")
        self.setup_ui()

    def setup_ui(self):
        # Title
        title_label = ttk.Label(self, text=f"Welcome, Student {self.username}", font=("Arial", 18, "bold"))
        title_label.pack(pady=20)

        # Assignments list
        list_frame = ttk.LabelFrame(self, text="My Assignments")
        self.assignments_tree = ttk.Treeview(list_frame, 
                                           columns=("Title", "Description", "Due Date", "Status"), show="headings")
        self.assignments_tree.heading("Title", text="Title")
        self.assignments_tree.heading("Description", text="Description")
        self.assignments_tree.heading("Due Date", text="Due Date")
        self.assignments_tree.heading("Status", text="Status")
        self.assignments_tree.pack(fill="both", expand=True)
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.load_assignments()

    def load_assignments(self):
        for i in self.assignments_tree.get_children():
            self.assignments_tree.delete(i)
        conn = connect_db('digital_classroom.db')
        assignments = get_assignments(conn)
        conn.close()
        for assignment in assignments:
            self.assignments_tree.insert("", "end", values=(assignment[1], assignment[2], assignment[3], assignment[4]))