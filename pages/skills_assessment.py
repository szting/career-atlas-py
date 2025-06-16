import streamlit as st
from data.skills_list import skills_categories

def show_skills_assessment():
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1>Skills Confidence Assessment</h1>
        <p style="font-size: 18px; color: #666;">Rate your confidence level in each skill area</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress
    st.progress(0.4)
    
    st.markdown("---")
    
    # Skills by category
    for category in skills_categories:
        st.markdown(f"### {category['name']}")
        
        cols = st.columns(2)
        for i, skill in enumerate(category['skills']):
            with cols[i % 2]:
                # Create unique key
                key = f"skill_{skill.replace(' ', '_')}"
                
                # Slider for confidence
                confidence = st.slider(
                    skill,
                    min_value=1,
                    max_value=5,
                    value=st.session_state.skills_answers.get(skill, 3),
                    key=key,
                    format="%d"
                )
                
                st.session_state.skills_answers[skill] = confidence
        
        st.markdown("---")
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.current_step = 'riasec'
            st.rerun()
    
    with col2:
        if st.button("Continue →", use_container_width=True):
            # Update profile
            st.session_state.user_profile['skillsConfidence'] = st.session_state.skills_answers.copy()
            st.session_state.user_profile['completedAssessments'].append('skills')
            
            # Store in assessment history
            st.session_state.assessment_history.append({
                'type': 'skills',
                'data': st.session_state.skills_answers.copy(),
                'timestamp': 'current'
            })
            
            # Navigate
            st.session_state.current_step = 'values'
            st.session_state.game_progress = 60
            st.rerun()
