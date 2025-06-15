import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

def check_password():
    """Returns `True` if the user had the correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        entered_password = st.session_state.get("password", "")
        correct_password = os.getenv("APP_PASSWORD", "career123")
        
        if entered_password == correct_password:
            st.session_state["authenticated"] = True
            # Clear the password from session state
            if "password" in st.session_state:
                del st.session_state["password"]
        else:
            st.session_state["authenticated"] = False

    # Return True if already authenticated
    if st.session_state.get("authenticated", False):
        return True

    # Show login form
    st.title("🔐 Career Assessment Tool")
    st.markdown("### Please enter the password to continue")
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.text_input(
            "Password", 
            type="password", 
            on_change=password_entered, 
            key="password",
            placeholder="Enter password",
            help="Contact your administrator for the password"
        )
        
        # Show error if authentication failed
        if "password" in st.session_state and not st.session_state.get("authenticated", False):
            st.error("😕 Incorrect password. Please try again.")
        
        # Security note - remove in production
        with st.expander("Demo Credentials"):
            st.info("""
            **For testing purposes only:**
            - App Password: career123
            - Admin Password: admin123
            
            ⚠️ Change these passwords before deploying to production!
            """)
    
    return False

def check_admin_password(password: str) -> bool:
    """Check if admin password is correct"""
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
    return password == admin_password
