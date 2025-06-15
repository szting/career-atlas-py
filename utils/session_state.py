import streamlit as st

def init_session_state():
    """Initialize all session state variables"""
    
    # Authentication state - Initialize first
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'auth_time' not in st.session_state:
        st.session_state.auth_time = None
    
    # User profile
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ""
    
    if 'user_email' not in st.session_state:
        st.session_state.user_email = ""
    
    # Persona selection
    if 'selected_persona' not in st.session_state:
        st.session_state.selected_persona = None
    
    # Assessment progress
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 'persona'
    
    if 'game_progress' not in st.session_state:
        st.session_state.game_progress = 0
    
    # RIASEC scores
    if 'riasec_scores' not in st.session_state:
        st.session_state.riasec_scores = {
            'realistic': 0,
            'investigative': 0,
            'artistic': 0,
            'social': 0,
            'enterprising': 0,
            'conventional': 0
        }
    
    if 'riasec_responses' not in st.session_state:
        st.session_state.riasec_responses = {}
    
    # Skills assessment
    if 'skills_confidence' not in st.session_state:
        st.session_state.skills_confidence = {}
    
    # Work values
    if 'work_values' not in st.session_state:
        st.session_state.work_values = []
    
    # Career recommendations
    if 'career_recommendations' not in st.session_state:
        st.session_state.career_recommendations = []
    
    # Coaching
    if 'coaching_responses' not in st.session_state:
        st.session_state.coaching_responses = {}
    
    if 'reflection_notes' not in st.session_state:
        st.session_state.reflection_notes = ""
    
    # Admin
    if 'show_admin' not in st.session_state:
        st.session_state.show_admin = False
    
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    # API keys
    if 'openai_api_key' not in st.session_state:
        st.session_state.openai_api_key = ""
    
    # Uploaded frameworks
    if 'uploaded_frameworks' not in st.session_state:
        st.session_state.uploaded_frameworks = {}
