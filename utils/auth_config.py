import streamlit as st
import bcrypt

def get_auth_config():
    """Get authentication configuration from Streamlit secrets or environment"""
    
    # Default password hash for 'admin123'
    default_password_hash = "$2b$12$iWXWlWvKgFrCVaWsgR2MUOtYm8ByLpUEaKJsL5V2gY9nqMjJ5b5Hy"
    
    # Try to get from Streamlit secrets first
    try:
        password_hash = st.secrets.get("passwords", {}).get("admin", default_password_hash)
        cookie_name = st.secrets.get("auth", {}).get("cookie_name", "career_assessment_cookie")
        cookie_key = st.secrets.get("auth", {}).get("cookie_key", "random_signature_key_123")
        cookie_expiry_days = st.secrets.get("auth", {}).get("cookie_expiry_days", 30)
    except:
        # Fallback to defaults
        password_hash = default_password_hash
        cookie_name = "career_assessment_cookie"
        cookie_key = "random_signature_key_123"
        cookie_expiry_days = 30
    
    config = {
        'credentials': {
            'usernames': {
                'admin': {
                    'name': 'Administrator',
                    'password': password_hash
                }
            }
        },
        'cookie': {
            'name': cookie_name,
            'key': cookie_key,
            'expiry_days': cookie_expiry_days
        }
    }
    
    return config
