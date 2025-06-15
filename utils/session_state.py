import streamlit as st

def init_session_state():
    """Initialize all session state variables"""
    
    # Core navigation states
    if 'selected_persona' not in st.session_state:
        st.session_state.selected_persona = None
    
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 'persona'
    
    if 'game_progress' not in st.session_state:
        st.session_state.game_progress = 0
    
    if 'show_admin' not in st.session_state:
        st.session_state.show_admin = False
    
    # Assessment data
    if 'riasec_scores' not in st.session_state:
        st.session_state.riasec_scores = {
            'realistic': 0,
            'investigative': 0,
            'artistic': 0,
            'social': 0,
            'enterprising': 0,
            'conventional': 0
        }
    
    if 'skills_confidence' not in st.session_state:
        st.session_state.skills_confidence = {}
    
    if 'work_values' not in st.session_state:
        st.session_state.work_values = []
    
    if 'career_matches' not in st.session_state:
        st.session_state.career_matches = []
    
    # User data
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ""
    
    if 'user_email' not in st.session_state:
        st.session_state.user_email = ""
    
    # API settings
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = ""
