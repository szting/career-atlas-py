# Coaching Questions Database

coaching_questions = [
    # Realistic Type Questions
    {
        'id': 'r-explore-1',
        'category': 'exploration',
        'riasecFocus': 'realistic',
        'question': 'What hands-on activities or projects have given you the most satisfaction?',
        'purpose': 'Identify specific practical interests and skills',
        'followUp': [
            'What made these experiences particularly rewarding?',
            'How might you incorporate more of these activities into your career?'
        ]
    },
    {
        'id': 'r-develop-1',
        'category': 'development',
        'riasecFocus': 'realistic',
        'question': 'What technical or practical skills would you like to develop further?',
        'purpose': 'Identify skill development opportunities',
        'followUp': [
            'What resources or training would help you develop these skills?',
            'How would mastering these skills impact your career goals?'
        ]
    },
    
    # Investigative Type Questions
    {
        'id': 'i-explore-1',
        'category': 'exploration',
        'riasecFocus': 'investigative',
        'question': 'What problems or mysteries do you find yourself naturally drawn to solving?',
        'purpose': 'Uncover analytical interests and problem-solving preferences',
        'followUp': [
            'What methods do you typically use to investigate these problems?',
            'How could you apply this curiosity in a professional setting?'
        ]
    },
    {
        'id': 'i-develop-1',
        'category': 'development',
        'riasecFocus': 'investigative',
        'question': 'What areas of knowledge would you like to explore more deeply?',
        'purpose': 'Identify learning goals and intellectual interests',
        'followUp': [
            'What specific topics within this area fascinate you most?',
            'How might expertise in this area advance your career?'
        ]
    },
    
    # Artistic Type Questions
    {
        'id': 'a-explore-1',
        'category': 'exploration',
        'riasecFocus': 'artistic',
        'question': 'How do you currently express your creativity, and how would you like to expand this?',
        'purpose': 'Explore creative outlets and artistic aspirations',
        'followUp': [
            'What barriers prevent you from being more creative in your work?',
            'What creative projects would you pursue if resources were unlimited?'
        ]
    },
    {
        'id': 'a-develop-1',
        'category': 'development',
        'riasecFocus': 'artistic',
        'question': 'What creative skills or techniques would enhance your professional value?',
        'purpose': 'Connect creativity to career development',
        'followUp': [
            'How could you practice these skills in your current role?',
            'What creative professionals do you admire and why?'
        ]
    },
    
    # Social Type Questions
    {
        'id': 's-explore-1',
        'category': 'exploration',
        'riasecFocus': 'social',
        'question': 'Describe a time when you made a meaningful difference in someone\'s life.',
        'purpose': 'Identify helping motivations and impact preferences',
        'followUp': [
            'What aspects of helping others energize you most?',
            'How could you create more opportunities for meaningful impact?'
        ]
    },
    {
        'id': 's-develop-1',
        'category': 'development',
        'riasecFocus': 'social',
        'question': 'What interpersonal skills would help you be more effective in supporting others?',
        'purpose': 'Identify relationship and communication skill gaps',
        'followUp': [
            'Which of these skills would have the most immediate impact?',
            'How could you practice these skills in low-stakes situations?'
        ]
    },
    
    # Enterprising Type Questions
    {
        'id': 'e-explore-1',
        'category': 'exploration',
        'riasecFocus': 'enterprising',
        'question': 'What opportunities do you see that others might be missing?',
        'purpose': 'Uncover entrepreneurial thinking and vision',
        'followUp': [
            'What would it take to pursue these opportunities?',
            'What\'s holding you back from taking action?'
        ]
    },
    {
        'id': 'e-develop-1',
        'category': 'development',
        'riasecFocus': 'enterprising',
        'question': 'What leadership or influence skills would accelerate your success?',
        'purpose': 'Identify leadership development needs',
        'followUp': [
            'What leadership challenges do you currently face?',
            'Who are your leadership role models and what can you learn from them?'
        ]
    },
    
    # Conventional Type Questions
    {
        'id': 'c-explore-1',
        'category': 'exploration',
        'riasecFocus': 'conventional',
        'question': 'What systems or processes have you improved or would like to improve?',
        'purpose': 'Identify organizational interests and efficiency focus',
        'followUp': [
            'What inefficiencies frustrate you most in your current work?',
            'How do you approach creating order from chaos?'
        ]
    },
    {
        'id': 'c-develop-1',
        'category': 'development',
        'riasecFocus': 'conventional',
        'question': 'What organizational or analytical tools would make you more effective?',
        'purpose': 'Identify system and process skill needs',
        'followUp': [
            'Which tools or methods have you been curious about?',
            'How would mastering these tools impact your daily work?'
        ]
    }
]

def get_coaching_questions(riasec_type, category=None):
    """Get coaching questions filtered by RIASEC type and optionally by category"""
    questions = [q for q in coaching_questions if q['riasecFocus'] == riasec_type]
    
    if category:
        questions = [q for q in questions if q['category'] == category]
    
    return questions
