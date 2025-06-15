import streamlit as st
from streamlit_option_menu import option_menu
import os
from dotenv import load_dotenv
from utils.session_state import init_session_state
from utils.auth import check_password
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

# Load environment variables
load_dotenv()

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="Career Assessment Tool",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
init_session_state()

# Custom CSS
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stButton > button {
        width: 100%;
        background-color: #4CAF50;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background-color: #45a049;
        transform: translateY(-2px);
    }
    .assessment-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    .progress-bar {
        background-color: #e0e0e0;
        border-radius: 10px;
        height: 10px;
        margin: 1rem 0;
    }
    .progress-fill {
        background-color: #4CAF50;
        height: 100%;
        border-radius: 10px;
        transition: width 0.3s ease;
    }
</style>
""", unsafe_allow_html=True)

# Check authentication FIRST - before any other content
if not st.session_state.authenticated:
    if not check_password():
        st.stop()

# Only show the main app if authenticated
# Sidebar navigation
with st.sidebar:
    st.title("🎯 Career Assessment")
    
    # Show progress if assessment started
    if st.session_state.current_step not in ['persona', 'welcome']:
        progress = st.session_state.game_progress
        st.progress(progress / 100)
        st.caption(f"Progress: {progress}%")
    
    # Navigation menu based on persona
    if st.session_state.selected_persona == 'individual':
        selected = option_menu(
            menu_title="Navigation",
            options=["Assessment", "Results", "Coaching"],
            icons=["clipboard-check", "graph-up", "chat-dots"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "0!important", "background-color": "#fafafa"},
                "icon": {"color": "#4CAF50", "font-size": "20px"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px"},
                "nav-link-selected": {"background-color": "#e8f5e9"},
            }
        )
    elif st.session_state.selected_persona == 'coach':
        selected = option_menu(
            menu_title="Navigation",
            options=["Coaching Dashboard"],
            icons=["person-badge"],
            menu_icon="cast",
            default_index=0
        )
    elif st.session_state.selected_persona == 'manager':
        selected = option_menu(
            menu_title="Navigation",
            options=["Manager Dashboard"],
            icons=["people"],
            menu_icon="cast",
            default_index=0
        )
    else:
        selected = None
    
    # Admin access
    st.divider()
    if st.button("🔐 Admin Access"):
        st.session_state.show_admin = True
    
    # Logout button
    if st.button("🚪 Logout"):
        st.session_state.authenticated = False
        st.session_state.current_step = 'persona'
        st.session_state.selected_persona = None
        st.rerun()

# Main content routing
if st.session_state.show_admin:
    admin_panel.render()
elif st.session_state.current_step == 'persona':
    persona_selection.render()
elif st.session_state.current_step == 'welcome':
    welcome.render()
elif st.session_state.selected_persona == 'individual':
    if selected == "Assessment":
        if st.session_state.current_step == 'riasec':
            riasec_assessment.render()
        elif st.session_state.current_step == 'skills':
            skills_assessment.render()
        elif st.session_state.current_step == 'values':
            values_assessment.render()
    elif selected == "Results":
        if st.session_state.current_step in ['results', 'coaching', 'reflection']:
            results.render()
        else:
            st.info("Please complete the assessment first to view results.")
    elif selected == "Coaching":
        if st.session_state.current_step in ['coaching', 'reflection']:
            coaching_dashboard.render()
        else:
            st.info("Please complete the assessment first to access coaching.")
elif st.session_state.selected_persona == 'coach':
    coaching_dashboard.render()
elif st.session_state.selected_persona == 'manager':
    manager_dashboard.render()
