import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
from streamlit_lottie import st_lottie
from datetime import datetime
import time 
import sqlite3 # <-- NEW: Import SQLite library

# --- Database Connection and Setup (Based on user's Connect file) ---

def make_connection():
    """
    Establishes and returns a connection to the 'Layout.db' file.
    Creates the file if it doesn't exist.
    Uses check_same_thread=False for Streamlit's multi-threading environment.
    """
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

# ======================================================================
# 🚨 AUTHENTICATION/DATABASE LAYER (Connect Class) 🚨
# --------------------------------------------------
# This class now uses the SQLite connection established above.
class Connect:
    """Class to interface with the SQLite database for user authentication."""

    # Note: Passwords are not hashed for simplicity, which is a major SECURITY RISK 
    # for production applications.

    @staticmethod
    def login(username, password):
        """Authenticates a user against the SQLite database."""
        sql = "SELECT Name, Email FROM Layout WHERE Name=? AND Password=?"
        try:
            cursor.execute(sql, (username, password))
            # fetchone() returns (Name, Email) on match, or None
            user = cursor.fetchone() 
            if user:
                # Returns (username, user_id). We use Name for both here.
                return (user[0], user[0]) 
            return None
        except Exception as e:
            print(f"Login error: {e}")
            return None

    @staticmethod
    def registration(username, email, password):
        """Registers a new user into the SQLite database."""
        sql = "INSERT INTO Layout (Name, Email, Password) VALUES (?, ?, ?)"
        try:
            cursor.execute(sql, (username, email, password))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # Username/Email already exists
            return False
        except Exception as e:
            print(f"Registration failed: {e}")
            return False

# ======================================================================
# NOTE: The st.set_page_config is now handled in the main() function below.

# --- Helper Functions ---

def load_lottieurl(url: str):
    """Fetches a Lottie animation from a URL, with error handling."""
    try:
        # Added a timeout for safety
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.json()
        return None
    except requests.exceptions.RequestException as e:
        # Log the error but don't crash the app if Lottie fails to load
        # print(f"Lottie load error: {e}")
        return None

# Load the Lottie animation for visual feedback (for data loading)
lottie_loading = load_lottieurl("https://lottie.host/db1d952d-60a0-4bd6-bbb1-11fa885687bc/tlQrUeuvPY.json")

