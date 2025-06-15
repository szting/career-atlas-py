import streamlit as st
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="Career Assessment Tool - Debug",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Debug information at the top
st.sidebar.title("🔍 Debug Info")
st.sidebar.write("Session State:")
for key, value in st.session_state.items():
    if key != "password":  # Don't show password
        st.sidebar.write(f"- {key}: {value}")

# Import after page config
from utils.session_state import init_session_state
from utils.auth import check_password, is_session_valid, refresh_session

# Initialize session state
init_session_state()

# Force logout button for testing
if st.sidebar.button("🔄 Force Logout (Debug)"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# Main authentication check
st.write("### Authentication Status")
st.write(f"- Authenticated: {st.session_state.get('authenticated', False)}")
st.write(f"- Session Valid: {is_session_valid()}")

# Check authentication and session validity
if not st.session_state.authenticated or not is_session_valid():
    st.warning("Not authenticated - showing login form")
    if not check_password():
        st.stop()
else:
    # Refresh session on activity
    refresh_session()
    st.success("✅ Authenticated! Main app would load here.")
    
    # Import pages only after authentication
    from pages import (
        persona_selection,
        welcome,
        riasec_assessment,
        skills_assessment,
        values_assessment,
        results,
        coaching_dashboard,
        manager_dashboard,
        admin_panel
    )
    
    st.write("Current step:", st.session_state.current_step)
