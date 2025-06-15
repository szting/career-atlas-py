import streamlit as st
import plotly.graph_objects as go
from utils.career_matcher import match_careers, get_top_riasec_types
from utils.openai_service import OpenAIService
import pandas as pd

def render():
    st.title("📊 Your Career Assessment Results")
    
    # Create tabs for different views
    tab1, tab2, tab3, tab4 = st.tabs(["RIASEC Profile", "Skills Analysis", "Career Matches", "Development Plan"])
    
    with tab1:
        render_riasec_profile()
    
    with tab2:
        render_skills_analysis()
    
    with tab3:
        render_career_matches()
    
    with tab4:
        render_development_plan()

def render_riasec_profile():
    """Render RIASEC personality profile"""
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
        line_color='#4CAF50',
        fillcolor='rgba(76, 175, 80, 0.3)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )),
        showlegend=False,
        height=400,
        title="RIASEC Interest Profile"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Top RIASEC types
    sorted_types = sorted(st.session_state.riasec_scores.items(), key=lambda x: x[1], reverse=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Primary Type", sorted_types[0][0].capitalize(), f"{sorted_types[0][1]}/5")
    with col2:
        st.metric("Secondary Type", sorted_types[1][0].capitalize(), f"{sorted_types[1][1]}/5")
    with col3:
        st.metric("Tertiary Type", sorted_types[2][0].capitalize(), f"{sorted_types[2][1]}/5")
    
    # Type descriptions
    type_descriptions = {
        'realistic': "Practical, hands-on, physical activities",
        'investigative': "Thinking, researching, analytical work",
        'artistic': "Creative, innovative, expressive activities",
        'social': "Helping, teaching, interpersonal work",
        'enterprising': "Leading, persuading, business activities",
        'conventional': "Organizing, structured, detail-oriented work"
    }
    
    st.markdown("### Your Top Interest Areas:")
    for type_name, score in sorted_types[:3]:
        st.markdown(f"**{type_name.capitalize()}**: {type_descriptions[type_name]}")

def render_skills_analysis():
    """Render skills confidence vs RIASEC interests spider diagram"""
    st.subheader("Skills Confidence vs Career Interests Analysis")
    
    # Map skills to RIASEC categories
    skill_to_riasec = {
        'Problem Solving': 'investigative',
        'Technical Skills': 'realistic',
        'Communication': 'social',
        'Leadership': 'enterprising',
        'Creativity': 'artistic',
        'Organization': 'conventional',
        'Analytical Thinking': 'investigative',
        'Teamwork': 'social',
        'Attention to Detail': 'conventional',
        'Strategic Planning': 'enterprising',
        'Hands-on Work': 'realistic',
        'Innovation': 'artistic'
    }
    
    # Calculate average skill confidence per RIASEC type
    riasec_skill_confidence = {r: [] for r in st.session_state.riasec_scores.keys()}
    
    for skill, confidence in st.session_state.skills_confidence.items():
        if skill in skill_to_riasec:
            riasec_type = skill_to_riasec[skill]
            riasec_skill_confidence[riasec_type].append(confidence)
    
    # Calculate averages
    avg_skill_confidence = {}
    for riasec_type, confidences in riasec_skill_confidence.items():
        if confidences:
            avg_skill_confidence[riasec_type] = sum(confidences) / len(confidences)
        else:
            avg_skill_confidence[riasec_type] = 50  # Default middle value
    
    # Create combined spider diagram
    categories = [cat.capitalize() for cat in st.session_state.riasec_scores.keys()]
    
    fig = go.Figure()
    
    # Add RIASEC interests (normalized to 0-100 scale)
    riasec_values = [v * 20 for v in st.session_state.riasec_scores.values()]
    fig.add_trace(go.Scatterpolar(
        r=riasec_values,
        theta=categories,
        fill='toself',
        name='Career Interests',
        line_color='#4CAF50',
        fillcolor='rgba(76, 175, 80, 0.2)'
    ))
    
    # Add Skills Confidence
    skill_values = list(avg_skill_confidence.values())
    fig.add_trace(go.Scatterpolar(
        r=skill_values,
        theta=categories,
        fill='toself',
        name='Skills Confidence',
        line_color='#2196F3',
        fillcolor='rgba(33, 150, 243, 0.2)'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )),
        showlegend=True,
        height=500,
        title="Career Interests vs Skills Confidence"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Analysis insights
    st.markdown("### Key Insights:")
    
    gaps = []
    alignments = []
    
    for riasec_type in st.session_state.riasec_scores.keys():
        interest = riasec_values[list(st.session_state.riasec_scores.keys()).index(riasec_type)]
        confidence = avg_skill_confidence[riasec_type]
        gap = interest - confidence
        
        if gap > 20:
            gaps.append((riasec_type, gap))
        elif abs(gap) < 10:
            alignments.append(riasec_type)
    
    if alignments:
        st.success(f"✅ **Strong Alignment**: Your skills and interests align well in: {', '.join([a.capitalize() for a in alignments])}")
    
    if gaps:
        st.warning("📈 **Development Opportunities**:")
        for riasec_type, gap in gaps:
            st.markdown(f"- **{riasec_type.capitalize()}**: Your interest is high but skills confidence could be improved")
    
    # Top skills
    st.markdown("### Your Top Skills:")
    top_skills = sorted(st.session_state.skills_confidence.items(), key=lambda x: x[1], reverse=True)[:5]
    
    for skill, confidence in top_skills:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.progress(confidence/100)
        with col2:
            st.caption(f"{skill}: {confidence}%")

def render_career_matches():
    """Render career recommendations"""
    st.subheader("🎯 Recommended Career Paths")
    
    # Get career matches
    careers = match_careers(
        st.session_state.riasec_scores,
        st.session_state.skills_confidence,
        st.session_state.work_values
    )
    
    # Display top matches
    for i, career in enumerate(careers[:5]):
        with st.expander(f"{i+1}. {career['title']} - {career['match_score']}% Match", expanded=(i==0)):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {career['description']}")
                st.markdown(f"**Required Skills:** {', '.join(career['required_skills'])}")
                st.markdown(f"**Work Environment:** {', '.join(career['work_environment'])}")
            
            with col2:
                st.metric("Match Score", f"{career['match_score']}%")
                st.markdown(f"**Salary Range:** {career['salary_range']}")
                st.markdown(f"**Growth:** {career['growth_outlook']}")
            
            # Match breakdown
            st.markdown("**Why this matches your profile:**")
            top_riasec = get_top_riasec_types(st.session_state.riasec_scores, 2)
            career_riasec = career.get('riasec_profile', {})
            
            matching_types = []
            for type_name, score in top_riasec:
                if career_riasec.get(type_name, 0) >= 3:
                    matching_types.append(type_name.capitalize())
            
            if matching_types:
                st.markdown(f"- Aligns with your {' and '.join(matching_types)} interests")
            
            matching_skills = [s for s in career['required_skills'] if s in st.session_state.skills_confidence and st.session_state.skills_confidence[s] >= 70]
            if matching_skills:
                st.markdown(f"- Leverages your skills in: {', '.join(matching_skills)}")
            
            matching_values = list(set(career['work_environment']) & set(st.session_state.work_values))
            if matching_values:
                st.markdown(f"- Offers: {', '.join(matching_values)}")

def render_development_plan():
    """Render personalized development plan"""
    st.subheader("📚 Your Personalized Development Plan")
    
    # Get AI-generated recommendations if API key is available
    openai_service = OpenAIService()
    
    user_profile = {
        'riasec_scores': st.session_state.riasec_scores,
        'skills_confidence': st.session_state.skills_confidence,
        'work_values': st.session_state.work_values
    }
    
    # Generate development plan
    st.markdown("### Skill Development Priorities")
    
    # Identify skill gaps based on top career matches
    careers = match_careers(
        st.session_state.riasec_scores,
        st.session_state.skills_confidence,
        st.session_state.work_values
    )
    
    # Collect required skills from top 3 careers
    required_skills = set()
    for career in careers[:3]:
        required_skills.update(career['required_skills'])
    
    # Find skills to develop
    skills_to_develop = []
    for skill in required_skills:
        if skill not in st.session_state.skills_confidence:
            skills_to_develop.append((skill, 0))
        elif st.session_state.skills_confidence[skill] < 70:
            skills_to_develop.append((skill, st.session_state.skills_confidence[skill]))
    
    if skills_to_develop:
        st.markdown("**Skills to Develop:**")
        for skill, current_level in sorted(skills_to_develop, key=lambda x: x[1]):
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.markdown(f"• {skill}")
            with col2:
                st.caption(f"Current: {current_level}%")
            with col3:
                st.caption("Target: 80%")
    
    # Work values alignment
    st.markdown("### Work Environment Priorities")
    st.markdown("Based on your values, prioritize opportunities that offer:")
    for value in st.session_state.work_values[:5]:
        st.markdown(f"• {value}")
    
    # Action steps
    st.markdown("### Next Steps")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Immediate Actions (Next 30 days):**")
        st.markdown("1. Update your resume to highlight relevant skills")
        st.markdown("2. Research top 3 career matches in detail")
        st.markdown("3. Connect with professionals in target fields")
        st.markdown("4. Identify learning resources for skill gaps")
    
    with col2:
        st.markdown("**Long-term Actions (3-6 months):**")
        st.markdown("1. Complete online courses for skill development")
        st.markdown("2. Seek projects that align with career interests")
        st.markdown("3. Build portfolio demonstrating key skills")
        st.markdown("4. Apply for positions matching your profile")
    
    # Download report button
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📥 Download Full Report", use_container_width=True):
            st.info("Report generation feature coming soon!")
        
        if st.button("💬 Get Personalized Coaching", use_container_width=True):
            st.session_state.current_step = 'coaching'
            st.rerun()
