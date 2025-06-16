import streamlit as st
import plotly.graph_objects as go

def show_results():
    st.markdown(f"""
    <div style="text-align: center; padding: 20px;">
        <h1>🎉 Assessment Complete!</h1>
        <p style="font-size: 20px;">Great job, {st.session_state.user_profile['name']}!</p>
    </div>
    """, unsafe_allow_html=True)
    
    # RIASEC Profile
    st.markdown("## Your RIASEC Profile")
    
    # Create radar chart
    categories = list(st.session_state.user_profile['riasecScores'].keys())
    values = list(st.session_state.user_profile['riasecScores'].values())
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=[cat.capitalize() for cat in categories],
        fill='toself',
        name='Your Profile'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )),
        showlegend=False,
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Top types
    sorted_types = sorted(
        st.session_state.user_profile['riasecScores'].items(), 
        key=lambda x: x[1], 
        reverse=True
    )
    
    st.markdown("### Your Top Interest Areas")
    for i, (type_name, score) in enumerate(sorted_types[:3]):
        st.markdown(f"**{i+1}. {type_name.capitalize()}** - Score: {score:.1f}/5")
    
    st.markdown("---")
    
    # Career Recommendations
    st.markdown("## Recommended Career Paths")
    
    for i, career in enumerate(st.session_state.recommended_careers[:5]):
        with st.expander(f"{i+1}. {career['title']} - {career['matchScore']}% Match"):
            st.markdown(f"**Description:** {career['description']}")
            st.markdown(f"**Primary Type:** {career['primary_type'].capitalize()}")
            st.markdown(f"**Required Skills:** {', '.join(career['required_skills'])}")
            st.markdown(f"**Salary Range:** {career['salary_range']}")
            st.markdown(f"**Growth Outlook:** {career['growth_outlook']}")
            st.markdown(f"**Education:** {career['education']}")
    
    st.markdown("---")
    
    # Actions
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📊 View Detailed Report", use_container_width=True):
            st.info("Detailed report feature coming soon!")
    
    with col2:
        if st.button("🎯 Explore Coaching", use_container_width=True):
            st.session_state.current_step = 'coaching'
            st.rerun()
    
    with col3:
        if st.button("🔄 Start Over", use_container_width=True):
            # Reset session state
            for key in ['user_profile', 'riasec_answers', 'skills_answers', 
                       'selected_values', 'recommended_careers', 'game_progress']:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.current_step = 'persona'
            st.rerun()
