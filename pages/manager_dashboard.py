import streamlit as st

def render():
    st.title("👔 Manager Dashboard")
    st.subheader("Team Development Insights")
    
    tab1, tab2, tab3 = st.tabs(["Team Overview", "Development Planning", "Reflection Questions"])
    
    with tab1:
        st.markdown("""
        ### Team RIASEC Distribution
        
        Understanding your team's personality types helps in:
        - Task allocation
        - Team composition
        - Communication strategies
        - Development planning
        """)
        
        # Mock team data
        st.info("Connect your team's assessment data to see insights here.")
    
    with tab2:
        st.markdown("""
        ### Career Development Planning
        
        Use these strategies to support your team:
        
        1. **Individual Development Plans (IDPs)**
           - Align with RIASEC profiles
           - Focus on strength development
           - Address skill gaps
        
        2. **Team Composition Analysis**
           - Balance different personality types
           - Create complementary teams
           - Leverage diverse strengths
        
        3. **Growth Opportunities**
           - Match projects to interests
           - Provide stretch assignments
           - Enable cross-functional exposure
        """)
    
    with tab3:
        st.markdown("### Manager Reflection Questions")
        
        reflection_questions = [
            {
                'category': 'Team Understanding',
                'questions': [
                    "How well do I understand each team member's career aspirations?",
                    "What unique strengths does each person bring to the team?",
                    "How can I better support individual growth paths?"
                ]
            },
            {
                'category': 'Development Support',
                'questions': [
                    "Am I providing enough growth opportunities for each personality type?",
                    "How can I tailor my management style to different RIASEC types?",
                    "What resources can I provide to support career development?"
                ]
            },
            {
                'category': 'Team Dynamics',
                'questions': [
                    "How can I leverage personality diversity for better team outcomes?",
                    "What team activities would engage all personality types?",
                    "How can I improve communication across different working styles?"
                ]
            }
        ]
        
        for category in reflection_questions:
            with st.expander(category['category']):
                for q in category['questions']:
                    st.markdown(f"• {q}")
                    st.text_area("Your reflection:", key=f"reflection_{q[:20]}", height=80)
    
    # Resources
    st.markdown("---")
    st.subheader("📚 Manager Resources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Guides & Templates**
        - IDP Template
        - 1-on-1 Discussion Guide
        - Career Conversation Starters
        """)
    
    with col2:
        st.markdown("""
        **Training Materials**
        - Understanding RIASEC Types
        - Coaching Conversations
        - Team Development Strategies
        """)
