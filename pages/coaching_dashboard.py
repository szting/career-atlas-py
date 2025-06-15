import streamlit as st
from data.coaching_questions import coaching_questions
from utils.openai_service import OpenAIService
import random

def render():
    st.title("🎯 Career Coaching Dashboard")
    
    # Clear indication about whose data is being viewed
    st.info("📌 **Note**: The RIASEC scores and assessment data shown below are for your **coachee** (the person you are coaching), not your own scores.")
    
    # Check if coming from individual assessment
    if st.session_state.selected_persona == 'individual' and st.session_state.current_step == 'coaching':
        st.markdown("### Your Coaching Session")
        st.markdown("Based on your assessment results, here are personalized coaching questions to explore:")
        
        # Display user's RIASEC profile
        if st.session_state.riasec_scores:
            with st.expander("📊 Your RIASEC Profile", expanded=True):
                display_riasec_summary()
    else:
        # Coach persona view
        st.markdown("### Coaching Tools & Resources")
        
        # Coachee information section
        st.markdown("#### 👤 Coachee Information")
        
        col1, col2 = st.columns(2)
        with col1:
            coachee_name = st.text_input("Coachee's Name:", placeholder="Enter coachee's name")
        with col2:
            session_date = st.date_input("Session Date:")
        
        # Manual RIASEC input for coaches
        st.markdown("#### 📊 Coachee's RIASEC Assessment Results")
        st.caption("Enter your coachee's RIASEC scores from their assessment:")
        
        riasec_types = ['Realistic', 'Investigative', 'Artistic', 'Social', 'Enterprising', 'Conventional']
        coach_riasec_scores = {}