import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from utils.database import connect_db

class TeacherDashboard(ttk.Frame):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.setup_ui()
        
    def setup_ui(self):
        # Create notebook for different sections
        self.notebook = ttk.Notebook(self)
        
        # Assignments tab
        self.assignments_frame = ttk.Frame(self.notebook)
        self.setup_assignments_tab()
        
        # Students tab
        self.students_frame = ttk.Frame(self.notebook)
        self.setup_students_tab()
        
        self.notebook.add(self.assignments_frame, text="Assignments")
        self.notebook.add(self.students_frame, text="Students")
        
        self.notebook.pack(expand=True, fill="both")
        self.pack(expand=True, fill="both")
        
    def setup_assignments_tab(self):
        create_frame = ttk.LabelFrame(self.assignments_frame, text="Create New Assignment")
        ttk.Label(create_frame, text="Title:").grid(row=0, column=0, pady=5, sticky="w")
        self.title_entry = ttk.Entry(create_frame)
        self.title_entry.grid(row=0, column=1, pady=5, sticky="ew")

        ttk.Label(create_frame, text="Description:").grid(row=1, column=0, pady=5, sticky="w")
        self.description_entry = ttk.Entry(create_frame)
        self.description_entry.grid(row=1, column=1, pady=5, sticky="ew")
        
        ttk.Label(create_frame, text="Due Date:").grid(row=2, column=0, pady=5, sticky="w")
        self.due_date = DateEntry(create_frame)
        self.due_date.grid(row=2, column=1, pady=5, sticky="ew")
        
        ttk.Button(create_frame, text="Create", 
                  command=self.create_assignment).grid(row=3, column=0, columnspan=2, pady=10)
        
        create_frame.pack(fill="x", padx=5, pady=5)
        create_frame.grid_columnconfigure(1, weight=1)
        
        # Assignments list
        list_frame = ttk.LabelFrame(self.assignments_frame, text="Assignments")
        self.assignments_tree = ttk.Treeview(list_frame, 
                                           columns=("Title", "Description", "Due Date", "Status"), show="headings")
        self.assignments_tree.heading("Title", text="Title")
        self.assignments_tree.heading("Description", text="Description")
        self.assignments_tree.heading("Due Date", text="Due Date")
        self.assignments_tree.heading("Status", text="Status")
        self.assignments_tree.pack(fill="both", expand=True)
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)
        self.load_assignments()
        
    def setup_students_tab(self):
        # Student list
        self.students_tree = ttk.Treeview(self.students_frame, 
                                        columns=("Name", "Email"))
        self.students_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
    def create_assignment(self):
        title = self.title_entry.get()
        description = self.description_entry.get()
        due_date = self.due_date.get()

        if title and description and due_date:
            conn = connect_db('digital_classroom.db')
            add_assignment(conn, title, description, due_date, "Pending")
            conn.close()
            self.title_entry.delete(0, tk.END)
            self.description_entry.delete(0, tk.END)
            self.load_assignments()
            messagebox.showinfo("Success", "Assignment created successfully!")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def load_assignments(self):
        for i in self.assignments_tree.get_children():
            self.assignments_tree.delete(i)
        conn = connect_db('digital_classroom.db')
        assignments = get_assignments(conn)
        conn.close()
        for assignment in assignments:
            self.assignments_tree.insert("", "end", values=(assignment[1], assignment[2], assignment[3], assignment[4]))