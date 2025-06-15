import streamlit as st
import plotly.graph_objects as go
from utils.career_matcher import match_careers

def render():
    st.title("📊 Your Career Assessment Results")
    
    # RIASEC Profile
    st.subheader("Your RIASEC Personality Profile")
    
    # Create spider diagram
    categories = list(st.session_state.riasec_scores.keys())
    values = list(st.session_state.riasec_scores.values())
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=[cat.capitalize() for cat in categories],
        fill='toself',
        name='Your Profile',
        line_color='#4CAF50'
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
    
    # Top RIASEC types
    sorted_types = sorted(st.session_state.riasec_scores.items(), key=lambda x: x[1], reverse=True)
    st.markdown(f"**Your Primary Type:** {sorted_types[0][0].capitalize()}")
    st.markdown(f"**Your Secondary Type:** {sorted_types[1][0].capitalize()}")
    
    # Career Matches
    st.subheader("🎯 Recommended Career Paths")
    
    # Get career matches
    careers = match_careers(
        st.session_state.riasec_scores,
        st.session_state.skills_confidence,
        st.session_state.work_values
    )
    
    for i, career in enumerate(careers[:5]):
        with st.expander(f"{i+1}. {career['title']} - {career['match_score']}% Match"):
            st.markdown(f"**Description:** {career['description']}")
            st.markdown(f"**Required Skills:** {', '.join(career['required_skills'])}")
            st.markdown(f"**Work Environment:** {', '.join(career['work_environment'])}")
            st.markdown(f"**Salary Range:** {career['salary_range']}")
            st.markdown(f"**Growth Outlook:** {career['growth_outlook']}")
    
    # Skills Summary
    st.subheader("💪 Your Top Skills")
    top_skills = sorted(st.session_state.skills_confidence.items(), key=lambda x: x[1], reverse=True)[:5]
    
    for skill, confidence in top_skills:
        st.progress(confidence/100)
        st.caption(f"{skill}: {confidence}%")
    
    # Work Values
    st.subheader("💎 Your Core Work Values")
    for value in st.session_state.work_values:
        st.markdown(f"• {value}")
    
    # Actions
    st.markdown("---")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Download Report"):
            st.info("Report download feature coming soon!")
    
    with col2:
        if st.button("💬 Get Coaching"):
            st.session_state.current_step = 'coaching'
            st.rerun()
