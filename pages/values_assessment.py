import streamlit as st

def render():
    st.title("💎 Work Values Assessment")
    st.markdown("Select your top 5 most important work values.")
    
    # Progress
    st.session_state.game_progress = 80
    
    work_values_list = [
        {'name': 'Work-Life Balance', 'description': 'Maintaining harmony between work and personal life'},
        {'name': 'Career Growth', 'description': 'Opportunities for advancement and skill development'},
        {'name': 'Job Security', 'description': 'Stable employment and financial security'},
        {'name': 'Creative Freedom', 'description': 'Ability to express creativity and innovation'},
        {'name': 'Social Impact', 'description': 'Making a positive difference in society'},
        {'name': 'Team Collaboration', 'description': 'Working closely with others'},
        {'name': 'Independence', 'description': 'Autonomy and self-direction in work'},
        {'name': 'Recognition', 'description': 'Being acknowledged for contributions'},
        {'name': 'Competitive Salary', 'description': 'High financial compensation'},
        {'name': 'Learning Opportunities', 'description': 'Continuous learning and development'}
    ]
    
    if 'work_values' not in st.session_state:
        st.session_state.work_values = []
    
    st.info(f"Selected: {len(st.session_state.work_values)}/5 values")
    
    for value in work_values_list:
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.markdown(f"**{value['name']}**")
            st.caption(value['description'])
        
        with col2:
            is_selected = value['name'] in st.session_state.work_values
            if st.checkbox("Select", key=f"value_{value['name']}", value=is_selected):
                if value['name'] not in st.session_state.work_values:
                    if len(st.session_state.work_values) < 5:
                        st.session_state.work_values.append(value['name'])
                    else:
                        st.warning("You can only select 5 values. Deselect one to choose another.")
                        st.rerun()
            else:
                if value['name'] in st.session_state.work_values:
                    st.session_state.work_values.remove(value['name'])
    
    st.markdown("---")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("← Back", key="back_values"):
            st.session_state.current_step = 'skills'
            st.rerun()
    
    with col2:
        if len(st.session_state.work_values) == 5:
            if st.button("View Results →", key="view_results"):
                st.session_state.current_step = 'results'
                st.session_state.game_progress = 100
                st.rerun()
        else:
            st.info("Please select exactly 5 values to continue")
