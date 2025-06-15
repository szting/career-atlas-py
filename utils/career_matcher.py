from data.careers import careers_database

def match_careers(riasec_scores, skills_confidence, work_values):
    """
    Match user profile with careers based on RIASEC scores, skills, and values
    
    Returns a list of careers sorted by match percentage
    """
    career_matches = []
    
    # Get top two RIASEC types
    sorted_types = sorted(riasec_scores.items(), key=lambda x: x[1], reverse=True)
    primary_type = sorted_types[0][0] if sorted_types else None
    secondary_type = sorted_types[1][0] if len(sorted_types) > 1 else None
    
    for career in careers_database:
        match_score = 0
        
        # RIASEC matching (40% weight)
        if career['primary_type'] == primary_type:
            match_score += 30
        if career.get('secondary_type') == secondary_type:
            match_score += 10
        elif career['primary_type'] == secondary_type:
            match_score += 20
        
        # Skills matching (35% weight)
        if career.get('required_skills'):
            matching_skills = 0
            for skill in career['required_skills']:
                if skill in skills_confidence and skills_confidence[skill] >= 60:
                    matching_skills += 1
            
            if career['required_skills']:
                skill_match_ratio = matching_skills / len(career['required_skills'])
                match_score += skill_match_ratio * 35
        
        # Work values matching (25% weight)
        if career.get('work_environment') and work_values:
            value_matches = 0
            for value in work_values:
                # Simple keyword matching - in production, use more sophisticated matching
                for env in career['work_environment']:
                    if value.lower() in env.lower() or env.lower() in value.lower():
                        value_matches += 1
                        break
            
            value_match_ratio = value_matches / len(work_values) if work_values else 0
            match_score += value_match_ratio * 25
        
        career_matches.append({
            **career,
            'match_score': round(match_score)
        })
    
    # Sort by match score
    career_matches.sort(key=lambda x: x['match_score'], reverse=True)
    
    return career_matches
