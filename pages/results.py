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
    
    # Check if we have the necessary data
    if not st.session_state.get('riasec_scores') or not st.session_state.get('skills_confidence'):
        st.warning("Please complete the assessment first to view your skills analysis.")
        return
    
    # Comprehensive skill to RIASEC mapping with fallback for unmapped skills
    skill_to_riasec = {
        # Realistic
        'Technical Skills': 'realistic',
        'Hands-on Work': 'realistic',
        'Mechanical Aptitude': 'realistic',
        'Physical Coordination': 'realistic',
        'Tool Usage': 'realistic',
        
        # Investigative
        'Problem Solving': 'investigative',
        'Analytical Thinking': 'investigative',
        'Research': 'investigative',
        'Data Analysis': 'investigative',
        'Critical Thinking': 'investigative',
        
        # Artistic
        'Creativity': 'artistic',
        'Innovation': 'artistic',
        'Design Thinking': 'artistic',
        'Artistic Expression': 'artistic',
        'Imagination': 'artistic',
        
        # Social
        'Communication': 'social',
        'Teamwork': 'social',
        'Teaching': 'social',
        'Empathy': 'social',
        'Interpersonal Skills': 'social',
        
        # Enterprising
        'Leadership': 'enterprising',
        'Strategic Planning': 'enterprising',
        'Negotiation': 'enterprising',
        'Sales': 'enterprising',
        'Persuasion': 'enterprising',
        
        # Conventional
        'Organization': 'conventional',
        'Attention to Detail': 'conventional',
        'Administrative Skills': 'conventional',
        'Record Keeping': 'conventional',
        'Process Management': 'conventional',
        
        # Additional common skills
        'Time Management': 'conventional',
        'Project Management': 'enterprising',
        'Public Speaking': 'social',
        'Adaptability': 'investigative',
        'Writing': 'artistic'
    }
    
    # Calculate average skill confidence per RIASEC type
    riasec_skill_confidence = {r: [] for r in st.session_state.riasec_scores.keys()}
    unmapped_skills = []
    
    for skill, confidence in st.session_state.skills_confidence.items():
        if skill in skill_to_riasec:
            riasec_type = skill_to_riasec[skill]
            riasec_skill_confidence[riasec_type].append(confidence)
        else:
            unmapped_skills.append(skill)
            # Attempt to map based on keywords
            skill_lower = skill.lower()
            if any(word in skill_lower for word in ['tech', 'computer', 'build', 'fix']):
                riasec_skill_confidence['realistic'].append(confidence)
            elif any(word in skill_lower for word in ['analyz', 'research', 'data', 'think']):
                riasec_skill_confidence['investigative'].append(confidence)
            elif any(word in skill_lower for word in ['creat', 'design', 'art', 'innovat']):
                riasec_skill_confidence['artistic'].append(confidence)
            elif any(word in skill_lower for word in ['help', 'teach', 'commun', 'team']):
                riasec_skill_confidence['social'].append(confidence)
            elif any(word in skill_lower for word in ['lead', 'manag', 'business', 'sell']):
                riasec_skill_confidence['enterprising'].append(confidence)
            elif any(word in skill_lower for word in ['organiz', 'detail', 'admin', 'process']):
                riasec_skill_confidence['conventional'].append(confidence)
    
    # Calculate averages with proper handling
    avg_skill_confidence = {}
    for riasec_type, confidences in riasec_skill_confidence.items():
        if confidences:
            avg_skill_confidence[riasec_type] = sum(confidences) / len(confidences)
        else:
            # Use the RIASEC interest score as a baseline if no skills mapped
            avg_skill_confidence[riasec_type] = st.session_state.riasec_scores[riasec_type] * 20
    
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
        fillcolor='rgba(76, 175, 80, 0.2)',
        line=dict(width=2)
    ))
    
    # Add Skills Confidence
    skill_values = list(avg_skill_confidence.values())
    fig.add_trace(go.Scatterpolar(
        r=skill_values,
        theta=categories,
        fill='toself',
        name='Skills Confidence',
        line_color='#2196F3',
        fillcolor='rgba(33, 150, 243, 0.2)',
        line=dict(width=2)
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickmode='linear',
                tick0=0,
                dtick=20,
                ticktext=['0%', '20%', '40%', '60%', '80%', '100%'],
                tickvals=[0, 20, 40, 60, 80, 100]
            )),
        showlegend=True,
        height=500,
        title="Career Interests vs Skills Confidence",
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Show data table for transparency
    with st.expander("View Detailed Scores"):
        data = {
            'RIASEC Type': categories,
            'Career Interest (%)': [f"{v:.0f}%" for v in riasec_values],
            'Skills Confidence (%)': [f"{v:.0f}%" for v in skill_values],
            'Gap': [f"{abs(r-s):.0f}%" for r, s in zip(riasec_values, skill_values)]
        }
        st.dataframe(pd.DataFrame(data))
    
    # Analysis insights
    st.markdown("### Key Insights:")
    
    gaps = []
    alignments = []
    opportunities = []
    
    for i, riasec_type in enumerate(st.session_state.riasec_scores.keys()):
        interest = riasec_values[i]
        confidence = avg_skill_confidence[riasec_type]
        gap = interest - confidence
        
        if gap > 20:
            gaps.append((riasec_type, gap, interest, confidence))
        elif abs(gap) < 10:
            alignments.append((riasec_type, interest, confidence))
        elif confidence > interest + 20:
            opportunities.append((riasec_type, interest, confidence))
    
    if alignments:
        st.success("✅ **Strong Alignment**")
        for riasec_type, interest, confidence in alignments:
            st.markdown(f"- **{riasec_type.capitalize()}**: Your interests ({interest:.0f}%) and skills ({confidence:.0f}%) are well-aligned")
    
    if gaps:
        st.warning("📈 **Development Opportunities**")
        for riasec_type, gap, interest, confidence in gaps:
            st.markdown(f"- **{riasec_type.capitalize()}**: High interest ({interest:.0f}%) but lower skill confidence ({confidence:.0f}%) - consider skill development")
    
    if opportunities:
        st.info("💡 **Hidden Strengths**")
        for riasec_type, interest, confidence in opportunities:
            st.markdown(f"- **{riasec_type.capitalize()}**: Strong skills ({confidence:.0f}%) with moderate interest ({interest:.0f}%) - explore new applications")
    
    # Top skills breakdown
    st.markdown("### Your Top Skills:")
    if st.session_state.skills_confidence:
        top_skills = sorted(st.session_state.skills_confidence.items(), key=lambda x: x[1], reverse=True)[:5]
        
        for skill, confidence in top_skills:
            col1, col2 = st.columns([3, 1])
            with col1:
                st.progress(confidence/100)
            with col2:
                st.caption(f"{skill}: {confidence}%")
    else:
        st.info("No skills data available. Please complete the skills assessment.")
    
    # Show unmapped skills if any
    if unmapped_skills:
        with st.expander("Skills with automatic categorization"):
            st.caption("These skills were automatically categorized based on keywords:")
            for skill in unmapped_skills:
                st.write(f"- {skill}")

