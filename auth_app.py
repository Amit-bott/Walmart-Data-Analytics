import streamlit as st
import Connect # Your database connector file
import requests
from streamlit_lottie import st_lottie 
import time

#  IMPORT YOUR PROJECT LOGIC HERE
from project_module import project_dashboard # Note: Renamed main_app to project_dashboard in file 1

# --- Utility Functions ---

def load_lottieurl(url: str):
    """Fetches Lottie JSON data from a URL."""
    try:
        # Added a timeout for safety
        r = requests.get(url, timeout=5) 
        if r.status_code == 200:
            return r.json()
    except requests.exceptions.RequestException as e:
        # st.error(f"Error loading Lottie animation: {e}") # Suppress error for cleaner UI
        pass # Return None silently if it fails
    return None

# -------------------------------------------------------------------------------------

#  THE NEW/MODIFIED FUNCTION TO DISPLAY THE PROJECT
def display_protected_project_page():
    """
    Displays the user dashboard in the sidebar and the main project content.
    """
    
    # --- SIDEBAR CONTENT (Authentication UI) ---
    st.sidebar.header("User Dashboard")
    st.sidebar.success(f"Access granted to: {st.session_state.username}")
    
    # Logout button moved to sidebar
    if st.sidebar.button("Logout", help="Click to log out of the application"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.info("Logged out successfully.")
        st.rerun() # Rerun to go back to the login page

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Project Filters & Controls**")
    
    # --- MAIN CONTENT ---
    #  CALL YOUR PROJECT DASHBOARD FUNCTION HERE!
    project_dashboard() 

# -------------------------------------------------------------------------------------

def display_login_or_register():
    """
    Displays the login and registration forms in a tabbed interface.
    """
    # Lottie animation URLs
    LOTTIE_URL_LOCK = "https://lottie.host/3ccff03a-36c7-4b15-81bf-54ee3362e18f/NfxIBmRe5o.json"
    LOTTIE_URL_REGISTER = "https://lottie.host/0715fade-5bd0-44af-881f-f61d67d55c73/J5rgz04sDq.json"
    
    lottie_lock = load_lottieurl(LOTTIE_URL_LOCK)
    lottie_register = load_lottieurl(LOTTIE_URL_REGISTER)

    # Displays the login and registration forms in a tabbed interface.
    login_tab, register_tab = st.tabs(["Login", "Register"])

    # --- Login Tab Content ---
    with login_tab:
        st.header("Login")
        col1_login, col2_login = st.columns([1, 2])
        
        with col1_login:
            if lottie_lock:
                st_lottie(lottie_lock, speed=1, loop=True, quality="high", height=400, width=400, key="lock_animation")
            else:
                st.info("Lottie animation space (could not load remote content).")

        # Place the Login Form in the second column of this tab
        with col2_login:
            with st.form("login_form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                login_button = st.form_submit_button("Log In")

                if login_button:
                    if username and password:
                        # Call the login function from the Connect module
                        user_data = Connect.login(username, password)
                        if user_data:
                            st.session_state.logged_in = True
                            st.session_state.username = user_data[0]
                            st.success("Logged in successfully! Redirecting...")
                            st.rerun() # Rerun to switch to the project page
                        else:
                            st.error("Invalid username or password.")
                    else:
                        st.error("Please enter both username and password.")

    # --- Registration Tab Content ---
    with register_tab:
        st.header("Register")

        col1_register, col2_register = st.columns([1, 2])
        
        with col1_register:
            if lottie_register:
                st_lottie(lottie_register, speed=1, loop=True, quality="high", height=400, width=400, key="register_animation")
            else:
                st.info("Lottie animation space (could not load remote content).")
                
        # Place the Registration Form in the second column of this tab
        with col2_register:
            with st.form("register_form"):
                new_username = st.text_input("New Username")
                new_email = st.text_input("Email")
                new_password = st.text_input("New Password", type="password")
                register_button = st.form_submit_button("Register")

                if register_button:
                    if new_username and new_email and new_password:
                        # Call the registration function from the Connect module
                        if Connect.registration(new_username, new_email, new_password):
                            st.success("Registration successful! You can now log in.")
                        else:
                            st.error("Registration failed. Username or email may already exist.")
                    else:
                        st.error("Please fill in all fields.")

# -------------------------------------------------------------------------------------

def main():
    """
    Main function for the Streamlit application, handling authentication flow.
    """
    # Initialize the authentication database on startup (Uncomment if needed)
    # Connect.make_connection()
    
    # === SET PAGE CONFIG ===
    st.set_page_config(
        page_title="Secure Walmart Sales Dashboard", 
        page_icon="🔐", 
        initial_sidebar_state='auto', 
        layout='wide'
    )
    # =======================

    # --- CSS Styles ---
    st.markdown(
        """
        <style>
        .stButton>button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border-radius: 8px;
            border: none;
            padding: 10px 24px;
            cursor: pointer;
        }
        .stButton>button:hover {
            background-color: #45a049;
        }
        div.stApp {
            font-size: 1.15rem; 
        }
        .stApp p {
            font-size: 1.25rem !important;
            line-height: 1.6;
        }
        .stDataFrame {
            font-size: 1rem; 
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # Initialize session state for user authentication
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None

    # Handle the main app flow
    #  THIS IS THE LINKAGE: If logged in, show project; otherwise, show login
    if st.session_state.logged_in:
        display_protected_project_page() 
    else:
        st.title("User Authentication App")
        st.caption("Please log in to access the Walmart Sales Dashboard.")
        display_login_or_register()

if __name__ == "__main__":
    main()