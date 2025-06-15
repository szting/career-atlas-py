import streamlit as st

def render():
    st.title("💪 Skills Confidence Assessment")
    st.markdown("Rate your confidence level in each skill area (0-100%)")
    
    # Skill categories
    skill_categories = {
        "Technical Skills": [
            "Problem Solving",
            "Technical Skills",
            "Analytical Thinking",
            "Data Analysis",
            "Computer Skills"
        ],
        "Interpersonal Skills": [
            "Communication",
            "Teamwork",
            "Leadership",
            "Empathy",
            "Conflict Resolution"
        ],
        "Creative Skills": [
            "Creativity",
            "Innovation",
            "Design Thinking",
            "Artistic Expression",
            "Strategic Planning"
        ],
        "Organizational Skills": [
            "Organization",
            "Time Management",
            "Attention to Detail",
            "Project Management",
            "Process Improvement"
        ]
    }
    
    # Initialize skills confidence if not exists
    if not st.session_state.skills_confidence:
        st.session_state.skills_confidence = {}
    
    # Display skill sliders by category
    for category, skills in skill_categories.items():
        st.subheader(category)
        
        for skill in skills:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                confidence = st.slider(
                    skill,
                    min_value=0,
                    max_value=100,
                    value=st.session_state.skills_confidence.get(skill, 50),
                    step=5,
                    key=f"skill_{skill}",
                    help=f"How confident are you in your {skill.lower()} abilities?"
                )
                st.session_state.skills_confidence[skill] = confidence
            
            with col2:
                if confidence >= 80:
                    st.success(f"{confidence}%")
                elif confidence >= 60:
                    st.warning(f"{confidence}%")
                else:
                    st.error(f"{confidence}%")
        
        st.markdown("---")
    
    # Show skills summary
    with st.expander("Your Skills Summary", expanded=False):
        top_skills = sorted(st.session_state.skills_confidence.items(), key=lambda x: x[1], reverse=True)[:5]
        development_skills = sorted(st.session_state.skills_confidence.items(), key=lambda x: x[1])[:5]
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**💪 Your Strongest Skills:**")
            for skill, conf in top_skills:
                st.markdown(f"• {skill}: {conf}%")
        
        with col2:
            st.markdown("**📈 Skills to Develop:**")
            for skill, conf in development_skills:
                st.markdown(f"• {skill}: {conf}%")
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.current_step = 'riasec'
            st.session_state.game_progress = 10
            st.rerun()
    
    with col3:
        if st.button("Next →", use_container_width=True):
            st.session_state.current_step = 'values'
            st.session_state.game_progress = 70
            st.rerun()