# Define the color map (using integer keys)
store_colors = {
    1: {'colors': ['#FF5733', '#FFC300', '#A133FF', '#33FFFF']},
    2: {'colors': ['#33FF57', '#8A2BE2', '#FF4500', '#2E8B57']},
    3: {'colors': ['#3357FF', '#FF33A1', '#4682B4', '#DAA520']},
    4: {'colors': ['#A133FF', '#33FFF6', '#9ACD32', '#CD853F']},
    5: {'colors': ['#FF8D33', '#61FF33', '#FFA07A', '#F08080']},
    6: {'colors': ['#8DFF33', '#338DFF', '#3CB371', '#D8BFD8']},
    7: {'colors': ['#33FFFF', '#FF338D', '#BDB76B', '#CD5C5C']},
    8: {'colors': ['#FF338D', '#33FF8D', '#FFE4B5', '#BA55D3']},
    9: {'colors': ['#8D33FF', '#33A1FF', '#00BFFF', '#B22222']},
    10: {'colors': ['#FFBD33', '#33FFBD', '#FFDAB9', '#A1FF33']},
    11: {'colors': ['#33FFBD', '#FFBD33', '#FFD700', '#C0C0C0']},
    12: {'colors': ['#BD33FF', '#33BDFF', '#7FFF00', '#D2691E']},
    13: {'colors': ['#FF33BD', '#BDFF33', '#FFF8DC', '#00CED1']},
    14: {'colors': ['#33BDFF', '#FF33BD', '#800000', '#A9A9A9']},
    15: {'colors': ['#BDFF33', '#33FFBD', '#483D8B', '#FF4500']},
    16: {'colors': ['#FF33A1', '#A133FF', '#D2B48C', '#2F4F4F']},
    17: {'colors': ['#A1FF33', '#33A1FF', '#FFE4C4', '#F0FFF0']},
    18: {'colors': ['#A133FF', '#FFA133', '#FAFAD2', '#DDA0DD']},
    19: {'colors': ['#FFD700', '#C0C0C0', '#A0522D', '#556B2F']},
    20: {'colors': ['#FF4500', '#ADFF2F', '#FF69B4', '#BA55D3']},
    21: {'colors': ['#7FFF00', '#D2691E', '#CD5C5C', '#5F9EA0']},
    22: {'colors': ['#BA55D3', '#20B2AA', '#E0FFFF', '#FFD700']},
    23: {'colors': ['#00BFFF', '#B22222', '#F0E68C', '#DAA520']},
    24: {'colors': ['#FFDAB9', '#E6E6FA', '#808000', '#4682B4']},
    25: {'colors': ['#F08080', '#2E8B57', '#CD853F', '#FF1493']},
    26: {'colors': ['#D8BFD8', '#FF6347', '#D2B48C', '#2F4F4F']},
    27: {'colors': ['#3CB371', '#9370DB', '#9ACD32', '#808000']},
    28: {'colors': ['#BDB76B', '#8B0000', '#4682B4', '#B0C4DE']},
    29: {'colors': ['#FFC0CB', '#5F9EA0', '#FFE4B5', '#9400D3']},
    30: {'colors': ['#CD853F', '#FF1493', '#FFE4C4', '#CD5C5C']},
    31: {'colors': ['#E0FFFF', '#FFD700', '#F0E68C', '#DAA520']},
    32: {'colors': ['#FFF8DC', '#00CED1', '#E6E6FA', '#F0FFF0']},
    33: {'colors': ['#800000', '#A9A9A9', '#FAFAD2', '#DDA0DD']},
    34: {'colors': ['#483D8B', '#FF4500', '#A0522D', '#556B2F']},
    35: {'colors': ['#D2B48C', '#2F4F4F', '#FFA07A', '#B22222']},
    36: {'colors': ['#9ACD32', '#808000', '#FF69B4', '#BA55D3']},
    37: {'colors': ['#4682B4', '#B0C4DE', '#A1FF33', '#33A1FF']},
    38: {'colors': ['#FFE4B5', '#9400D3', '#A133FF', '#FFA133']},
    39: {'colors': ['#FFE4C4', '#CD5C5C', '#FFD700', '#C0C0C0']},
    40: {'colors': ['#F0E68C', '#DAA520', '#FF4500', '#ADFF2F']},
    41: {'colors': ['#E6E6FA', '#F0FFF0', '#7FFF00', '#D2691E']},
    42: {'colors': ['#FAFAD2', '#DDA0DD', '#BA55D3', '#20B2AA']},
    43: {'colors': ['#A0522D', '#556B2F', '#00BFFF', '#B22222']},
    44: {'colors': ['#FFA07A', '#B22222', '#FFDAB9', '#E6E6FA']},
    45: {'colors': ['#FF69B4', '#BA55D3', '#F08080', '#2E8B57']},
}

# -------------------------------------------------------------------------------------

# --- Authentication Display Functions ---

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
    # CALL THE DASHBOARD FUNCTION HERE!
    project_dashboard() 

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
                        # Call the login function from the Connect mock module
                        user_data = Connect.login(username, password)
                        if user_data:
                            st.session_state.logged_in = True
                            st.session_state.username = user_data[0]
                            st.success("Logged in successfully! Redirecting...")
                            time.sleep(1) # Wait briefly before rerunning
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
                        # Call the registration function from the Connect mock module
                        if Connect.registration(new_username, new_email, new_password):
                            st.success("Registration successful! You can now log in.")
                        else:
                            st.error("Registration failed. Username or email may already exist.")
                    else:
                        st.error("Please fill in all fields.")

def main():
    """
    Main function for the Streamlit application, handling authentication flow.
    """
    
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
    # This is the linkage: If logged in, show project; otherwise, show login
    if st.session_state.logged_in:
        display_protected_project_page() 
    else:
        st.title("User Authentication App")
        st.caption("Please log in or register to access the Walmart Sales Dashboard.")
        display_login_or_register()

