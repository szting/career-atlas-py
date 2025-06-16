import streamlit as st

def show_welcome():
    persona_titles = {
        'individual': 'Discover Your Career Path',
        'coach': 'Career Coaching Toolkit',
        'manager': 'Team Development Hub'
    }
    
    persona_descriptions = {
        'individual': 'Complete our comprehensive assessment to uncover careers that align with your personality, skills, and values.',
        'coach': 'Access powerful coaching tools and frameworks to guide others in their career journey.',
        'manager': 'Gain insights into your team members and support their professional growth.'
    }
    
    st.markdown(f"""
    <div style="text-align: center; padding: 40px;">
        <h1>{persona_titles.get(st.session_state.selected_persona, 'Welcome')}</h1>
        <p style="font-size: 18px; color: #666; margin-bottom: 30px;">
            {persona_descriptions.get(st.session_state.selected_persona, '')}
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Name input
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        name = st.text_input("What's your name?", placeholder="Enter your name...", key="name_input")
        
        if st.button("Continue", use_container_width=True, disabled=not name):
            st.session_state.user_profile['name'] = name
            st.session_state.current_step = 'riasec'
            st.session_state.game_progress = 20
            st.rerun()
        
        if st.button("← Back", use_container_width=True):
            st.session_state.current_step = 'persona'
            st.session_state.selected_persona = None
            st.rerun()
