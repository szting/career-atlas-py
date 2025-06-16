import streamlit as st
from utils.session_state import init_session_state
from utils.simple_auth import check_password

# Page configuration
st.set_page_config(
    page_title="Career Assessment Tool",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
init_session_state()

# Check authentication
if not check_password():
    st.stop()

# Import pages after authentication
from pages.persona_selection import show_persona_selection
from pages.welcome import show_welcome
from pages.riasec_assessment import show_riasec_assessment
from pages.skills_assessment import show_skills_assessment
from pages.values_assessment import show_values_assessment
from pages.results import show_results
from pages.coaching_dashboard import show_coaching_dashboard
from pages.manager_dashboard import show_manager_dashboard
from pages.admin_panel import show_admin_panel

# Main app logic
def main():
    # Handle navigation based on current step
    if st.session_state.current_step == 'persona':
        show_persona_selection()
    elif st.session_state.current_step == 'welcome':
        show_welcome()
    elif st.session_state.current_step == 'riasec':
        show_riasec_assessment()
    elif st.session_state.current_step == 'skills':
        show_skills_assessment()
    elif st.session_state.current_step == 'values':
        show_values_assessment()
    elif st.session_state.current_step == 'results':
        show_results()
    elif st.session_state.current_step == 'coaching':
        show_coaching_dashboard()
    elif st.session_state.current_step == 'manager':
        show_manager_dashboard()
    elif st.session_state.current_step == 'admin':
        show_admin_panel()

if __name__ == "__main__":
    main()
