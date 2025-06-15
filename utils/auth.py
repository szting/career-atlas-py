import streamlit as st
import os
import hashlib
import time
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

def hash_password(password: str) -> str:
    """Hash a password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_password():
    """Returns `True` if the user had the correct password."""
    
    # Initialize login attempts tracking
    if 'login_attempts' not in st.session_state:
        st.session_state.login_attempts = 0
    if 'last_attempt_time' not in st.session_state:
        st.session_state.last_attempt_time = None
    
    # Check for rate limiting (max 5 attempts per 15 minutes)
    if st.session_state.login_attempts >= 5:
        if st.session_state.last_attempt_time:
            time_since_last = datetime.now() - st.session_state.last_attempt_time
            if time_since_last < timedelta(minutes=15):
                remaining_time = timedelta(minutes=15) - time_since_last
                st.error(f"🔒 Too many failed attempts. Please try again in {remaining_time.seconds // 60} minutes.")
                return False
            else:
                # Reset attempts after cooldown
                st.session_state.login_attempts = 0
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        entered_password = st.session_state.get("password", "")
        
        # Get password from environment (should be hashed in production)
        correct_password = os.getenv("APP_PASSWORD", "career123")
        
        # For production, passwords should be stored as hashes
        # Example: correct_password_hash = os.getenv("APP_PASSWORD_HASH", hash_password("career123"))
        
        if entered_password == correct_password:
            st.session_state["authenticated"] = True
            st.session_state["auth_time"] = datetime.now()
            st.session_state.login_attempts = 0
            # Clear the password from session state
            if "password" in st.session_state:
                del st.session_state["password"]
        else:
            st.session_state["authenticated"] = False
            st.session_state.login_attempts += 1
            st.session_state.last_attempt_time = datetime.now()
            # Clear password on failed attempt
            if "password" in st.session_state:
                del st.session_state["password"]

    # Check session timeout (30 minutes)
    if st.session_state.get("authenticated", False):
        auth_time = st.session_state.get("auth_time")
        if auth_time:
            time_since_auth = datetime.now() - auth_time
            if time_since_auth > timedelta(minutes=30):
                st.session_state["authenticated"] = False
                st.warning("⏱️ Your session has expired. Please log in again.")
                return False
        return True

    # Show login form
    st.title("🔐 Career Assessment Tool")
    st.markdown("### Please enter the password to continue")
    
    # Add subtle branding
    st.markdown("""
    <style>
    .login-container {
        max-width: 400px;
        margin: auto;
        padding: 2rem;
        background-color: #f8f9fa;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container():
            st.text_input(
                "Password", 
                type="password", 
                on_change=password_entered, 
                key="password",
                placeholder="Enter password",
                help="Contact your administrator for the password"
            )
            
            # Show error if authentication failed
            if st.session_state.get("login_attempts", 0) > 0:
                attempts_left = 5 - st.session_state.login_attempts
                if attempts_left > 0:
                    st.error(f"😕 Incorrect password. {attempts_left} attempts remaining.")
                else:
                    st.error("🔒 Account temporarily locked due to multiple failed attempts.")
            
            # Show demo credentials only in development mode
            if os.getenv("SHOW_DEMO_CREDENTIALS", "false").lower() == "true":
                with st.expander("Demo Credentials"):
                    st.info("""
                    **For testing purposes only:**
                    - App Password: career123
                    - Admin Password: admin123
                    
                    ⚠️ Change these passwords before deploying to production!
                    """)
            
            # Password requirements info
            with st.expander("Password Requirements"):
                st.markdown("""
                - Minimum 8 characters
                - At least one uppercase letter
                - At least one lowercase letter
                - At least one number
                - At least one special character
                """)
    
    # Footer
    st.markdown("---")
    st.caption("© 2024 Career Assessment Tool. All rights reserved.")
    
    return False

def check_admin_password(password: str) -> bool:
    """Check if admin password is correct"""
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")
    return password == admin_password

def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password strength
    Returns: (is_valid, error_message)
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"
    
    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"
    
    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"
    
    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        return False, "Password must contain at least one special character"
    
    return True, ""

def is_session_valid() -> bool:
    """Check if the current session is still valid"""
    if not st.session_state.get("authenticated", False):
        return False
    
    auth_time = st.session_state.get("auth_time")
    if not auth_time:
        return False
    
    # Check if session has expired (30 minutes)
    time_since_auth = datetime.now() - auth_time
    if time_since_auth > timedelta(minutes=30):
        return False
    
    return True

def refresh_session():
    """Refresh the session timestamp"""
    if st.session_state.get("authenticated", False):
        st.session_state["auth_time"] = datetime.now()
