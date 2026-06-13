import streamlit as st
import Connect
# These imports are necessary for fetching and displaying Lottie animations.
# Note: In a real Streamlit environment, you would need to 'pip install requests streamlit-lottie'.
import requests
from streamlit_lottie import st_lottie 

def load_lottieurl(url: str):
    """Fetches Lottie JSON data from a URL."""
    try:
        # Added a timeout for safety
        r = requests.get(url, timeout=5) 
        if r.status_code == 200:
            return r.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error loading Lottie animation: {e}")
    return None

def main():
    """
    Main function for the Streamlit authentication application.
    """
    # Initialize the authentication database on startup
    # Connect.make_connection()
    
    # === CHANGE MADE HERE: Added layout='wide' ===
    st.set_page_config(
        page_title="Secure App", 
        page_icon="🔐", 
        initial_sidebar_state='auto', 
        layout='wide'
    )
    # ============================================

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
        
        /* >>> CSS FOR BIGGER TEXT ON WELCOME PAGE <<< */
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
    st.title("User Authentication App")
    st.caption("Using `auth.py` to simulate secure, session-persistent user management.")

    # Initialize session state for user authentication
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
        st.session_state.username = None

    # Handle the main app flow
    if st.session_state.logged_in:
        display_welcome_page()
    else:
        display_login_or_register()

# -------------------------------------------------------------------------------------

def display_login_or_register():
    """
    Displays the correct Lottie animation and the login/registration forms in a tabbed interface.
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
        
        # Define columns ONLY inside the tab so they only render when the tab is active
        # These columns will now use the full 'wide' screen width
        col1_login, col2_login = st.columns([1, 2])
        
        with col1_login:
             if lottie_lock:
                 # Animation size set to 250x250
                st_lottie(
                    lottie_lock,
                    speed=1,
                    reverse=False,
                    loop=True,
                    quality="high", 
                    height=400,
                    width=400,
                    key="lock_animation",
                )
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
                        # Call the login function from the auth module
                        user_data = Connect.login(username, password)
                        if user_data:
                            st.session_state.logged_in = True
                            st.session_state.username = user_data[0]
                            st.success("Logged in successfully!")
                            st.rerun() # Rerun to switch to the welcome page
                        else:
                            st.error("Invalid username or password.")
                    else:
                        st.error("Please enter both username and password.")

    # --- Registration Tab Content ---
    with register_tab:
        st.header("Register")

        # Define columns ONLY inside the tab so they only render when the tab is active
        col1_register, col2_register = st.columns([1, 2])
        
        with col1_register:
             if lottie_register:
                 # Animation size set to 250x230
                st_lottie(
                    lottie_register,
                    speed=1,
                    reverse=False,
                    loop=True,
                    quality="high", 
                    height=400,
                    width=400,
                    key="register_animation", # Unique key for this Lottie instance
                )
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
                        # Call the registration function from the auth module
                        if Connect.registration(new_username, new_email, new_password):
                            st.success("Registration successful! You can now log in.")
                        else:
                            st.error("Registration failed. Username or email may already exist.")
                    else:
                        st.error("Please fill in all fields.")

# -------------------------------------------------------------------------------------

def display_welcome_page():
    """
    Displays the content for authenticated users, utilizing the sidebar and larger text.
    """
    
    # --- SIDEBAR CONTENT ---
    st.sidebar.header("User Dashboard")
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    
    # Logout button moved to sidebar
    if st.sidebar.button("Logout", help="Click to log out of the application"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.success("Logged out successfully.")
        st.rerun() # Rerun to go back to the login page

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Protected Area**")
    # -----------------------
    
    # --- MAIN CONTENT ---
    
    # Using st.title for the main welcome message (large font)
    st.title(f"🎉 Welcome Back, {st.session_state.username}! 🎉") 
    
    # Using st.markdown with increased spacing/size (due to custom CSS)
    st.markdown("### This is the **Protected Content Section** of your app.")
    st.markdown("Feel free to use the administrative tools below.")
    st.markdown("---")
    
    st.header("Admin Area (for Testing)")
    
    # Display all registered users
    st.subheader("Registered Users")
    users = Connect.view()
    if users:
        # The dataframe will automatically expand and use the full 'wide' width
        user_data = [{"Username": user[0], "Email": user[1]} for user in users]
        st.dataframe(user_data, use_container_width=True, hide_index=True)
    else:
        st.warning("No users currently registered in the system.")
        
    # Delete a user
    st.subheader("Delete User")
    with st.form("delete_form"):
        user_to_delete = st.text_input("Enter username to delete", help="This action is permanent.")
        delete_button = st.form_submit_button("Delete User")
        
        if delete_button:
            if user_to_delete:
                # Call the delete function from the auth module
                if Connect.delete_user(user_to_delete):
                    st.success(f"User **'{user_to_delete}'** deleted successfully.")
                    
                    # Log out the user if they delete their own account
                    if user_to_delete == st.session_state.username:
                        st.session_state.logged_in = False 
                        st.session_state.username = None
                    
                    st.rerun() # Rerun to refresh the user list
                else:
                    st.error(f"Failed to delete user **'{user_to_delete}'**. User not found.")
            else:
                st.error("Please enter a username to delete.")
    
    st.markdown("---")


if __name__ == "__main__":
    main()