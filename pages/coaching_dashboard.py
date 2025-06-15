import streamlit as st
from data.coaching_questions import get_coaching_questions

def render():
    st.title("🎓 Career Coaching Dashboard")
    
    if st.session_state.selected_persona == 'individual':
        # Individual coaching view
        st.subheader("Personalized Coaching Questions")
        
        # Get primary RIASEC type
        sorted_types = sorted(st.session_state.riasec_scores.items(), key=lambda x: x[1], reverse=True)
        primary_type = sorted_types[0][0] if sorted_types else 'social'
        
        # Get coaching questions
        questions = get_coaching_questions(primary_type)
        
        st.info(f"Based on your {primary_type.capitalize()} personality type, here are some reflection questions:")
        
        for i, q in enumerate(questions[:5]):
            with st.expander(f"Question {i+1}: {q['question']}"):
                st.markdown(f"**Purpose:** {q['purpose']}")
                
                # Text area for response
                response = st.text_area(
                    "Your thoughts:",
                    key=f"coaching_response_{i}",
                    height=100
                )
                
                if q.get('followUp'):
                    st.markdown("**Follow-up questions:**")
                    for followup in q['followUp']:
                        st.markdown(f"• {followup}")
    
    else:
        # Coach view
        st.subheader("Coaching Tools & Resources")
        
        tab1, tab2, tab3 = st.tabs(["Question Bank", "Client Progress", "Resources"])
        
        with tab1:
            st.markdown("### RIASEC-Based Coaching Questions")
            
            riasec_types = ['realistic', 'investigative', 'artistic', 'social', 'enterprising', 'conventional']
            selected_type = st.selectbox("Select RIASEC Type", riasec_types)
            
            questions = get_coaching_questions(selected_type)
            
            for q in questions:
                with st.expander(q['question']):
                    st.markdown(f"**Category:** {q['category']}")
                    st.markdown(f"**Purpose:** {q['purpose']}")
                    if q.get('followUp'):
                        st.markdown("**Follow-up questions:**")
                        for followup in q['followUp']:
                            st.markdown(f"• {followup}")
        
        with tab2:
            st.info("Client progress tracking coming soon!")
        
        with tab3:
            st.markdown("""
            ### Coaching Resources
            
            - **RIASEC Model Guide**: Understanding Holland's career types
            - **Active Listening Techniques**: Building rapport with clients
            - **Goal Setting Framework**: SMART goals for career development
            - **Career Transition Strategies**: Supporting career changes
            """)
    
    # Back button
    if st.button("← Back to Results"):
        st.session_state.current_step = 'results'
        st.rerun()
