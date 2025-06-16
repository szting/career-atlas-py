import streamlit as st

def show_persona_selection():
    st.markdown("""
    <div style="text-align: center; padding: 50px;">
        <h1>🎯 Career Assessment Tool</h1>
        <p style="font-size: 20px; color: #666; margin-bottom: 40px;">Choose your role to begin</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div style="background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); height: 300px;">
            <h3 style="color: #4F46E5;">👤 Individual</h3>
            <p>Take the assessment to discover career paths that match your personality and interests</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start as Individual", key="individual", use_container_width=True):
            st.session_state.selected_persona = 'individual'
            st.session_state.current_step = 'welcome'
            st.rerun()
    
    with col2:
        st.markdown("""
        <div style="background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); height: 300px;">
            <h3 style="color: #059669;">🎯 Career Coach</h3>
            <p>Guide others through their career exploration with coaching tools and insights</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start as Coach", key="coach", use_container_width=True):
            st.session_state.selected_persona = 'coach'
            st.session_state.current_step = 'welcome'
            st.rerun()
    
    with col3:
        st.markdown("""
        <div style="background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); height: 300px;">
            <h3 style="color: #DC2626;">👔 Manager</h3>
            <p>Understand your team better and support their career development</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Start as Manager", key="manager", use_container_width=True):
            st.session_state.selected_persona = 'manager'
            st.session_state.current_step = 'welcome'
            st.rerun()
    
    # Admin access
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("🔧 Admin Panel", key="admin_access"):
            st.session_state.current_step = 'admin'
            st.rerun()
