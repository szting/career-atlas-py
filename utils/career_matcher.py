from typing import Dict, List, Tuple
import numpy as np

def get_top_riasec_types(riasec_scores: Dict[str, float], top_n: int = 3) -> List[Tuple[str, float]]:
    """Get top N RIASEC types sorted by score"""
    sorted_types = sorted(riasec_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_types[:top_n]

def calculate_match_score(riasec_scores: Dict[str, float], 
                         skills_confidence: Dict[str, float],
                         work_values: List[str],
                         career_profile: Dict) -> float:
    """Calculate match score between user profile and career"""
    
    # RIASEC match (40% weight)
    riasec_match = 0
    career_riasec = career_profile.get('riasec_profile', {})
    for type_name, user_score in riasec_scores.items():
        career_score = career_riasec.get(type_name, 0)
        riasec_match += (1 - abs(user_score - career_score) / 5) * 100
    riasec_match = riasec_match / len(riasec_scores) * 0.4
    
    # Skills match (40% weight)
    skills_match = 0
    required_skills = career_profile.get('required_skills', [])
    if required_skills:
        matched_skills = 0
        for skill in required_skills:
            if skill in skills_confidence:
                matched_skills += skills_confidence[skill] / 100
        skills_match = (matched_skills / len(required_skills)) * 100 * 0.4
    else:
        skills_match = 40  # Default if no skills specified
    
    # Values match (20% weight)
    values_match = 0
    career_values = career_profile.get('work_environment', [])
    if career_values and work_values:
        matched_values = len(set(work_values) & set(career_values))
        values_match = (matched_values / max(len(work_values), len(career_values))) * 100 * 0.2
    else:
        values_match = 20  # Default if no values specified
    
    return round(riasec_match + skills_match + values_match)

def match_careers(riasec_scores: Dict[str, float],
                 skills_confidence: Dict[str, float],
                 work_values: List[str]) -> List[Dict]:
    """Match user profile with careers from database"""
    
    # Default career database (will be replaced by uploaded data)
    default_careers = [
        {
            'title': 'Software Developer',
            'description': 'Design, develop, and maintain software applications',
            'riasec_profile': {'investigative': 4, 'realistic': 3, 'conventional': 2, 'artistic': 2, 'enterprising': 1, 'social': 1},
            'required_skills': ['Problem Solving', 'Technical Skills', 'Analytical Thinking', 'Communication', 'Teamwork'],
            'work_environment': ['Innovation', 'Flexibility', 'Learning Opportunities', 'Work-Life Balance'],
            'salary_range': '$70,000 - $130,000',
            'growth_outlook': 'Much faster than average (22% growth)'
        },
        {
            'title': 'Data Analyst',
            'description': 'Analyze data to help organizations make informed decisions',
            'riasec_profile': {'investigative': 5, 'conventional': 3, 'realistic': 2, 'enterprising': 2, 'artistic': 1, 'social': 1},
            'required_skills': ['Analytical Thinking', 'Technical Skills', 'Problem Solving', 'Communication', 'Attention to Detail'],
            'work_environment': ['Stability', 'Learning Opportunities', 'Teamwork', 'Recognition'],
            'salary_range': '$60,000 - $95,000',
            'growth_outlook': 'Much faster than average (25% growth)'
        },
        {
            'title': 'Marketing Manager',
            'description': 'Plan and execute marketing strategies to promote products or services',
            'riasec_profile': {'enterprising': 5, 'artistic': 3, 'social': 3, 'conventional': 2, 'investigative': 1, 'realistic': 0},
            'required_skills': ['Leadership', 'Communication', 'Creativity', 'Strategic Planning', 'Teamwork'],
            'work_environment': ['Leadership Opportunities', 'Innovation', 'Recognition', 'Flexibility'],
            'salary_range': '$65,000 - $135,000',
            'growth_outlook': 'Faster than average (10% growth)'
        },
        {
            'title': 'Graphic Designer',
            'description': 'Create visual concepts to communicate ideas through images and layouts',
            'riasec_profile': {'artistic': 5, 'realistic': 2, 'enterprising': 2, 'investigative': 1, 'social': 1, 'conventional': 1},
            'required_skills': ['Creativity', 'Technical Skills', 'Communication', 'Attention to Detail', 'Time Management'],
            'work_environment': ['Creativity', 'Flexibility', 'Independence', 'Innovation'],
            'salary_range': '$45,000 - $85,000',
            'growth_outlook': 'Average (3% growth)'
        },
        {
            'title': 'Human Resources Manager',
            'description': 'Oversee recruitment, training, and employee relations',
            'riasec_profile': {'social': 5, 'enterprising': 3, 'conventional': 3, 'investigative': 1, 'artistic': 1, 'realistic': 0},
            'required_skills': ['Communication', 'Leadership', 'Problem Solving', 'Empathy', 'Organization'],
            'work_environment': ['Helping Others', 'Teamwork', 'Stability', 'Work-Life Balance'],
            'salary_range': '$70,000 - $125,000',
            'growth_outlook': 'Faster than average (9% growth)'
        }
    ]
    
    # Use uploaded career database if available
    import streamlit as st
    careers = st.session_state.get('career_database', default_careers)
    if not careers:
        careers = default_careers
    
    # Calculate match scores
    career_matches = []
    for career in careers:
        match_score = calculate_match_score(riasec_scores, skills_confidence, work_values, career)
        career_match = career.copy()
        career_match['match_score'] = match_score
        career_matches.append(career_match)
    
    # Sort by match score
    career_matches.sort(key=lambda x: x['match_score'], reverse=True)
    
    return career_matches
