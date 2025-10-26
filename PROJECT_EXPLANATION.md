# Digital Classroom Application

This application is a desktop-based "Digital Classroom" management system built using Python and the `tkinter` library for its graphical user interface (GUI). It allows for user authentication (Admin, Teacher, Student), user management, and assignment management.

## Project Structure

- `main.py`: The entry point of the application. Initializes the main window, handles database setup, and manages switching between login and dashboard views.
- `views/`:
  - `login.py`: Contains the `LoginWindow` class, responsible for user authentication. It hashes passwords using `hashlib.sha256` before verifying credentials against the database.
  - `admin/dashboard.py`: Implements the `AdminDashboard` for administrators, allowing them to manage users and assignments. It includes functionalities like adding, editing, and deleting users, ensuring passwords are hashed before storage or update.
  - `teacher/dashboard.py`: (To be implemented/expanded) Dashboard for teachers to manage their classes and assignments.
  - `student/dashboard.py`: (To be implemented/expanded) Dashboard for students to view assignments and submit work.
- `utils/`:
  - `database.py`: Provides utility functions for all database interactions. This includes `connect_db` (to establish a connection), `create_tables` (to set up necessary tables), `add_user`, `get_users`, `update_user`, `delete_user` (for user management), and similar functions for assignment management. Passwords are hashed in `add_user` and `update_user` before being stored.
- `digital_classroom.db`: The SQLite database file where all application data (users, assignments) is stored.

## Key Functions and Their Purposes

### `main.py`
- `__init__(self, master)`: Initializes the main application window and sets up the database connection.
- `switch_to_dashboard(self, user_type)`: Dynamically loads and displays the appropriate dashboard (Admin, Teacher, or Student) based on the logged-in user's type.

### `views/login.py`
- `login(self)`: Authenticates the user by hashing the entered password and querying the database. If successful, it switches to the appropriate dashboard.

### `views/admin/dashboard.py`
- `_save_new_user(self)`: Handles the creation of a new user, hashing the password before storing it in the database.
- `_save_edited_user(self)`: Updates an existing user's information, ensuring the password is hashed if it's being updated.
- `_delete_user(self)`: Deletes a selected user from the database.
- `_logout(self)`: Logs out the current user and returns to the login screen.

### `utils/database.py`
- `connect_db()`: Establishes a connection to the `digital_classroom.db` SQLite database.
- `create_tables()`: Creates the `users` and `assignments` tables if they do not already exist.
- `add_user(username, password, user_type)`: Inserts a new user into the database, hashing the password before storage.
- `update_user(user_id, username, password, user_type)`: Updates an existing user's details, hashing the password if it's provided.
- `get_users()`: Retrieves all user records from the database.
- `get_user_by_credentials(username, hashed_password)`: Fetches a user record based on username and a hashed password, used for login verification.