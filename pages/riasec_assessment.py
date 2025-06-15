import streamlit as st
from data.riasec_questions import riasec_questions

def render():
    st.title("🎯 RIASEC Personality Assessment")
    st.markdown("Rate how much you agree with each statement on a scale of 1-5.")
    
    # Progress
    progress = 10 + (30 * st.session_state.get('riasec_progress', 0) / 100)
    st.session_state.game_progress = progress
    
    # Questions (simplified for now)
    if 'riasec_answers' not in st.session_state:
        st.session_state.riasec_answers = {}
    
    # Display a subset of questions for demo
    demo_questions = [
        {"id": "r1", "text": "I enjoy working with tools and machines", "type": "realistic"},
        {"id": "i1", "text": "I like to solve complex problems", "type": "investigative"},
        {"id": "a1", "text": "I enjoy creative activities like art, drama, or music", "type": "artistic"},
        {"id": "s1", "text": "I like helping and teaching others", "type": "social"},
        {"id": "e1", "text": "I enjoy leading and persuading people", "type": "enterprising"},
        {"id": "c1", "text": "I prefer working with data and details", "type": "conventional"}
    ]
    
    for i, question in enumerate(demo_questions):
        st.markdown(f"**{i+1}. {question['text']}**")
        rating = st.slider(
            "Rate your agreement",
            1, 5, 
            value=st.session_state.riasec_answers.get(question['id'], 3),
            key=f"riasec_{question['id']}"
        )
        st.session_state.riasec_answers[question['id']] = rating
        
        # Update scores
        if question['type'] in st.session_state.riasec_scores:
            st.session_state.riasec_scores[question['type']] = rating
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("← Back", key="back_riasec"):
            st.session_state.current_step = 'welcome'
            st.rerun()
    
    with col2:
        if st.button("Next →", key="next_riasec"):
            st.session_state.current_step = 'skills'
            st.session_state.game_progress = 40
            st.rerun()