def render_career_matches():
    """Render career recommendations"""
    st.subheader("🎯 Recommended Career Paths")
    
    # Check if assessment is complete
    if not st.session_state.get('riasec_scores') or not st.session_state.get('skills_confidence'):
        st.warning("Please complete the assessment first to view career recommendations.")
        return
    
    # Get AI-generated career recommendations if available
    openai_service = OpenAIService()
    
    user_profile = {
        'riasec_scores': st.session_state.riasec_scores,
        'skills_confidence': st.session_state.skills_confidence,
        'work_values': st.session_state.work_values
    }
    
    # Check if we have uploaded frameworks
    uploaded_frameworks = st.session_state.get('uploaded_frameworks', {})
    
    # Generate AI recommendations
    with st.spinner("Generating personalized career recommendations..."):
        ai_recommendations = openai_service.generate_career_recommendations(
            user_profile, 
            uploaded_frameworks
        )
    
    # Store in session state
    st.session_state.career_recommendations = ai_recommendations
    
    # Display AI recommendations if available
    if ai_recommendations:
        st.markdown("### AI-Powered Career Recommendations")
        st.caption("Based on your assessment results and any uploaded skill frameworks")
        
        for i, career in enumerate(ai_recommendations[:5]):
            with st.expander(f"{i+1}. {career['title']} - {career['match_score']}% Match", expanded=(i==0)):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Description:** {career['description']}")
                    
                    if career.get('activities'):
                        st.markdown("**Key Activities:**")
                        for activity in career['activities'][:4]:
                            st.markdown(f"  • {activity}")
                    
                    if career.get('skills_to_develop'):
                        st.markdown("**Skills to Develop:**")
                        for skill in career['skills_to_develop'][:3]:
                            st.markdown(f"  • {skill}")
                
                with col2:
                    st.metric("Match Score", f"{career['match_score']}%")
                    
                    # Visual match indicator
                    if career['match_score'] >= 80:
                        st.success("Excellent Match")
                    elif career['match_score'] >= 70:
                        st.info("Good Match")
                    else:
                        st.warning("Moderate Match")
                
                if career.get('next_steps'):
                    st.markdown("**Next Steps:**")
                    for j, step in enumerate(career['next_steps'][:4], 1):
                        st.markdown(f"{j}. {step}")
    
    # Also show traditional career matches
    st.markdown("### Additional Career Matches")
    st.caption("Based on standard RIASEC career matching")
    
    careers = match_careers(
        st.session_state.riasec_scores,
        st.session_state.skills_confidence,
        st.session_state.work_values
    )
    
    # Display traditional matches
    for i, career in enumerate(careers[:3]):
        with st.expander(f"{career['title']} - {career['match_score']}% Match"):
            col1, col2 = st.columns([2, 1])
            
            with col1:
                st.markdown(f"**Description:** {career['description']}")
                st.markdown(f"**Required Skills:** {', '.join(career['required_skills'])}")
                st.markdown(f"**Work Environment:** {', '.join(career['work_environment'])}")
            
            with col2:
                st.metric("Match Score", f"{career['match_score']}%")
                st.markdown(f"**Salary Range:** {career['salary_range']}")
                st.markdown(f"**Growth:** {career['growth_outlook']}")

