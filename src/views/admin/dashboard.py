import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import hashlib
from utils.database import connect_db, get_users, add_user, get_assignments

class AdminDashboard(ttk.Frame):
    def __init__(self, parent, username):
        super().__init__(parent)
        self.parent = parent
        self.username = username
        self.pack(expand=True, fill="both")
        self.setup_ui()

    def setup_ui(self):
        # Title
        title_label = ttk.Label(self, text=f"Welcome, Admin {self.username}", font=("Arial", 18, "bold"))
        title_label.pack(pady=20)

        # Buttons
        manage_users_button = ttk.Button(self, text="Manage Users", command=self.manage_users)
        manage_users_button.pack(pady=10)

        manage_courses_button = ttk.Button(self, text="Manage Courses", command=self.oversee_assignments)
        manage_courses_button.pack(pady=10)

        generate_reports_button = ttk.Button(self, text="View Reports", command=self.generate_reports)
        generate_reports_button.pack(pady=10)

        logout_button = ttk.Button(self, text="Logout", command=self.logout)
        logout_button.pack(pady=10)

    def logout(self):
        self.destroy()
        from views.login import LoginWindow
        LoginWindow(self.parent)

    def manage_users(self):
        print("Manage Users button clicked!")
        manage_users_window = tk.Toplevel(self.parent)
        manage_users_window.title("Manage Users")
        manage_users_window.geometry("800x600")

        # Frame for user list
        list_frame = ttk.LabelFrame(manage_users_window, text="User List")
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.users_tree = ttk.Treeview(list_frame, columns=("ID", "Username", "User Type"), show="headings")
        self.users_tree.heading("ID", text="ID")
        self.users_tree.column("ID", width=0, stretch=tk.NO)
        self.users_tree.heading("Username", text="Username")
        self.users_tree.heading("User Type", text="User Type")
        self.users_tree.pack(fill="both", expand=True)

        self.load_users()

        # Frame for buttons
        button_frame = ttk.Frame(manage_users_window)
        button_frame.pack(fill="x", padx=10, pady=5)

        add_user_button = ttk.Button(button_frame, text="Add User", command=self.add_user)
        add_user_button.pack(side="left", padx=5)

        edit_user_button = ttk.Button(button_frame, text="Edit User", command=self.edit_user)
        edit_user_button.pack(side="left", padx=5)

        delete_user_button = ttk.Button(button_frame, text="Delete User", command=self.delete_user)
        delete_user_button.pack(side="left", padx=5)

    def load_users(self):
        for i in self.users_tree.get_children():
            self.users_tree.delete(i)
        conn = connect_db('digital_classroom.db')
        users = get_users(conn)
        conn.close()
        for user in users:
            self.users_tree.insert("", "end", values=(user[0], user[1], user[3]))

    def add_user(self):
        add_user_window = tk.Toplevel(self.parent)
        add_user_window.title("Add New User")
        add_user_window.geometry("400x300")

        form_frame = ttk.Frame(add_user_window, padding="20")
        form_frame.pack(expand=True, fill="both")

        username_label = ttk.Label(form_frame, text="Username:")
        username_label.grid(row=0, column=0, pady=5, padx=5, sticky="w")
        self.new_username_entry = ttk.Entry(form_frame)
        self.new_username_entry.grid(row=0, column=1, pady=5, padx=5, sticky="ew")

        password_label = ttk.Label(form_frame, text="Password:")
        password_label.grid(row=1, column=0, pady=5, padx=5, sticky="w")
        self.new_password_entry = ttk.Entry(form_frame, show="*")
        self.new_password_entry.grid(row=1, column=1, pady=5, padx=5, sticky="ew")

        user_type_label = ttk.Label(form_frame, text="User Type:")
        user_type_label.grid(row=2, column=0, pady=5, padx=5, sticky="w")
        self.new_user_type_combobox = ttk.Combobox(form_frame, values=["admin", "teacher", "student"])
        self.new_user_type_combobox.grid(row=2, column=1, pady=5, padx=5, sticky="ew")
        self.new_user_type_combobox.set("student") # Default value

        save_button = ttk.Button(form_frame, text="Save User", command=lambda: self._save_new_user(add_user_window))
        save_button.grid(row=3, column=0, columnspan=2, pady=10)

        form_frame.grid_columnconfigure(1, weight=1)

    def _save_new_user(self, add_user_window):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()
        user_type = self.new_user_type_combobox.get()

        print(f"Attempting to save new user: Username={username}, UserType={user_type}")

        if not username or not password or not user_type:
            messagebox.showerror("Error", "All fields are required.")
            print("Error: All fields are required.")
            return

        conn = connect_db('digital_classroom.db')
        try:
            print("Calling add_user function...")
            add_user(conn, username, password, user_type)
            print("add_user function called successfully.")
            messagebox.showinfo("Success", "User added successfully.")
            self.load_users() # Refresh the user list
            add_user_window.destroy()
            print("add_user_window destroyed.")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists.")
            print(f"Error: Username '{username}' already exists.")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")
            print(f"An unexpected error occurred: {e}")
        finally:
            conn.close()
            print("Database connection closed.")


    def edit_user(self):
        selected_item = self.users_tree.focus()
        if not selected_item:
            messagebox.showwarning("Edit User", "Please select a user to edit.")
            return

        user_id = self.users_tree.item(selected_item, "values")[0]
        # Fetch user details from the database based on user_id
        conn = connect_db('digital_classroom.db')
        cursor = conn.cursor()
        cursor.execute('SELECT id, username, password, user_type FROM users WHERE id = ?', (user_id,))
        user_data = cursor.fetchone()
        conn.close()

        if not user_data:
            messagebox.showerror("Edit User", "User not found.")
            return

        user_id, username, password, user_type = user_data

        edit_user_window = tk.Toplevel(self.parent)
        edit_user_window.title("Edit User")
        edit_user_window.geometry("400x300")

        form_frame = ttk.Frame(edit_user_window, padding="20")
        form_frame.pack(expand=True, fill="both")

        username_label = ttk.Label(form_frame, text="Username:")
        username_label.grid(row=0, column=0, pady=5, padx=5, sticky="w")
        username_entry = ttk.Entry(form_frame)
        username_entry.insert(0, username)
        username_entry.grid(row=0, column=1, pady=5, padx=5, sticky="ew")

        password_label = ttk.Label(form_frame, text="Password:")
        password_label.grid(row=1, column=0, pady=5, padx=5, sticky="w")
        password_entry = ttk.Entry(form_frame, show="*")
        password_entry.insert(0, password)
        password_entry.grid(row=1, column=1, pady=5, padx=5, sticky="ew")

        user_type_label = ttk.Label(form_frame, text="User Type:")
        user_type_label.grid(row=2, column=0, pady=5, padx=5, sticky="w")
        user_type_var = tk.StringVar(form_frame)
        user_type_var.set(user_type)  # Set initial value
        user_type_combobox = ttk.Combobox(form_frame, textvariable=user_type_var, values=["admin", "teacher", "student"])
        user_type_combobox.grid(row=2, column=1, pady=5, padx=5, sticky="ew")

        save_button = ttk.Button(form_frame, text="Save Changes", command=lambda: self._save_edited_user(user_id, username_entry.get(), password_entry.get(), user_type_var.get(), edit_user_window))
        save_button.grid(row=3, column=0, columnspan=2, pady=10)

        form_frame.grid_columnconfigure(1, weight=1)

    def _save_edited_user(self, user_id, username, password, user_type, window):
        if not username or not password or not user_type:
            messagebox.showerror("Error", "All fields are required.")
            return

        conn = connect_db('digital_classroom.db')
        try:
            # Hash the password before updating
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            update_user(conn, user_id, username, hashed_password, user_type)
            messagebox.showinfo("Success", "User updated successfully.")
            self.load_users()
            window.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to update user: {e}")
        finally:
            conn.close()

    def delete_user(self):
        selected_item = self.users_tree.focus()
        if not selected_item:
            messagebox.showwarning("Delete User", "Please select a user to delete.")
            return

        user_id = self.users_tree.item(selected_item, "values")[0]
        username = self.users_tree.item(selected_item, "values")[1]

        if messagebox.askyesno("Delete User", f"Are you sure you want to delete user {username}?"):
            conn = connect_db('digital_classroom.db')
            try:
                cursor = conn.cursor()
                cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
                conn.commit()
                messagebox.showinfo("Success", "User deleted successfully.")
                self.load_users()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Failed to delete user: {e}")
            finally:
                conn.close()

    def oversee_assignments(self):
        oversee_assignments_window = tk.Toplevel(self.parent)
        oversee_assignments_window.title("Oversee Assignments")
        oversee_assignments_window.geometry("800x600")

        # Frame for assignment list
        list_frame = ttk.LabelFrame(oversee_assignments_window, text="Assignment List")
        list_frame.pack(fill="both", expand=True, padx=10, pady=10)

        self.assignments_tree = ttk.Treeview(list_frame, columns=("Title", "Description", "Due Date", "Status"), show="headings")
        self.assignments_tree.heading("Title", text="Title")
        self.assignments_tree.heading("Description", text="Description")
        self.assignments_tree.heading("Due Date", text="Due Date")
        self.assignments_tree.heading("Status", text="Status")
        self.assignments_tree.pack(fill="both", expand=True)

        self.load_assignments()

        # Frame for buttons
        button_frame = ttk.Frame(oversee_assignments_window)
        button_frame.pack(fill="x", padx=10, pady=5)

        add_assignment_button = ttk.Button(button_frame, text="Add Assignment", command=self.add_assignment)
        add_assignment_button.pack(side="left", padx=5)

        edit_assignment_button = ttk.Button(button_frame, text="Edit Assignment", command=self.edit_assignment)
        edit_assignment_button.pack(side="left", padx=5)

        delete_assignment_button = ttk.Button(button_frame, text="Delete Assignment", command=self.delete_assignment)
        delete_assignment_button.pack(side="left", padx=5)

    def load_assignments(self):
        for i in self.assignments_tree.get_children():
            self.assignments_tree.delete(i)
        conn = connect_db('digital_classroom.db')
        assignments = get_assignments(conn)
        conn.close()
        for assignment in assignments:
            self.assignments_tree.insert("", "end", values=(assignment[1], assignment[2], assignment[3], assignment[4]))

    def add_assignment(self):
        add_assignment_window = tk.Toplevel(self.parent)
        add_assignment_window.title("Add New Assignment")
        add_assignment_window.geometry("400x400")

        form_frame = ttk.Frame(add_assignment_window, padding="20")
        form_frame.pack(expand=True, fill="both")

        title_label = ttk.Label(form_frame, text="Title:")
        title_label.grid(row=0, column=0, pady=5, padx=5, sticky="w")
        self.new_assignment_title_entry = ttk.Entry(form_frame)
        self.new_assignment_title_entry.grid(row=0, column=1, pady=5, padx=5, sticky="ew")

        description_label = ttk.Label(form_frame, text="Description:")
        description_label.grid(row=1, column=0, pady=5, padx=5, sticky="w")
        self.new_assignment_description_entry = ttk.Entry(form_frame)
        self.new_assignment_description_entry.grid(row=1, column=1, pady=5, padx=5, sticky="ew")

        due_date_label = ttk.Label(form_frame, text="Due Date (YYYY-MM-DD):")
        due_date_label.grid(row=2, column=0, pady=5, padx=5, sticky="w")
        self.new_assignment_due_date_entry = ttk.Entry(form_frame)
        self.new_assignment_due_date_entry.grid(row=2, column=1, pady=5, padx=5, sticky="ew")

        status_label = ttk.Label(form_frame, text="Status:")
        status_label.grid(row=3, column=0, pady=5, padx=5, sticky="w")
        self.new_assignment_status_combobox = ttk.Combobox(form_frame, values=["pending", "in_progress", "completed"])
        self.new_assignment_status_combobox.grid(row=3, column=1, pady=5, padx=5, sticky="ew")
        self.new_assignment_status_combobox.set("pending") # Default value

        save_button = ttk.Button(form_frame, text="Save Assignment", command=lambda: self._save_new_assignment(add_assignment_window))
        save_button.grid(row=4, column=0, columnspan=2, pady=10)

        form_frame.grid_columnconfigure(1, weight=1)

    def _save_new_assignment(self, window):
        title = self.new_assignment_title_entry.get()
        description = self.new_assignment_description_entry.get()
        due_date = self.new_assignment_due_date_entry.get()
        status = self.new_assignment_status_combobox.get()

        if not title or not description or not due_date or not status:
            messagebox.showerror("Error", "All fields are required.")
            return

        conn = connect_db('digital_classroom.db')
        try:
            add_assignment(conn, title, description, due_date, status)
            messagebox.showinfo("Success", "Assignment added successfully.")
            self.load_assignments() # Refresh the assignment list
            window.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to add assignment: {e}")
        finally:
            conn.close()

    def edit_assignment(self):
        selected_item = self.assignments_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select an assignment to edit.")
            return

        assignment_id = self.assignments_tree.item(selected_item)['values'][0]
        conn = connect_db('digital_classroom.db')
        assignment = get_assignment_by_id(conn, assignment_id)
        conn.close()

        if not assignment:
            messagebox.showerror("Error", "Assignment not found.")
            return

        edit_assignment_window = tk.Toplevel(self.parent)
        edit_assignment_window.title("Edit Assignment")
        edit_assignment_window.geometry("400x400")

        form_frame = ttk.Frame(edit_assignment_window, padding="20")
        form_frame.pack(expand=True, fill="both")

        title_label = ttk.Label(form_frame, text="Title:")
        title_label.grid(row=0, column=0, pady=5, padx=5, sticky="w")
        self.edit_assignment_title_entry = ttk.Entry(form_frame)
        self.edit_assignment_title_entry.grid(row=0, column=1, pady=5, padx=5, sticky="ew")
        self.edit_assignment_title_entry.insert(0, assignment[1])

        description_label = ttk.Label(form_frame, text="Description:")
        description_label.grid(row=1, column=0, pady=5, padx=5, sticky="w")
        self.edit_assignment_description_entry = ttk.Entry(form_frame)
        self.edit_assignment_description_entry.grid(row=1, column=1, pady=5, padx=5, sticky="ew")
        self.edit_assignment_description_entry.insert(0, assignment[2])

        due_date_label = ttk.Label(form_frame, text="Due Date (YYYY-MM-DD):")
        due_date_label.grid(row=2, column=0, pady=5, padx=5, sticky="w")
        self.edit_assignment_due_date_entry = ttk.Entry(form_frame)
        self.edit_assignment_due_date_entry.grid(row=2, column=1, pady=5, padx=5, sticky="ew")
        self.edit_assignment_due_date_entry.insert(0, assignment[3])

        status_label = ttk.Label(form_frame, text="Status:")
        status_label.grid(row=3, column=0, pady=5, padx=5, sticky="w")
        self.edit_assignment_status_combobox = ttk.Combobox(form_frame, values=["pending", "in_progress", "completed"])
        self.edit_assignment_status_combobox.grid(row=3, column=1, pady=5, padx=5, sticky="ew")
        self.edit_assignment_status_combobox.set(assignment[4])

        save_button = ttk.Button(form_frame, text="Save Changes", command=lambda: self._save_edited_assignment(assignment_id, edit_assignment_window))
        save_button.grid(row=4, column=0, columnspan=2, pady=10)

        form_frame.grid_columnconfigure(1, weight=1)

    def _save_edited_assignment(self, assignment_id, window):
        title = self.edit_assignment_title_entry.get()
        description = self.edit_assignment_description_entry.get()
        due_date = self.edit_assignment_due_date_entry.get()
        status = self.edit_assignment_status_combobox.get()

        if not title or not description or not due_date or not status:
            messagebox.showerror("Error", "All fields are required.")
            return

        conn = connect_db('digital_classroom.db')
        try:
            update_assignment(conn, assignment_id, title, description, due_date, status)
            messagebox.showinfo("Success", "Assignment updated successfully.")
            self.load_assignments()
            window.destroy()
        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"Failed to update assignment: {e}")
        finally:
            conn.close()

    def delete_assignment(self):
        selected_item = self.assignments_tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select an assignment to delete.")
            return

        assignment_id = self.assignments_tree.item(selected_item)['values'][0]

        if messagebox.askyesno("Delete Assignment", "Are you sure you want to delete this assignment?"):
            conn = connect_db('digital_classroom.db')
            try:
                delete_assignment(conn, assignment_id)
                messagebox.showinfo("Success", "Assignment deleted successfully.")
                self.load_assignments()
            except sqlite3.Error as e:
                messagebox.showerror("Database Error", f"Failed to delete assignment: {e}")
            finally:
                conn.close()

    def generate_reports(self):
        print("Generate Reports button clicked")
        # Code to generate reports on user activity and assignments
        pass