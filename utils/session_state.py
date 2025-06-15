import streamlit as st

def init_session_state():
    """Initialize all session state variables"""
    
    # Authentication
    if 'authentication_status' not in st.session_state:
        st.session_state.authentication_status = None
    
    # Navigation
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 'persona'
    
    if 'selected_persona' not in st.session_state:
        st.session_state.selected_persona = None
    
    if 'show_admin' not in st.session_state:
        st.session_state.show_admin = False
    
    # Progress tracking
    if 'game_progress' not in st.session_state:
        st.session_state.game_progress = 0
    
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
    
    # API Keys
    if 'api_keys' not in st.session_state:
        st.session_state.api_keys = {
            'openai': st.secrets.get('api_keys', {}).get('openai', '')
        }
    
    # User data
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ''
    
    if 'user_email' not in st.session_state:
        st.session_state.user_email = ''
    
    # Coaching data
    if 'coaching_questions' not in st.session_state:
        st.session_state.coaching_questions = []
    
    if 'reflection_questions' not in st.session_state:
        st.session