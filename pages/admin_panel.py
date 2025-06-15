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
        
        # Check for assessment data in session state
        has_assessment_data = False
        
        # Check if any assessment has been completed
        if (st.session_state.get('riasec_scores') and 
            any(score > 0 for score in st.session_state.riasec_scores.values())):
            has_assessment_data = True
        
        # Calculate metrics
        total_assessments = 1 if has_assessment_data else 0
        active_users = 1 if st.session_state.get('authenticated') else 0
        
        # Calculate completion rate based on actual progress
        completion_rate = 0
        if has_assessment_data:
            steps_completed = 0
            if any(score > 0 for score in st.session_state.get('riasec_scores', {}).values()):
                steps_completed += 1
            if st.session_state.get('skills_confidence'):
                steps_completed += 1
            if st.session_state.get('work_values'):
                steps_completed += 1
            completion_rate = (steps_completed / 3) * 100
        
        # Display metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Assessments", total_assessments)
        
        with col2:
            st.metric("Active Users", active_users)
        
        with col3:
            st.metric("Completion Rate", f"{completion_rate:.0f}%")
        
        # Show current session data if available
        if has_assessment_data:
            st.markdown("### Current Session Assessment Data")
            st.info("Note: This shows data from the current active session. In production, this would aggregate data from all users.")
            
            # RIASEC Results
            if st.session_state.get('riasec_scores'):
                st.markdown("#### RIASEC Assessment Results")
                
                riasec_data = st.session_state.riasec_scores
                
                # Create two columns for better display
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**RIASEC Scores:**")
                    for riasec_type, score in riasec_data.items():
                        # Show actual score value
                        st.write(f"• **{riasec_type.capitalize()}**: {score:.1f}/5")
                        # Progress bar
                        st.progress(score / 5)
                
                with col2:
                    # Show top 3 types
                    sorted_types = sorted(riasec_data.items(), key=lambda x: x[1], reverse=True)
                    st.markdown("**Top Interest Areas:**")
                    for i, (riasec_type, score) in enumerate(sorted_types[:3], 1):
                        if score > 0:  # Only show if there's a score
                            st.write(f"{i}. **{riasec_type.capitalize()}**: {score:.1f}/5")
                            # Add description
                            descriptions = {
                                'realistic': "Hands-on, practical activities",
                                'investigative': "Research and analytical work",
                                'artistic': "Creative and innovative tasks",
                                'social': "Helping and teaching others",
                                'enterprising': "Leadership and business",
                                'conventional': "Organized, structured work"
                            }
                            st.caption(descriptions.get(riasec_type, ""))
            
            # Assessment Progress Details
            st.markdown("#### Assessment Progress Details")
            
            progress_data = {
                "RIASEC Assessment": "✅ Complete" if any(score > 0 for score in st.session_state.get('riasec_scores', {}).values()) else "❌ Incomplete",
                "Skills Assessment": "✅ Complete" if st.session_state.get('skills_confidence') else "❌ Incomplete", 
                "Values Assessment": "✅ Complete" if st.session_state.get('work_values') else "❌ Incomplete"
            }
            
            progress_col1, progress_col2, progress_col3 = st.columns(3)
            
            with progress_col1:
                st.metric("RIASEC", progress_data["RIASEC Assessment"])
            
            with progress_col2:
                st.metric("Skills", progress_data["Skills Assessment"])
            
            with progress_col3:
                st.metric("Values", progress_data["Values Assessment"])
            
            # Skills Summary
            if st.session_state.get('skills_confidence'):
                st.markdown("#### Skills Confidence Summary")
                skills_data = st.session_state.skills_confidence
                
                if skills_data:
                    avg_confidence = sum(skills_data.values()) / len(skills_data)
                    st.metric("Average Skills Confidence", f"{avg_confidence:.1f}%")
                    
                    # Show top 5 skills
                    top_skills = sorted(skills_data.items(), key=lambda x: x[1], reverse=True)[:5]
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Top 5 Skills:**")
                        for skill, confidence in top_skills:
                            st.write(f"• {skill}: {confidence}%")
                            st.progress(confidence / 100)
                    
                    with col2:
                        # Skills by category
                        st.markdown("**Skills Count by Category:**")
                        # This is a simplified categorization
                        technical_count = sum(1 for skill in skills_data.keys() if any(word in skill.lower() for word in ['technical', 'computer', 'data']))
                        soft_count = sum(1 for skill in skills_data.keys() if any(word in skill.lower() for word in ['communication', 'leadership', 'team']))
                        other_count = len(skills_data) - technical_count - soft_count
                        
                        st.write(f"• Technical Skills: {technical_count}")
                        st.write(f"• Soft Skills: {soft_count}")
                        st.write(f"• Other Skills: {other_count}")
            
            # Work Values
            if st.session_state.get('work_values'):
                st.markdown("#### Work Values")
                values = st.session_state.work_values
                st.write("**Selected Values:**")
                
                values_cols = st.columns(2)
                for i, value in enumerate(values):
                    with values_cols[i % 2]:
                        st.write(f"• {value}")
            
            # User Information
            if st.session_state.get('user_name') or st.session_state.get('user_email'):
                st.markdown("#### User Information")
                if st.session_state.get('user_name'):
                    st.write(f"**Name:** {st.session_state.user_name}")
                if st.session_state.get('user_email'):
                    st.write(f"**Email:** {st.session_state.user_email}")
                if st.session_state.get('selected_persona'):
                    st.write(f"**Persona:** {st.session_state.selected_persona.capitalize()}")
        else:
            st.info("No assessment data available yet. Complete an assessment to see analytics.")
            st.markdown("""
            To see analytics data:
            1. Log out from the admin panel
            2. Complete an assessment as an individual
            3. Return to the admin panel to view the results
            
            Note: In a production environment, this would show aggregated data from all users.
            """)
    
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
