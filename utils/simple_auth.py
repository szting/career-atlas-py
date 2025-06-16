import streamlit as st

def check_password():
    """Returns `True` if the user had the correct password."""
    
    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == "Cl@r1tyC2r3r":
            st.session_state["authenticated"] = True
            del st.session_state["password"]  # Don't store password
        else:
            st.session_state["authenticated"] = False

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        # First run, show password input
        st.markdown("""
        <div style="text-align: center; padding: 50px;">
            <h1>🎯 Career Assessment Tool</h1>
            <p style="font-size: 18px; color: #666;">Please enter the password to continue</p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.text_input(
                "Password", 
                type="password", 
                on_change=password_entered, 
                key="password",
                placeholder="Enter password..."
            )
            if st.session_state.get("authenticated") == False and "password" not in st.session_state:
                st.error("😕 Incorrect password. Please try again.")
        
        return False
    
    return True

def logout():
    """Logout function to clear session state"""
    for key in list(st.session_state.keys()):
        if key != 'authenticated':
            del st.session_state[key]
    st.session_state.authenticated = False
