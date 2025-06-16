import streamlit as st
import json

def show_admin_panel():
    st.markdown("""
    <div style="text-align: center; padding: 20px;">
        <h1>🔧 Admin Panel</h1>
        <p style="font-size: 18px; color: #666;">Configure and manage the assessment tool</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Analytics", "📝 Content Management", "🔑 API Settings", "📤 Export Data"])
    
    with tab1:
        st.markdown("### Assessment Analytics")
        
        # Check if we have assessment data
        if st.session_state.assessment_history:
            # Get latest assessment data
            latest_riasec = None
            latest_skills = None
            latest_values = None
            
            for assessment in st.session_state.assessment_history:
                if assessment['type'] == 'riasec':
                    latest_riasec = assessment['data']
                elif assessment['type'] == 'skills':
                    latest_skills = assessment['data']
                elif assessment['type'] == 'values':
                    latest_values = assessment['data']
            
            # Display user info
            st.markdown("#### Current User Profile")
            st.markdown(f"**Name:** {st.session_state.user_profile.get('name', 'Not provided')}")
            st.markdown(f"**Completed Assessments:** {', '.join(st.session_state.user_profile.get('completedAssessments', []))}")
            
            # RIASEC Results
            if latest_riasec:
                st.markdown("#### RIASEC Assessment Results")
                for type_name, score in latest_riasec.items():
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.progress(score / 5)
                    with col2:
                        st.markdown(f"**{type_name.capitalize()}:** {score:.1f}/5")
            else:
                st.info("No RIASEC assessment data available yet")
            
            # Skills Results
            if latest_skills:
                st.markdown("#### Skills Confidence Summary")
                st.markdown(f"**Total skills assessed:** {len(latest_skills)}")
                avg_confidence = sum(latest_skills.values()) / len(latest_skills) if latest_skills else 0
                st.markdown(f"**Average confidence:** {avg_confidence:.1f}/5")
            else:
                st.info("No skills assessment data available yet")
            
            # Values Results
            if latest_values:
                st.markdown("#### Selected Work Values")
                for value in latest_values:
                    st.markdown(f"- {value}")
            else:
                st.info("No values assessment data available yet")
        else:
            st.info("No assessment data available. Complete an assessment to see analytics.")
    
    with tab2:
        st.markdown("### Content Management")
        
        content_type = st.selectbox(
            "Select content to manage:",
            ["RIASEC Questions", "Skills Categories", "Work Values", "Career Database", "Coaching Questions"]
        )
        
        if content_type == "RIASEC Questions":
            st.markdown("#### RIASEC Questions Configuration")
            st.info("Upload a JSON file with RIASEC questions or edit existing ones")
            
            uploaded_file = st.file_uploader("Upload RIASEC questions (JSON)", type="json")
            if uploaded_file:
                questions = json.load(uploaded_file)
                st.success(f"Loaded {len(questions)} questions")
                st.json(questions[:2])  # Show preview
        
        elif content_type == "Career Database":
            st.markdown("#### Career Database Management")
            st.info("Add or modify career paths in the database")
            
            with st.expander("Add New Career"):
                career_title = st.text_input("Career Title")
                career_desc = st.text_area("Description")
                primary_type = st.selectbox("Primary RIASEC Type", 
                    ["realistic", "investigative", "artistic", "social", "enterprising", "conventional"])
                
                if st.button("Add Career"):
                    st.success(f"Career '{career_title}' added successfully!")
    
    with tab3:
        st.markdown("### API Configuration")
        
        st.markdown("#### OpenAI API Settings")
        api_key = st.text_input("OpenAI API Key", type="password", placeholder="sk-...")
        
        if st.button("Save API Key"):
            st.success("API Key saved successfully!")
        
        st.markdown("#### API Usage Statistics")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Requests", "0")
        with col2:
            st.metric("Tokens Used", "0")
        with col3:
            st.metric("Cost", "$0.00")
    
    with tab4:
        st.markdown("### Export Assessment Data")
        
        export_format = st.radio("Select export format:", ["CSV", "JSON", "PDF Report"])
        
        if st.button("Export Data"):
            if export_format == "JSON":
                data = {
                    "user_profile": st.session_state.user_profile,
                    "assessment_history": st.session_state.assessment_history,
                    "recommended_careers": st.session_state.recommended_careers
                }
                st.download_button(
                    label="Download JSON",
                    data=json.dumps(data, indent=2),
                    file_name="assessment_data.json",
                    mime="application/json"
                )
            else:
                st.info(f"{export_format} export coming soon!")
    
    st.markdown("---")
    
    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("← Back to Home", use_container_width=True):
            st.session_state.current_step = 'persona'
            st.rerun()
    
    with col2:
        if st.button("🚪 Logout", use_container_width=True):
            from utils.simple_auth import logout
            logout()
            st.rerun()
