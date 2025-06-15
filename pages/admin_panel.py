import streamlit as st
import json
import os

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
                        if key not in ['admin_authenticated', 'show_admin']:
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
        
        # Mock analytics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Assessments", "0")
        
        with col2:
            st.metric("Active Users", "0")
        
        with col3:
            st.metric("Completion Rate", "0%")
        
        st.info("Connect to a database to see real analytics")
    
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
