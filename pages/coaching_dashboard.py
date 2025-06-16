import streamlit as st
from data.coaching_questions import coaching_questions

def show_coaching_dashboard():
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1>🎯 Career Coaching Dashboard</h1>
        <p style="font-size: 18px; color: #666;">Personalized coaching based on your assessment</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get top RIASEC type
    top_type = max(
        st.session_state.user_profile['riasecScores'].items(), 
        key=lambda x: x[1]
    )[0]
    
    st.markdown(f"### Your Primary Interest Type: {top_type.capitalize()}")
    
    # Filter coaching questions for top type
    relevant_questions = [q for q in coaching_questions if q.get('riasecFocus') == top_type]
    
    if relevant_questions:
        st.markdown("### Coaching Questions for Reflection")
        
        for i, question in enumerate(relevant_questions[:5]):
            with st.expander(f"Question {i+1}: {question['question']}"):
                st.markdown(f"**Purpose:** {question['purpose']}")
                
                if 'followUp' in question:
                    st.markdown("**Follow-up questions:**")
                    for followup in question['followUp']:
                        st.markdown(f"- {followup}")
                
                # Text area for notes
                st.text_area(
                    "Your thoughts:",
                    key=f"coaching_notes_{i}",
                    placeholder="Reflect on this question..."
                )
    
    st.markdown("---")
    
    # Career exploration tools
    st.markdown("### Career Exploration Tools")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **🔍 Research Resources**
        - O*NET Interest Profiler
        - Bureau of Labor Statistics
        - Professional associations
        - LinkedIn career insights
        """)
    
    with col2:
        st.markdown("""
        **📚 Skill Development**
        - Online courses (Coursera, edX)
        - Professional certifications
        - Mentorship programs
        - Industry workshops
        """)
    
    st.markdown("---")
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Results", use_container_width=True):
            st.session_state.current_step = 'results'
            st.rerun()
    
    with col2:
        if st.button("🔄 Start New Assessment", use_container_width=True):
            # Reset session state
            for key in ['user_profile', 'riasec_answers', 'skills_answers', 
                       'selected_values', 'recommended_careers', 'game_progress']:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.current_step = 'persona'
            st.rerun()
