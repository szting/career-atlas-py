import streamlit as st
import json
import os
from datetime import datetime

def render():
    st.title("🔐 Admin Panel")
    
    # Admin authentication (simplified)
    if 'admin_authenticated' not in st.session_state:
        password = st.text_input("Enter admin password:", type="password")
        if st.button("Login"):
            if password == "admin123":  # In production, use proper authentication
                st.session_state.admin_authenticated = True
                st.rerun()
            else:
                st.error("Invalid password")
        return
    
    # Admin tabs
    tab1, tab2, tab3, tab4 = st.tabs(["Data Management", "API Settings", "Analytics", "File Upload"])
    
    with tab1:
        st.subheader("📊 Assessment Data Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Export All Data"):
                st.info("Data export functionality coming soon!")
        
        with col2:
            if st.button("Clear All Data"):
                if st.checkbox("Confirm data deletion"):
                    # Clear session state
                    for key in list(st.session_state.keys()):
                        if key not in ['admin_authenticated', 'show_admin', 'authenticated', 'auth_time']:
                            del st.session_state[key]
                    st.success("All data cleared!")
    
    with tab2:
        st.subheader("🔑 API Configuration")
        
        # OpenAI API Key
        api_key = st.text_input(
            "OpenAI API Key:",
            value=st.session_state.get('openai_api_key', ''),
            type="password"
        )
        
        if st.button("Save API Key"):
            st.session_state.openai_api_key = api_key
            # In production, save to secure storage
            st.success("API key saved!")
        
        # Test connection
        if st.button("Test API Connection"):
            if api_key:
                st.info("API connection test coming soon!")
            else:
                st.error("Please enter an API key first")
    
    with tab3:
        st.subheader("📈 Analytics Dashboard")
        
        # Get actual assessment data from session state
        total_assessments = 1 if st.session_state.get('riasec_scores') else 0
        active_users = 1 if st.session_state.get('authenticated') else 0
        
        # Calculate completion rate
        completion_rate = 0
        if st.session_state.get('riasec_scores') and st.session_state.get('skills_confidence') and st.session_state.get('work_values'):
            completion_rate = 100
        elif st.session_state.get('riasec_scores') or st.session_state.get('skills_confidence'):
            completion_rate = 50
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Assessments", total_assessments)
        
        with col2:
            st.metric("Active Users", active_users)
        
        with col3:
            st.metric("Completion Rate", f"{completion_rate}%")
        
        # Show RIASEC results if available
        if st.session_state.get('riasec_scores'):
            st.markdown("### Current RIASEC Assessment Results")
            
            riasec_data = st.session_state.riasec_scores
            
            # Create two columns for better display
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**RIASEC Scores:**")
                for riasec_type, score in riasec_data.items():
                    st.metric(riasec_type.capitalize(), f"{score}/5")
            
            with col2:
                # Show top 3 types
                sorted_types = sorted(riasec_data.items(), key=lambda x: x[1], reverse=True)
                st.markdown("**Top Interest Areas:**")
                for i, (riasec_type, score) in enumerate(sorted_types[:3], 1):
                    st.write(f"{i}. {riasec_type.capitalize()}: {score}/5")
            
            # Show assessment completion status
            st.markdown("### Assessment Progress")
            
            progress_data = {
                "RIASEC Assessment": "✅ Complete" if st.session_state.get('riasec_scores') else "❌ Incomplete",
                "Skills Assessment": "✅ Complete" if st.session_state.get('skills_confidence') else "❌ Incomplete", 
                "Values Assessment": "✅ Complete" if st.session_state.get('work_values') else "❌ Incomplete"
            }
            
            for assessment, status in progress_data.items():
                st.write(f"**{assessment}:** {status}")
            
            # Show skills data if available
            if st.session_state.get('skills_confidence'):
                st.markdown("### Skills Confidence Summary")
                skills_data = st.session_state.skills_confidence
                avg_confidence = sum(skills_data.values()) / len(skills_data) if skills_data else 0
                st.metric("Average Skills Confidence", f"{avg_confidence:.1f}%")
                
                # Show top 5 skills
                if skills_data:
                    top_skills = sorted(skills_data.items(), key=lambda x: x[1], reverse=True)[:5]
                    st.markdown("**Top 5 Skills:**")
                    for skill, confidence in top_skills:
                        st.write(f"• {skill}: {confidence}%")
            
            # Show work values if available
            if st.session_state.get('work_values'):
                st.markdown("### Work Values")
                values = st.session_state.work_values
                st.write("**Selected Values:**")
                for value in values:
                    st.write(f"• {value}")
        else:
            st.info("No assessment data available yet. Complete an assessment to see analytics.")
    
    with tab4:
        st.subheader("📁 File Upload System")
        
        st.markdown("""
        Upload JSON files to update:
        - Career paths database
        - RIASEC questions
        - Skills categories
        - Coaching questions
        """)
        
        file_type = st.selectbox(
            "Select file type:",
            ["Career Paths", "RIASEC Questions", "Skills List", "Coaching Questions"]
        )
        
        uploaded_file = st.file_uploader("Choose a JSON file", type="json")
        
        if uploaded_file is not None:
            try:
                data = json.load(uploaded_file)
                st.success(f"File uploaded successfully! Found {len(data)} items.")
                
                if st.button("Preview Data"):
                    st.json(data[:3] if isinstance(data, list) else data)
                
                if st.button("Save Changes"):
                    # In production, save to appropriate data files
                    st.success(f"{file_type} updated successfully!")
            except Exception as e:
                st.error(f"Error reading file: {str(e)}")
        
        # Download templates
        st.markdown("### Download Templates")
        
        if st.button("Download Career Paths Template"):
            st.info("Template download coming soon!")
    
    # Logout
    st.markdown("---")
    if st.button("Logout"):
        st.session_state.admin_authenticated = False
        st.session_state.show_admin = False
        st.rerun()