# -------------------------------------------------------------------------------------

# --- Main Dashboard Content Function (Original Logic) ---
def project_dashboard():
    """Contains the main dashboard content and Streamlit rendering logic."""
    
    # NOTE: This title is now displayed AFTER successful login.
    st.title("Walmart Sales Data Analysis Dashboard 📈")

    st.markdown("""
    Welcome to the interactive Walmart sales data dashboard. This application allows you to
    analyze key metrics and visualize trends from your uploaded CSV file using **interactive Plotly charts**.
    Use the sidebar to upload a file and apply filters to explore the data.
    """)

    # --- Sidebar File Uploader ---
    # NOTE: The sidebar is now shared with the authentication status display
    st.sidebar.header("Upload your CSV file")
    uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        
        # --- Data Loading and Preparation ---
        @st.cache_data
        def load_data(file):
            """Loads and prepares the data from the uploaded CSV file."""
            data = pd.read_csv(file)
            
            # --- FIX 1: Robust Date Conversion ---
            if 'Date' in data.columns:
                # Convert 'Date' column to datetime, setting dayfirst=True to handle common US date formats
                data['Date'] = pd.to_datetime(data['Date'], errors='coerce', dayfirst=True)
                data.dropna(subset=['Date'], inplace=True) 
            
            # --- FIX 2: Ensure Store is Integer for Color Lookup ---
            if 'Store' in data.columns:
                # Coerce to integer, dropping rows where 'Store' cannot be converted
                data['Store'] = pd.to_numeric(data['Store'], errors='coerce').astype('Int64')
                data.dropna(subset=['Store'], inplace=True) 
                
            return data

        # 1. INITIAL DATA LOAD - Use a placeholder for explicit removal
        loading_placeholder = st.empty() 
        
        with loading_placeholder.container():
            st.info('Reading and processing data from CSV...')
            if lottie_loading:
                st_lottie(lottie_loading, height=250, key="loading_animation_initial") 
            
            # Use try/except to catch data loading issues
            try:
                df = load_data(uploaded_file)
            except Exception as e:
                st.error(f"Failed to load or process data. Check the file format. Error: {e}")
                return
        
        # Explicitly clear the placeholder after data is loaded
        loading_placeholder.empty()

        # Robust check to ensure all necessary columns are present before proceeding
        required_columns = ['Store', 'Date', 'Weekly_Sales', 'Holiday_Flag', 'Temperature', 'Fuel_Price', 'Unemployment']
        if not all(col in df.columns for col in required_columns):
            missing_cols = [col for col in required_columns if col not in df.columns]
            st.error(f"Error: The uploaded file is missing the following required columns: **{', '.join(missing_cols)}**. Please upload a file with these columns.")
            return
        
        # Sort stores for clean selection
        stores_numeric = sorted(df['Store'].unique())
        
        # --- Sidebar Filters ---
        st.sidebar.header("Filter Data")

        # Store selector (returns an integer)
        selected_store_int = st.sidebar.selectbox("Select a Store", options=stores_numeric)
        
        # Date range selector
        min_date = df['Date'].min().date()
        max_date = df['Date'].max().date()
        date_range = st.sidebar.date_input(
            "Select Date Range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )

        # Apply basic store and date filters
        if len(date_range) == 2:
            start_date, end_date = date_range
            
            filtered_df = df[
                (df['Store'] == selected_store_int) & # Filter by integer store ID
                (df['Date'] >= pd.to_datetime(start_date)) &
                (df['Date'] <= pd.to_datetime(end_date))
            ].copy()
        else:
            st.warning("Please select a complete start and end date range.")
            return

        # Holiday filter
        holiday_filter = st.sidebar.checkbox("Show only Holiday Weeks", value=False)
        if holiday_filter:
            filtered_df = filtered_df[filtered_df['Holiday_Flag'] == 1]
            
        # --- CRITICAL FIX 3: Check for Empty Filtered Data ---
        if filtered_df.empty:
            st.warning("No data found for the selected store, date range, and filter combination. Please adjust your selections.")
            return

        # 2. FILTER/STORE SWITCHING - Animation for visual flair
        with st.spinner('Applying filters and generating visualizations...'):
            if lottie_loading:
                # Using a shorter animation for the filter update
                st_lottie(lottie_loading, height=100, key="loading_animation_filter") 
            time.sleep(0.5) 
            
            # Use the integer ID for lookups, which is now correct
            selected_color_set = store_colors.get(selected_store_int, {}).get('colors', ['#999999', '#AAAAAA', '#BBBBBB', '#CCCCCC'])
            
            # --- Display Raw Data ---
            with st.expander(f"Click to see Raw Data for Store {selected_store_int}"):
                st.dataframe(filtered_df)

            # --- Sidebar Plot Customization ---
            st.sidebar.markdown("---")
            st.sidebar.header("Plot Customization")
            
            n_bins = st.sidebar.slider(
                "Number of bins for Weekly Sales Distribution",
                min_value=5,
                max_value=100,
                value=25
            )

            # --- Main Content: Visualizations and Analysis ---
            st.header(f"Key Performance Indicators for Store {selected_store_int}")
            
            # Calculate metrics
            total_sales = np.sum(filtered_df['Weekly_Sales'])
            avg_sales = np.mean(filtered_df['Weekly_Sales'])
            num_weeks = len(filtered_df)
            avg_temp = np.mean(filtered_df['Temperature'])
            avg_fuel = np.mean(filtered_df['Fuel_Price'])
            max_sales = np.max(filtered_df['Weekly_Sales'])
            min_sales = np.min(filtered_df['Weekly_Sales'])
            
            # Metric cards
            col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
            
            with col1:
                st.metric("Total Sales", f"${total_sales:,.2f}")
            with col2:
                st.metric("Avg Weekly Sales", f"${avg_sales:,.2f}")
            with col3:
                st.metric("Weeks Count", num_weeks)
            with col4:
                st.metric("Avg Temp", f"{avg_temp:.2f} °F")
            with col5:
                st.metric("Avg Fuel Price", f"${avg_fuel:.2f}")
            with col6:
                st.metric("Max Sales", f"${max_sales:,.2f}")
            with col7:
                st.metric("Min Sales", f"${min_sales:,.2f}")
                
            
            # ----------------------------------------------------
            # Plots 7 & 8: Violin and Box Plot for the SELECTED Store
            st.markdown("---")
            st.subheader(f"Weekly Sales Distribution for Store {selected_store_int}")

            plot_col1, plot_col2 = st.columns(2)

            # Violin Plot
            with plot_col1:
                st.markdown("##### Violin Plot")
                fig7 = px.violin(filtered_df, y='Weekly_Sales', box=True, points="all",
                                    labels={'Weekly_Sales': 'Weekly Sales ($)'},
                                    color_discrete_sequence=[selected_color_set[0]],
                                    template='plotly_dark'
                                )
                fig7.update_layout(xaxis={'visible': False, 'showticklabels': False})
                st.plotly_chart(fig7, use_container_width=True, height=600)
                
            # Box Plot
            with plot_col2:
                st.markdown("##### Box Plot")
                fig8 = px.box(filtered_df, y='Weekly_Sales',
                                     labels={'Weekly_Sales': 'Weekly Sales ($)'},
                                     color_discrete_sequence=[selected_color_set[1]],
                                     template='plotly_dark'
                                 )
                fig8.update_layout(xaxis={'visible': False, 'showticklabels': False})
                st.plotly_chart(fig8, use_container_width=True, height=600)
            # ----------------------------------------------------
            
            tab1, tab2 = st.tabs(["Sales & Distribution Analysis", "Correlation & Relationships"])
            
            with tab1:
                st.subheader("Weekly Sales Trend Over Time")
                fig = px.line(filtered_df, x='Date', y='Weekly_Sales',
                                    labels={'Weekly_Sales': 'Weekly Sales ($)'},
                                    color_discrete_sequence=[selected_color_set[2]],
                                    template='plotly_dark'
                                    )
                st.plotly_chart(fig, use_container_width=True, height=500)

                st.subheader("Weekly Sales Distribution")
                st.markdown(f"""
                    This histogram shows the **frequency of weekly sales amounts** for Store **{selected_store_int}** with **{n_bins}** bins.
                """)
                fig2 = go.Figure(data=[go.Histogram(
                    x=filtered_df['Weekly_Sales'],
                    nbinsx=n_bins,
                    marker_color=selected_color_set[1],
                    marker_line_color='black',
                    marker_line_width=1.5
                )])
                fig2.update_layout(
                    xaxis_title_text='Weekly Sales ($)',
                    yaxis_title_text='Frequency',
                    template='plotly_dark'
                )
                st.plotly_chart(fig2, use_container_width=True, height=500)

                st.subheader("Total Sales: Holiday vs. Non-Holiday Weeks")
                holiday_sales = filtered_df.groupby('Holiday_Flag')['Weekly_Sales'].sum().reset_index()
                holiday_sales['Week_Type'] = holiday_sales['Holiday_Flag'].map({0: 'Non-Holiday', 1: 'Holiday'})
                
                # Map colors for the bar chart
                store_color_map_tab1 = {
                    'Non-Holiday': selected_color_set[2],
                    'Holiday': selected_color_set[3]
                }

                fig3 = px.bar(holiday_sales, x='Week_Type', y='Weekly_Sales',
                                    labels={'Weekly_Sales': 'Total Sales ($)', 'Week_Type': 'Week Type'},
                                    color='Week_Type', 
                                    color_discrete_map=store_color_map_tab1,
                                    template='plotly_dark'
                                    )
                st.plotly_chart(fig3, use_container_width=True, height=500)
            
            with tab2:
                st.subheader("Weekly Sales vs. Temperature (Regression Plot)")
                fig4 = px.scatter(filtered_df, x='Temperature', y='Weekly_Sales', trendline="ols",
                                        labels={'Temperature': 'Temperature (F)', 'Weekly_Sales': 'Weekly Sales ($)'},
                                        color_discrete_sequence=[selected_color_set[0]],
                                        template='plotly_dark'
                                        )
                st.plotly_chart(fig4, use_container_width=True, height=500)

                st.subheader("Weekly Sales vs. Fuel Price")
                fig5 = px.scatter(filtered_df, x='Fuel_Price', y='Weekly_Sales',
                                        labels={'Fuel_Price': 'Fuel Price ($)', 'Weekly_Sales': 'Weekly Sales ($)'},
                                        color_discrete_sequence=[selected_color_set[1]],
                                        template='plotly_dark'
                                        )
                st.plotly_chart(fig5, use_container_width=True, height=500)

                st.subheader("Correlation Heatmap of Features")
                # Select key numerical columns for correlation calculation
                numerical_df = filtered_df[['Weekly_Sales', 'Temperature', 'Fuel_Price', 'Unemployment', 'Holiday_Flag']].select_dtypes(include=np.number)
                correlation_matrix = numerical_df.corr()
                
                fig6 = go.Figure(data=go.Heatmap(
                    z=correlation_matrix.values,
                    x=correlation_matrix.columns,
                    y=correlation_matrix.index,
                    colorscale='Twilight',
                    zmid=0,
                    text=correlation_matrix.round(2).values,
                    hoverinfo='text'
                ))
                
                fig6.update_layout(
                    margin=dict(l=50, r=50, t=50, b=50),
                    xaxis_nticks=len(correlation_matrix.columns),
                    yaxis_nticks=len(correlation_matrix.index),
                    template='plotly_dark'
                )
                
                st.plotly_chart(fig6, use_container_width=True, height=500)

    else:
        # Display this message when the user is logged in but hasn't uploaded a file yet.
        st.info("Please upload a CSV file to begin the analysis.")

# This line now calls the main function, which orchestrates the authentication flow.
if __name__ == "__main__":
    main()
