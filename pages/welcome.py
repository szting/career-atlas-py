import streamlit as st

def render():
    st.title("🎯 Welcome to Your Career Journey!")
    
    st.markdown("""
    ### Discover Your Ideal Career Path
    
    This comprehensive assessment will help you understand:
    
    - **Your Personality Type** (RIASEC Model)
    - **Your Skills & Strengths**
    - **Your Work Values & Preferences**
    
    The assessment takes approximately 15-20 minutes to complete.
    """)
    
    # User information form
    with st.form("user_info"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Your Name", value=st.session_state.get('user_name', ''))
        
        with col2:
            email = st.text_input("Your Email", value=st.session_state.get('user_email', ''))
        
        submitted = st.form_submit_button("Start Assessment")
        
        if submitted:
            if name and email:
                st.session_state.user_name = name
                st.session_state.user_email = email
                st.session_state.current_step = 'riasec'
                st.session_state.game_progress = 10
                st.rerun()
            else:
                st.error("Please enter both your name and email to continue.")
    
    # Assessment overview
    st.markdown("---")
    st.subheader("What to Expect")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="assessment-card">
            <h4>1. RIASEC Assessment</h4>
            <p>Discover your personality type through Holland's career interest model.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="assessment-card">
            <h4>2. Skills Evaluation</h4>
            <p>Rate your confidence in various professional skills.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="assessment-card">
            <h4>3. Values Assessment</h4>
            <p>Identify what matters most to you in your work environment.</p>
        </div>
        """, unsafe_allow_html=True)
