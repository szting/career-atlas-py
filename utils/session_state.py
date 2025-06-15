import streamlit as st
from typing import Dict, List

def init_session_state():
    """Initialize all session state variables"""
    
    # User information
    if 'user_name' not in st.session_state:
        st.session_state.user_name = ''
    if 'user_email' not in st.session_state:
        st.session_state.user_email = ''
    
    # Authentication
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
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
            'openai': ''
        }
    
    # Coaching data
    if 'coaching_questions' not in st.session_state:
        st.session_state.coaching_questions = []
    if 'selected_question_index' not in st.session_state:
        st.session_state.selected_question_index = 0
    if 'user_responses' not in st.session_state:
        st.session_state.user_responses = {}
    
    # Manager data
    if 'team_members' not in st.session_state:
        st.session_state.team_members = []
    if 'selected_team_member' not in st.session_state:
        st.session_state.selected_team_member = None
    
    # Admin data
    if 'uploaded_frameworks' not in st.session_state:
        st.session_state.uploaded_frameworks = []
    if 'career_database' not in st.session_state:
        st.session_state.career_database = []