def render_development_plan():
    """Render personalized development plan"""
    st.subheader("📚 Your Personalized Development Plan")
    
    # Check if assessment is complete
    if not st.session_state.get('riasec_scores') or not st.session_state.get('skills_confidence'):
        st.warning("Please complete the assessment first to view your development plan.")
        return
    
    # Get AI-generated recommendations if API key is available
    openai_service = OpenAIService()
    
    user_profile = {
        'riasec_scores': st.session_state.riasec_scores,
        'skills_confidence': st.session_state.skills_confidence,
        'work_values': st.session_state.work_values
    }
    
    # Use career recommendations from previous tab if available
    career_recommendations = st.session_state.get('career_recommendations', [])
    
    if career_recommendations:
        st.markdown("### Based on Your Top Career Matches")
        
        # Aggregate skills to develop from all recommendations
        all_skills_to_develop = set()
        for career in career_recommendations[:3]:
            if career.get('skills_to_develop'):
                all_skills_to_develop.update(career['skills_to_develop'])
        
        if all_skills_to_develop:
            st.markdown("#### Priority Skills to Develop:")
            
            # Categorize skills
            technical_skills = []
            soft_skills = []
            
            for skill in all_skills_to_develop:
                if any(word in skill.lower() for word in ['technical', 'programming', 'software', 'data', 'analysis', 'tools']):
                    technical_skills.append(skill)
                else:
                    soft_skills.append(skill)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Technical Skills:**")
                for skill in technical_skills[:5]:
                    st.markdown(f"• {skill}")
            
            with col2:
                st.markdown("**Professional Skills:**")
                for skill in soft_skills[:5]:
                    st.markdown(f"• {skill}")
    
    # Skill gap analysis
    st.markdown("### Skill Gap Analysis")
    
    # Identify skills below 70% confidence
    skills_to_improve = [(skill, conf) for skill, conf in st.session_state.skills_confidence.items() if conf < 70]
    
    if skills_to_improve:
        st.markdown("**Focus Areas for Improvement:**")
        
        # Sort by confidence (lowest first)
        skills_to_improve.sort(key=lambda x: x[1])
        
        for skill, current_level in skills_to_improve[:5]:
            col1, col2, col3, col4 = st.columns([2, 1, 1, 1])
            with col1:
                st.markdown(f"**{skill}**")
            with col2:
                st.caption(f"Current: {current_level}%")
            with col3:
                st.caption("Target: 80%")
            with col4:
                improvement_needed = 80 - current_level
                st.caption(f"Gap: {improvement_needed}%")
    
    # Work values alignment
    st.markdown("### Work Environment Priorities")
    st.markdown("Based on your values, prioritize opportunities that offer:")
    
    values_col1, values_col2 = st.columns(2)
    
    work_values = st.session_state.get('work_values', [])
    if work_values:
        with values_col1:
            for i, value in enumerate(work_values[:3]):
                st.markdown(f"{i+1}. **{value}**")
        
        with values_col2:
            for i, value in enumerate(work_values[3:6], 4):
                st.markdown(f"{i}. **{value}**")
    else:
        st.info("Complete the work values assessment to see your priorities.")
    
    # Action steps with timeline
    st.markdown("### Development Timeline")
    
    timeline_tab1, timeline_tab2, timeline_tab3 = st.tabs(["Next 30 Days", "3-6 Months", "6-12 Months"])
    
    with timeline_tab1:
        st.markdown("**Immediate Actions:**")
        st.markdown("✓ Update resume highlighting your top skills and RIASEC alignment")
        st.markdown("✓ Research your top 3 career matches in detail")
        st.markdown("✓ Join 2-3 professional communities in your areas of interest")
        st.markdown("✓ Schedule informational interviews with professionals in target roles")
        st.markdown("✓ Create a learning plan for your top skill gaps")
    
    with timeline_tab2:
        st.markdown("**Short-term Goals:**")
        st.markdown("📚 Complete 1-2 online courses for priority skills")
        st.markdown("🤝 Build network with 20+ professionals in target field")
        st.markdown("💼 Gain practical experience through projects or volunteering")
        st.markdown("📊 Create portfolio showcasing relevant skills")
        st.markdown("🎯 Apply for 5-10 positions aligned with your profile")
    
    with timeline_tab3:
        st.markdown("**Long-term Objectives:**")
        st.markdown("🚀 Transition to role aligned with top RIASEC types")
        st.markdown("📈 Achieve 80%+ confidence in all key skills")
        st.markdown("🌟 Establish yourself in your chosen career path")
        st.markdown("👥 Become a mentor to others in your field")
        st.markdown("🎓 Consider advanced certifications or education")
    
    # Resources section
    st.markdown("### Recommended Resources")
    
    resource_col1, resource_col2 = st.columns(2)
    
    with resource_col1:
        st.markdown("**Online Learning Platforms:**")
        st.markdown("• Coursera - University courses")
        st.markdown("• LinkedIn Learning - Professional skills")
        st.markdown("• Udemy - Technical skills")
        st.markdown("• edX - Academic programs")
    
    with resource_col2:
        st.markdown("**Professional Development:**")
        st.markdown("• Industry associations")
        st.markdown("• Local meetup groups")
        st.markdown("• Online communities (Reddit, Discord)")
        st.markdown("• Professional conferences")
    
    # Download and coaching buttons
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("📥 Download Full Report", use_container_width=True):
            st.info("Report generation feature coming soon!")
        
        if st.button("💬 Get Personalized Coaching", use_container_width=True):
            st.session_state.current_step = 'coaching'
            st.rerun()
