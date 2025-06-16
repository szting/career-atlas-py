def calculate_career_matches(user_profile):
    """Calculate career matches based on user profile"""
    from data.careers import careers
    
    matches = []
    
    for career in careers:
        score = 0
        
        # RIASEC matching (40% weight)
        primary_score = user_profile['riasecScores'].get(career['primary_type'], 0)
        secondary_score = user_profile['riasecScores'].get(career.get('secondary_type', ''), 0)
        riasec_score = (primary_score * 0.7 + secondary_score * 0.3) / 5 * 40
        
        # Skills matching (35% weight)
        skills_match = 0
        if user_profile['skillsConfidence']:
            matched_skills = 0
            for skill in career['required_skills']:
                if skill in user_profile['skillsConfidence']:
                    matched_skills += user_profile['skillsConfidence'][skill] / 5
            skills_score = (matched_skills / len(career['required_skills'])) * 35 if career['required_skills'] else 0
        else:
            skills_score = 0
        
        # Work values matching (25% weight)
        values_score = 0
        if user_profile['workValues']:
            value_keywords = {
                'Work-Life Balance': ['flexible', 'balance', 'remote'],
                'Job Security': ['stable', 'secure', 'established'],
                'High Earnings': ['high salary', 'lucrative', 'well-paid'],
                'Helping Others': ['help', 'serve', 'support', 'care'],
                'Creativity': ['creative', 'innovative', 'design'],
                'Leadership': ['lead', 'manage', 'direct'],
                'Continuous Learning': ['learn', 'grow', 'develop'],
                'Recognition': ['recognition', 'prestige', 'respected']
            }
            
            matched_values = 0
            for value in user_profile['workValues']:
                keywords = value_keywords.get(value, [])
                for keyword in keywords:
                    if any(keyword in env.lower() for env in career.get('work_environment', [])):
                        matched_values += 1
                        break
            
            values_score = (matched_values / len(user_profile['workValues'])) * 25 if user_profile['workValues'] else 0
        
        total_score = riasec_score + skills_score + values_score
        
        matches.append({
            **career,
            'matchScore': round(total_score)
        })
    
    # Sort by match score
    matches.sort(key=lambda x: x['matchScore'], reverse=True)
    
    return matches[:10]  # Return top 10 matches
