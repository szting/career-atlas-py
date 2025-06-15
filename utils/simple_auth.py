import streamlit as st
from datetime import datetime, timedelta

def check_simple_password():
    """Simple password authentication with session management"""
    
    # Check if already authenticated and session is valid
    if st.session_state.get('authenticated', False):
        auth_time = st.session_state.get('auth_time')
        if auth_time:
            # Check if session expired (30 minutes)
            if datetime.now() - auth_time < timedelta(minutes=30):
                return True
            else:
                # Session expired
                st.session_state.authenticated = False
                st.warning("⏱️ Session expired. Please log in again.")
    
    # Show login form
    st.title("🔐 Career Assessment Tool")
    st.markdown("### Please enter the password to continue")
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.form("login_form"):
            password = st.text_input(
                "Password", 
                type="password", 
                placeholder="Enter password"
            )
            
            submitted = st.form_submit_button("Login", use_container_width=True)
            
            if submitted:
                if password == "Cl@r1tyC2r33r":  # Fixed typo in password
                    st.session_state.authenticated = True
                    st.session_state.auth_time = datetime.now()
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Incorrect password. Please try again.")
    
    # Footer
    st.markdown("---")
    st.caption("© 2024 Career Assessment Tool. All rights reserved.")
    
    return False

def logout():
    """Clear authentication session"""
    st.session_state.authenticated = False
    if 'auth_time' in st.session_state:
        del st.session_state.auth_time
