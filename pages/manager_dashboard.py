import streamlit as st

def show_manager_dashboard():
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1>👔 Manager Dashboard</h1>
        <p style="font-size: 18px; color: #666;">Team development insights and tools</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Team member profile summary
    st.markdown("### Team Member Profile Summary")
    st.markdown(f"**Name:** {st.session_state.user_profile['name']}")
    
    # RIASEC summary
    top_types = sorted(
        st.session_state.user_profile['riasecScores'].items(), 
        key=lambda x: x[1], 
        reverse=True
    )[:3]
    
    st.markdown("**Top Interest Areas:**")
    for type_name, score in top_types:
        st.markdown(f"- {type_name.capitalize()}: {score:.1f}/5")
    
    # Key strengths
    st.markdown("**Key Strengths:**")
    top_skills = sorted(
        st.session_state.user_profile['skillsConfidence'].items(),
        key=lambda x: x[1],
        reverse=True
    )[:5]
    
    for skill, confidence in top_skills:
        st.markdown(f"- {skill}: {confidence}/5")
    
    st.markdown("---")
    
    # Development recommendations
    st.markdown("### Development Recommendations")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        **🎯 Role Alignment**
        - Consider projects that leverage their top interests
        - Assign tasks that match their skill strengths
        - Provide opportunities for growth in areas of interest
        """)
    
    with col2:
        st.markdown("""
        **📈 Career Development**
        - Discuss career aspirations regularly
        - Create individual development plans
        - Identify mentorship opportunities
        - Support skill-building initiatives
        """)
    
    st.markdown("---")
    
    # Team insights
    st.markdown("### Team Development Strategies")
    
    strategies = {
        'realistic': "Provide hands-on projects and practical problem-solving opportunities",
        'investigative': "Encourage research projects and analytical challenges",
        'artistic': "Foster creative initiatives and innovation projects",
        'social': "Create collaborative projects and mentoring opportunities",
        'enterprising': "Offer leadership roles and business development tasks",
        'conventional': "Assign process improvement and organizational projects"
    }
    
    top_type = top_types[0][0]
    st.info(f"**Recommended strategy:** {strategies.get(top_type, 'Customize based on individual interests')}")
    
    st.markdown("---")
    
    # Reflection questions
    st.markdown("### Manager Reflection Questions")
    
    questions = [
        "How can I better align this team member's role with their interests?",
        "What development opportunities would benefit both the individual and the team?",
        "How can I leverage their strengths in upcoming projects?",
        "What support do they need to reach their career goals?"
    ]
    
    for i, question in enumerate(questions):
        st.text_area(
            question,
            key=f"manager_reflection_{i}",
            placeholder="Your thoughts..."
        )
    
    st.markdown("---")
    
    # Navigation
    if st.button("🔄 Start New Assessment", use_container_width=True):
        # Reset session state
        for key in ['user_profile', 'riasec_answers', 'skills_answers', 
                   'selected_values', 'recommended_careers', 'game_progress']:
            if key in st.session_state:
                del st.session_state[key]
        st.session_state.current_step = 'persona'
        st.rerun()
