import streamlit as st
from utils.openai_service import OpenAIService
import json

def render():
    if st.session_state.selected_persona == 'coach':
        render_coach_view()
    else:
        render_individual_coaching()

def render_individual_coaching():
    """Render coaching interface for individuals"""
    st.title("💬 Personalized Career Coaching")
    
    # Check if assessment is complete
    if not st.session_state.riasec_scores or not st.session_state.skills_confidence:
        st.warning("Please complete the assessment first to access personalized coaching.")
        return
    
    # Initialize OpenAI service
    openai_service = OpenAIService()
    
    # Generate coaching questions if not already generated
    if not st.session_state.coaching_questions:
        with st.spinner("Generating personalized coaching questions..."):
            user_profile = {
                'riasec_scores': st.session_state.riasec_scores,
                'skills_confidence': st.session_state.skills_confidence,
                'work_values': st.session_state.work_values
            }
            st.session_state.coaching_questions = openai_service.generate_coaching_questions(user_profile)
    
    # Display coaching interface
    st.markdown("### Let's explore your career journey together")
    
    # Question categories
    categories = ['exploration', 'development', 'goal-setting', 'reflection']
    category_names = {
        'exploration': '🔍 Career Exploration',
        'development': '📈 Skill Development',
        'goal-setting': '🎯 Goal Setting',
        'reflection': '💭 Self Reflection'
    }
    
    # Category tabs
    tabs = st.tabs([category_names[cat] for cat in categories])
    
    for i, (tab, category) in enumerate(zip(tabs, categories)):
        with tab:
            category_questions = [q for q in st.session_state.coaching_questions if q['category'] == category]
            
            if category_questions:
                for j, question in enumerate(category_questions):
                    with st.expander(f"Question {j+1}: {question['question'][:50]}...", expanded=(j==0)):
                        st.markdown(f"**{question['question']}**")
                        
                        # Purpose of the question
                        st.info(f"💡 **Why this matters:** {question['purpose']}")
                        
                        # User response area
                        response_key = f"response_{category}_{j}"
                        response = st.text_area(
                            "Your thoughts:",
                            value=st.session_state.user_responses.get(response_key, ''),
                            key=f"text_{response_key}",
                            height=100,
                            placeholder="Take your time to reflect and share your thoughts..."
                        )
                        
                        if response:
                            st.session_state.user_responses[response_key] = response
                        
                        # Follow-up questions
                        if question.get('follow_up'):
                            st.markdown("**Consider also:**")
                            for follow_up in question['follow_up']:
                                st.markdown(f"• {follow_up}")
            else:
                st.info(f"No questions available for {category_names[category]}")
    
    # Progress and actions
    st.markdown("---")
    
    # Show coaching progress
    total_questions = len(st.session_state.coaching_questions)
    answered_questions = len(st.session_state.user_responses)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.progress(answered_questions / total_questions if total_questions > 0 else 0)
    with col2:
        st.caption(f"{answered_questions}/{total_questions} answered")
    
    # Action buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Save Responses", use_container_width=True):
            save_coaching_responses()
    
    with col2:
        if st.button("🔄 Generate New Questions", use_container_width=True):
            st.session_state.coaching_questions = []
            st.session_state.user_responses = {}
            st.rerun()
    
    with col3:
        if st.button("📊 Back to Results", use_container_width=True):
            st.session_state.current_step = 'results'
            st.rerun()

def render_coach_view():
    """Render coach dashboard"""
    st.title("🎓 Career Coach Dashboard")
    
    # Coach tools
    tab1, tab2, tab3 = st.tabs(["Client Sessions", "Assessment Tools", "Resources"])
    
    with tab1:
        st.subheader("Recent Client Sessions")
        
        # Mock client data
        clients = [
            {"name": "John Doe", "date": "2024-01-15", "status": "Completed", "primary_type": "Investigative"},
            {"name": "Jane Smith", "date": "2024-01-14", "status": "In Progress", "primary_type": "Artistic"},
            {"name": "Mike Johnson", "date": "2024-01-13", "status": "Scheduled", "primary_type": "Enterprising"}
        ]
        
        for client in clients:
            with st.expander(f"{client['name']} - {client['date']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Status", client['status'])
                with col2:
                    st.metric("Primary Type", client['primary_type'])
                with col3:
                    if st.button("View Details", key=f"view_{client['name']}"):
                        st.info("Client details view coming soon!")
    
    with tab2:
        st.subheader("Assessment Administration")
        
        # Quick