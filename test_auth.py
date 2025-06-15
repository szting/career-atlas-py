import streamlit as st
from utils.session_state import init_session_state
from utils.auth import check_password

# Page config
st.set_page_config(
    page_title="Auth Test",
    page_icon="🔐",
    layout="wide"
)

# Initialize session state
init_session_state()

# Debug info
st.write("Debug Info:")
st.write(f"Authenticated: {st.session_state.get('authenticated', False)}")
st.write(f"Session State Keys: {list(st.session_state.keys())}")

# Check password
if not st.session_state.get('authenticated', False):
    st.write("Not authenticated - showing login form")
    if not check_password():
        st.stop()
else:
    st.success("You are authenticated!")
    st.write("Main app content would go here")
    
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.rerun()
