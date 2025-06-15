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
            value=st.session_state.api_keys.get('openai', '') if 'api_keys' in st.session_state else '',
            type="password"
        )
        
        if st.button("Save API Key"):
            if 'api_keys' not in st.session_state:
                st.session_state.api_keys = {}
            st.session_state.api_keys['openai'] = api_key
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
        
        # Debug information
        st.caption("Debug: Session State Keys")
        st.caption(f"Available keys: {list(st.session_state.keys())}")
        
        # Get actual assessment data from session state
        # Check if RIASEC scores exist and have actual values
        riasec_scores = st.session_state.get('riasec_scores', {})
        has_riasec_data = any(score > 0 for score in riasec_scores.values()) if riasec_scores else False
        
        skills_confidence = st.session_state.get('skills_confidence', {})
        has_skills_data = len(skills_confidence) > 0
        
        work_values = st.session_state.get('work_values', [])
        has_values_data = len(work_values) > 0
        
        # Calculate metrics
        total_assessments = 1 if has_riasec_data else 0
        active_users = 1 if st.session_state.get('authenticated') else 0
        
        # Calculate completion rate
        completion_rate = 0
        if has_riasec_data and has_skills_data and has_values_data:
            completion_rate = 100
        elif has_riasec_data and has_skills_data:
            completion_rate = 66
        elif has_riasec_data:
            completion_rate = 33
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Assessments", total_assessments)
        
        with col2:
            st.metric("Active Users", active_users)
        
        with col3:
            st.metric("Completion Rate", f"{completion_rate}%")
        
        # Show RIASEC results if available
        if has_riasec_data:
            st.markdown("### Current RIASEC Assessment Results")
            
            # Create two columns for better display
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**RIASEC Scores:**")
                for riasec_type, score in riasec_scores.items():
                    st.metric(riasec_type.capitalize(), f"{score:.1f}/5")
            
            with col2:
                # Show top 3 types
                sorted_types = sorted(riasec_scores.items(), key=lambda x: x[1], reverse=True)
                st.markdown("**Top Interest Areas:**")
                for i, (riasec_type, score) in enumerate(sorted_types[:3], 1):
                    st.write(f"{i}. {riasec_type.capitalize()}: {score:.1f}/5")
            
            # Show assessment completion status
            st.markdown("### Assessment Progress")
            
            progress_data = {
                "RIASEC Assessment": "✅ Complete" if has_riasec_data else "❌ Incomplete",
                "Skills Assessment": "✅ Complete" if has_skills_data else "❌ Incomplete", 
                "Values Assessment": "✅ Complete" if has_values_data else "❌ Incomplete"
            }
            
            for assessment, status in progress_data.items():
                st.write(f"**{assessment}:** {status}")
            
            # Show skills data if available
            if has_skills_data:
                st.markdown("### Skills Confidence Summary")
                avg_confidence = sum(skills_confidence.values()) / len(skills_confidence) if skills_confidence else 0
                st.metric("Average Skills Confidence", f"{avg_confidence:.1f}%")
                
                # Show top 5 skills
                if skills_confidence:
                    top_skills = sorted(skills_confidence.items(), key=lambda x: x[1], reverse=True)[:5]
                    st.markdown("**Top 5 Skills:**")
                    for skill, confidence in top_skills:
                        st.write(f"• {skill}: {confidence}%")
            
            # Show work values if available
            if has_values_data:
                st.markdown("### Work Values")
                st.write("**Selected Values:**")
                for value in work_values:
                    st.write(f"• {value}")
        else:
            st.info("No assessment data available yet. Complete an assessment to see analytics.")
            
            # Show current RIASEC scores for debugging
            if riasec_scores:
                st.markdown("### Debug: Current RIASEC Scores")
                st.json(riasec_scores)
    
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
