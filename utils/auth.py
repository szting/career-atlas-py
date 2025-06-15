import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

def check_password():
    """Returns `True` if the user had the correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == os.getenv("APP_PASSWORD", "career123"):
            st.session_state["authenticated"] = True
            del st.session_state["password"]  # Don't store password
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
            placeholder="Enter password"
        )
        
        if st.session_state.get("authenticated", False) == False:
            st.error("😕 Incorrect password")
            
        st.info("💡 Default password: career123")
    
    return False

def check_admin_password(password: str) -> bool:
    """Check if admin password is correct"""
    return password == os.getenv("ADMIN_PASSWORD", "admin123")
