import streamlit as st
from data.riasec_questions import riasec_questions

def show_riasec_assessment():
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1>RIASEC Personality Assessment</h1>
        <p style="font-size: 18px; color: #666;">Rate how much you agree with each statement</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress bar
    progress = (len(st.session_state.riasec_answers) / len(riasec_questions)) * 100
    st.progress(progress / 100)
    
    # Questions
    st.markdown("---")
    
    for i, question in enumerate(riasec_questions):
        st.markdown(f"**{i+1}. {question['text']}**")
        
        # Create unique key for each question
        key = f"riasec_{question['id']}"
        
        # Radio buttons for rating
        rating = st.radio(
            "Rate:",
            options=[1, 2, 3, 4, 5],
            format_func=lambda x: {
                1: "Strongly Disagree",
                2: "Disagree", 
                3: "Neutral",
                4: "Agree",
                5: "Strongly Agree"
            }[x],
            horizontal=True,
            key=key,
            index=st.session_state.riasec_answers.get(question['id'], 3) - 1
        )
        
        st.session_state.riasec_answers[question['id']] = rating
        st.markdown("---")
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.current_step = 'welcome'
            st.rerun()
    
    with col2:
        if st.button("Continue →", use_container_width=True):
            # Calculate RIASEC scores
            scores = {
                'realistic': 0,
                'investigative': 0,
                'artistic': 0,
                'social': 0,
                'enterprising': 0,
                'conventional': 0
            }
            
            for question in riasec_questions:
                rating = st.session_state.riasec_answers.get(question['id'], 3)
                scores[question['type']] += rating
            
            # Normalize scores (0-5 scale)
            questions_per_type = len(riasec_questions) // 6
            for key in scores:
                scores[key] = scores[key] / questions_per_type
            
            # Update profile
            st.session_state.user_profile['riasecScores'] = scores
            st.session_state.user_profile['completedAssessments'].append('riasec')
            
            # Store in assessment history for analytics
            st.session_state.assessment_history.append({
                'type': 'riasec',
                'data': scores,
                'timestamp': 'current'
            })
            
            # Navigate to next step
            st.session_state.current_step = 'skills'
            st.session_state.game_progress = 40
            st.rerun()
