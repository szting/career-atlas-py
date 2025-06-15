import streamlit as st
from typing import Dict, List
from datetime import datetime

def init_session_state():
    """Initialize all session state variables"""
    
    # Authentication - Simple approach
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'auth_time' not in st.session_state:
        st.session_state.auth_time = None
    
    # API Keys - Initialize with empty string if not set
    if 'api_keys' not in st.session_state:
        st.session_state.api_keys = {
            'openai': '',
            'anthropic': '',
            'google': ''
        }
    
    # Load API key from environment if available
    import os
    if os.getenv('OPENAI_API_KEY'):
        st.session_state.api_keys['openai'] = os.getenv('OPENAI_API_KEY')
    
    # User flow
    if 'current_step' not in st.session_state:
        st.session_state.current_step = 'persona'
    
    if 'selected_persona' not in st.session_state:
        st.session_state.selected_persona = None
    
    # Assessment data - Initialize with proper structure
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
    
    # Progress tracking
    if 'game_progress' not in st.session_state:
        st.session_state.game_progress = 0
    
    # Admin panel
    if 'show_admin' not in st.session_state:
        st.session_state.show_admin = False
    
    # Coaching data
    if 'coaching_questions' not in st.session_state:
        st.session_state.coaching_questions = []
    
    if 'reflection_questions' not in st.session_state:
        st.session_state.reflection_questions = []
    
    # Career recommendations
    if 'career_recommendations' not in st.session_state:
        st.session_state.career_recommendations = []
    
    # Uploaded frameworks
    if 'uploaded_frameworks' not in st.session_state:
        st.session_state.uploaded_frameworks = {}
