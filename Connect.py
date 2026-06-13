import sqlite3
# Note: You should be using a proper password hashing library like 'bcrypt'
# for production applications. This implementation is for demonstration only!

# --- Database Connection and Setup ---

def make_connection():
    """
    Establishes and returns a connection to the 'Layout.db' file.
    Creates the file if it doesn't exist.
    Uses check_same_thread=False for Streamlit's multi-threading environment.
    """
    # NOTE: 'Layout.db' must be in the same directory as this script.
    conn = sqlite3.connect('Layout.db', check_same_thread=False)
    return conn

# Establish connection and cursor globally
conn = make_connection()
cursor = conn.cursor()

def create_table():
    """
    Creates the 'Layout' table with Name, Email, and Password columns.
    """
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Layout (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Email TEXT NOT NULL UNIQUE,
                Password TEXT NOT NULL
            )
        """)
        conn.commit()
        # print("Layout table checked/created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")

# Run the table creation/check once
create_table()

# -------------------------------------


# --- Corrected Application Logic Functions ---

def registration(username: str, email: str, password: str) -> bool:
    """
    Registers a new user into the Layout table.
    NOTE: The password is NOT HASHED for simplicity, which is a major SECURITY RISK.
    """
    # Fix 1: Takes three individual arguments as expected by the Streamlit app.
    sql = "INSERT INTO Layout (Name, Email, Password) VALUES (?, ?, ?)"
    try:
        data = (username, email, password) # Create the data tuple here
        cursor.execute(sql, data)
        conn.commit()
        # print("Registration successful.")
        return True
    except sqlite3.IntegrityError:
        # print("Error: Email already exists.")
        return False
    except Exception as e:
        print(f"Registration failed: {e}")
        return False


def login(username: str, password: str) -> tuple or None:
    """
    Logs in a user by checking for a matching Name (used as username) and Password.
    Returns the user data (tuple) on success, or None on failure.
    NOTE: Plaintext password comparison used (SECURITY RISK).
    """
    # Fix 2: Changed query to use Name (username) instead of Email, 
    # as the Streamlit app passes username.
    sql = "SELECT Name, Email FROM Layout WHERE Name=? AND Password=?"
    try:
        data = (username, password) # Create the data tuple here
        cursor.execute(sql, data)
        # fetchone() returns (Name, Email) on match, or None
        user = cursor.fetchone() 
        if user:
            # print("Login successful.")
            # Returns user data (Name, Email)
            return user 
        else:
            # print("Login failed: Invalid username or password.")
            return None
    except Exception as e:
        print(f"Login error: {e}")
        return None

def view() -> list:
    """
    Fetches all users (Name and Email) from the Layout table.
    """
    sql = "SELECT Name, Email FROM Layout ORDER BY Name"
    try:
        cursor.execute(sql)
        # fetchall() returns a list of tuples: [(name1, email1), (name2, email2), ...]
        return cursor.fetchall()
    except Exception as e:
        print(f"View error: {e}")
        return []

def delete_user(username: str) -> bool:
    """
    Deletes a user based on their Name (username).
    """
    sql = "DELETE FROM Layout WHERE Name=?"
    try:
        cursor.execute(sql, (username,))
        rows_deleted = cursor.rowcount
        conn.commit()
        if rows_deleted > 0:
            # print(f"User '{username}' deleted successfully.")
            return True
        else:
            # print(f"Delete failed: User '{username}' not found.")
            return False
    except Exception as e:
        print(f"Delete error: {e}")
        return False