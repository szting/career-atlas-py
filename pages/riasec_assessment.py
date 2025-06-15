import streamlit as st

def render():
    st.title("🎯 RIASEC Interest Assessment")
    st.markdown("Rate how much you enjoy each activity on a scale of 1-5")
    
    # RIASEC questions
    questions = {
        'realistic': [
            "Working with tools or machinery",
            "Building or fixing things with your hands",
            "Working outdoors or with nature",
            "Operating equipment or vehicles",
            "Working with plants or animals"
        ],
        'investigative': [
            "Solving complex problems",
            "Conducting research or experiments",
            "Analyzing data or information",
            "Learning about scientific theories",
            "Working with abstract ideas"
        ],
        'artistic': [
            "Creating original work (art, music, writing)",
            "Expressing yourself creatively",
            "Designing visual layouts or graphics",
            "Performing for an audience",
            "Working in unstructured environments"
        ],
        'social': [
            "Helping others solve problems",
            "Teaching or training people",
            "Working in teams",
            "Counseling or advising others",
            "Organizing community activities"
        ],
        'enterprising': [
            "Leading projects or teams",
            "Persuading or influencing others",
            "Making business decisions",
            "Taking calculated risks",
            "Selling products or ideas"
        ],
        'conventional': [
            "Organizing files and records",
            "Following established procedures",
            "Working with numbers and data",
            "Maintaining accurate records",
            "Creating systems and processes"
        ]
    }
    
    # Initialize scores if not exists
    if 'temp_riasec_scores' not in st.session_state:
        st.session_state.temp_riasec_scores = {k: [] for k in questions.keys()}
    
    # Display questions by category
    for category, category_questions in questions.items():
        st.subheader(f"{category.capitalize()} Activities")
        
        cols = st.columns(5)
        for i, question in enumerate(category_questions):
            st.markdown(f"**{question}**")
            
            # Create radio buttons in columns
            selected = None
            for j, col in enumerate(cols):
                with col:
                    if st.button(
                        str(j+1),
                        key=f"{category}_{i}_{j+1}",
                        use_container_width=True,
                        type="secondary" if f"{category}_{i}" not in st.session_state else (
                            "primary" if st.session_state.get(f"{category}_{i}") == j+1 else "secondary"
                        )
                    ):
                        st.session_state[f"{category}_{i}"] = j+1
                        st.rerun()
            
            # Show scale labels
            if i == 0:
                col1, col2, col3, col4, col5 = st.columns(5)
                with col1:
                    st.caption("Strongly Dislike")
                with col5:
                    st.caption("Strongly Enjoy")
            
            st.markdown("---")
    
    # Check if all questions answered
    all_answered = True
    for category in questions:
        for i in range(len(questions[category])):
            if f"{category}_{i}" not in st.session_state:
                all_answered = False
                break
    
    # Navigation
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col3:
        if st.button("Next →", disabled=not all_answered, use_container_width=True):
            # Calculate scores
            for category in questions:
                scores = []
                for i in range(len(questions[category])):
                    scores.append(st.session_state.get(f"{category}_{i}", 3))
                st.session_state.riasec_scores[category] = sum(scores) / len(scores)
            
            # Clear temporary scores
            for category in questions:
                for i in range(len(questions[category])):
                    if f"{category}_{i}" in st.session_state:
                        del st.session_state[f"{category}_{i}"]
            
            st.session_state.current_step = 'skills'
            st.session_state.game_progress = 40
            st.rerun()
    
    if not all_answered:
        st.warning("Please answer all questions before proceeding.")
