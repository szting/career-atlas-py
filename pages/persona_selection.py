import streamlit as st
from utils.session_state import init_session_state

def render():
    st.title("🎯 Career Assessment Tool")
    st.subheader("Choose Your Role")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="assessment-card">
            <h3>👤 Individual</h3>
            <p>Take the career assessment to discover your ideal career path based on your interests, skills, and values.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start as Individual", key="individual_btn"):
            st.session_state.selected_persona = 'individual'
            st.session_state.current_step = 'welcome'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="assessment-card">
            <h3>🎓 Career Coach</h3>
            <p>Access coaching tools and resources to guide individuals through their career development journey.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start as Coach", key="coach_btn"):
            st.session_state.selected_persona = 'coach'
            st.session_state.current_step = 'coaching'
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="assessment-card">
            <h3>👔 Manager</h3>
            <p>Use team insights and reflection tools to support your team members' career growth and development.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start as Manager", key="manager_btn"):
            st.session_state.selected_persona = 'manager'
            st.session_state.current_step = 'reflection'
            st.rerun()
