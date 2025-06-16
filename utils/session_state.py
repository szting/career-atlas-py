import streamlit as st

def init_session_state():
    """Initialize all session state variables"""
    
    # Authentication
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    # Navigation
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 'persona'
    
    if 'selected_persona' not in st.session_state:
        st.session_state.selected_persona = None
    
    # User profile
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {
            'name': '',
            'riasecScores': {
                'realistic': 0,
                'investigative': 0,
                'artistic': 0,
                'social': 0,
                'enterprising': 0,
                'conventional': 0
            },
            'skillsConfidence': {},
            'workValues': [],
            'completedAssessments': []
        }
    
    # Assessment progress
    if 'game_progress' not in st.session_state:
        st.session_state.game_progress = 0
    
    # Results
    if 'recommended_careers' not in st.session_state:
        st.session_state.recommended_careers = []
    
    # RIASEC assessment state
    if 'riasec_answers' not in st.session_state:
        st.session_state.riasec_answers = {}
    
    # Skills assessment state
    if 'skills_answers' not in st.session_state:
        st.session_state.skills_answers = {}
    
    # Values assessment state
    if 'selected_values' not in st.session_state:
        st.session_state.selected_values = []
    
    # Admin panel state
    if 'show_admin' not in st.session_state:
        st.session_state.show_admin = False
    
    # Store assessment data for analytics
    if 'assessment_history' not in st.session_state:
        st.session_state.assessment_history = []
