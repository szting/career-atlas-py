import streamlit as st

def render():
    st.title("💪 Skills Confidence Assessment")
    st.markdown("Rate your confidence level in each skill area.")
    
    # Progress
    st.session_state.game_progress = 50
    
    # Skills categories
    skills_categories = [
        {
            'name': 'Technical Skills',
            'skills': ['Problem Solving', 'Data Analysis', 'Programming', 'Research']
        },
        {
            'name': 'Creative Skills',
            'skills': ['Design', 'Writing', 'Innovation', 'Artistic Expression']
        },
        {
            'name': 'Interpersonal Skills',
            'skills': ['Communication', 'Leadership', 'Teamwork', 'Teaching']
        }
    ]
    
    if 'skills_confidence' not in st.session_state:
        st.session_state.skills_confidence = {}
    
    for category in skills_categories:
        st.subheader(category['name'])
        
        for skill in category['skills']:
            confidence = st.slider(
                skill,
                0, 100, 
                value=st.session_state.skills_confidence.get(skill, 50),
                key=f"skill_{skill}",
                format="%d%%"
            )
            st.session_state.skills_confidence[skill] = confidence
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("← Back", key="back_skills"):
            st.session_state.current_step = 'riasec'
            st.rerun()
    
    with col2:
        if st.button("Next →", key="next_skills"):
            st.session_state.current_step = 'values'
            st.session_state.game_progress = 70
            st.rerun()
