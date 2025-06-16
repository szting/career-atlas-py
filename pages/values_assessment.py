import streamlit as st
from data.work_values import work_values

def show_values_assessment():
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1>Work Values Assessment</h1>
        <p style="font-size: 18px; color: #666;">Select your top 5 most important work values</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Progress
    st.progress(0.6)
    
    st.markdown("---")
    
    # Display selected count
    selected_count = len(st.session_state.selected_values)
    if selected_count < 5:
        st.info(f"Selected: {selected_count}/5 values")
    else:
        st.success(f"✓ Selected: {selected_count}/5 values")
    
    # Values grid
    cols = st.columns(2)
    for i, value in enumerate(work_values):
        with cols[i % 2]:
            # Checkbox for each value
            selected = st.checkbox(
                value['name'],
                value=value['name'] in st.session_state.selected_values,
                key=f"value_{value['name']}",
                disabled=len(st.session_state.selected_values) >= 5 and value['name'] not in st.session_state.selected_values
            )
            
            st.caption(value['description'])
            
            # Update selection
            if selected and value['name'] not in st.session_state.selected_values:
                st.session_state.selected_values.append(value['name'])
            elif not selected and value['name'] in st.session_state.selected_values:
                st.session_state.selected_values.remove(value['name'])
            
            st.markdown("---")
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.current_step = 'skills'
            st.rerun()
    
    with col2:
        if st.button(
            "Complete Assessment →", 
            use_container_width=True,
            disabled=len(st.session_state.selected_values) != 5
        ):
            # Update profile
            st.session_state.user_profile['workValues'] = st.session_state.selected_values.copy()
            st.session_state.user_profile['completedAssessments'].append('values')
            
            # Store in assessment history
            st.session_state.assessment_history.append({
                'type': 'values',
                'data': st.session_state.selected_values.copy(),
                'timestamp': 'current'
            })
            
            # Calculate career matches
            from utils.career_matcher import calculate_career_matches
            st.session_state.recommended_careers = calculate_career_matches(st.session_state.user_profile)
            
            # Navigate based on persona
            if st.session_state.selected_persona == 'individual':
                st.session_state.current_step = 'results'
            elif st.session_state.selected_persona == 'coach':
                st.session_state.current_step = 'coaching'
            else:
                st.session_state.current_step = 'manager'
            
            st.session_state.game_progress = 100
            st.rerun()
