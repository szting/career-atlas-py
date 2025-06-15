import streamlit as st

def render():
    st.title("💎 Work Values Assessment")
    st.markdown("Select the work values that are most important to you (choose up to 10)")
    
    # Work values options
    all_values = [
        "Work-Life Balance",
        "Job Security",
        "High Salary",
        "Career Growth",
        "Learning Opportunities",
        "Flexibility",
        "Remote Work",
        "Teamwork",
        "Independence",
        "Leadership Opportunities",
        "Recognition",
        "Helping Others",
        "Creativity",
        "Innovation",
        "Stability",
        "Challenge",
        "Variety",
        "Travel Opportunities",
        "Social Impact",
        "Prestige",
        "Autonomy",
        "Structured Environment",
        "Fast-Paced Environment",
        "Work with Latest Technology",
        "Mentorship",
        "Company Culture",
        "Benefits Package",
        "Location",
        "Small Company",
        "Large Corporation"
    ]
    
    # Initialize selected values
    if 'temp_values' not in st.session_state:
        st.session_state.temp_values = st.session_state.work_values.copy() if st.session_state.work_values else []
    
    # Display values in columns
    st.markdown(f"**Selected: {len(st.session_state.temp_values)}/10**")
    
    # Create value selection grid
    cols = st.columns(3)
    for i, value in enumerate(all_values):
        with cols[i % 3]:
            if st.checkbox(
                value,
                value=value in st.session_state.temp_values,
                key=f"value_{value}",
                disabled=len(st.session_state.temp_values) >= 10 and value not in st.session_state.temp_values
            ):
                if value not in st.session_state.temp_values:
                    st.session_state.temp_values.append(value)
            else:
                if value in st.session_state.temp_values:
                    st.session_state.temp_values.remove(value)
    
    # Show selected values summary
    if st.session_state.temp_values:
        st.markdown("---")
        st.subheader("Your Selected Values:")
        
        # Categorize values
        categories = {
            "Lifestyle": ["Work-Life Balance", "Flexibility", "Remote Work", "Location", "Travel Opportunities"],
            "Security": ["Job Security", "Stability", "Benefits Package", "Structured Environment"],
            "Growth": ["Career Growth", "Learning Opportunities", "Leadership Opportunities", "Mentorship", "Challenge"],
            "Rewards": ["High Salary", "Recognition", "Prestige"],
            "Purpose": ["Helping Others", "Social Impact", "Creativity", "Innovation"],
            "Environment": ["Teamwork", "Independence", "Autonomy", "Company Culture", "Small Company", "Large Corporation", "Fast-Paced Environment", "Work with Latest Technology", "Variety"]
        }
        
        categorized_values = {}
        for category, values in categories.items():
            selected_in_category = [v for v in st.session_state.temp_values if v in values]
            if selected_in_category:
                categorized_values[category] = selected_in_category
        
        cols = st.columns(len(categorized_values))
        for i, (category, values) in enumerate(categorized_values.items()):
            with cols[i]:
                st.markdown(f"**{category}:**")
                for value in values:
                    st.markdown(f"• {value}")
    
    # Navigation
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.button("← Back", use_container_width=True):
            st.session_state.current_step = 'skills'
            st.session_state.game_progress = 40
            st.rerun()
    
    with col3:
        if st.button("Complete Assessment →", 
                    disabled=len(st.session_state.temp_values) < 5,
                    use_container_width=True):
            st.session_state.work_values = st.session_state.temp_values.copy()
            del st.session_state.temp_values
            st.session_state.current_step = 'results'
            st.session_state.game_progress = 100
            st.rerun()
    
    if len(st.session_state.temp_values) < 5:
        st.warning("Please select at least 5 values to continue.")
