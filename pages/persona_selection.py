import streamlit as st

def render():
    st.title("🎯 Career Assessment Tool")
    st.subheader("Select Your Role")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="assessment-card">
            <h3>👤 Individual</h3>
            <p>Take the career assessment to discover your ideal career path</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("I'm an Individual", key="individual_btn", use_container_width=True):
            st.session_state.selected_persona = 'individual'
            st.session_state.current_step = 'welcome'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div class="assessment-card">
            <h3>🎓 Career Coach</h3>
            <p>Access coaching tools and client assessments</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("I'm a Coach", key="coach_btn", use_container_width=True):
            st.session_state.selected_persona = 'coach'
            st.session_state.current_step = 'coach_dashboard'
            st.rerun()
    
    with col3:
        st.markdown("""
        <div class="assessment-card">
            <h3>👔 Manager</h3>
            <p>View team assessments and development insights</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("I'm a Manager", key="manager_btn", use_container_width=True):
            st.session_state.selected_persona = 'manager'
            st.session_state.current_step = 'manager_dashboard'
            st.rerun()
