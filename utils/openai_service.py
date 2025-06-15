import os
import json
from typing import Dict, List, Tuple, Optional
import streamlit as st

# Import OpenAI at module level
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    st.warning("OpenAI library not installed. Using fallback responses.")

class OpenAIService:
    def __init__(self):
        # Try to get API key from session state first, then environment
        self.api_key = st.session_state.get('api_keys', {}).get('openai', '') or os.getenv('OPENAI_API_KEY', '')
        self.model = "gpt-4o-mini"
        self._client = None
        
        # Check if API key is available
        if not self.api_key:
            st.info("OpenAI API key not configured. Using fallback responses.")
    
    def _get_client(self):
        """Lazy load OpenAI client"""
        if self._client is None and self.api_key and OPENAI_AVAILABLE:
            try:
                self._client = openai.OpenAI(api_key=self.api_key)
            except Exception as e:
                st.warning(f"Error initializing OpenAI client: {str(e)}")
                return None
        return self._client
    
    def _make_request(self, messages: List[Dict], max_tokens: int = 1000) -> str:
        """Make request to OpenAI API with fallback"""
        try:
            # Check if API key exists
            if not self.api_key:
                return self._generate_fallback_response(messages)
            
            client = self._get_client()
            if not client:
                return self._generate_fallback_response(messages)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            st.warning(f"OpenAI API error: {str(e)}. Using fallback responses.")
            return self._generate_fallback_response(messages)
    
    def generate_career_recommendations(self, user_profile: Dict, uploaded_frameworks: Dict = None) -> List[Dict]:
        """Generate career recommendations based on profile and uploaded frameworks"""
        from utils.career_matcher import get_top_riasec_types
        
        top_types = get_top_riasec_types(user_profile['riasec_scores'])
        
        # Build prompt including uploaded frameworks if available
        prompt = self._build_career_recommendations_prompt(user_profile, top_types, uploaded_frameworks)
        
        messages = [
            {
                'role': 'system',
                'content': 'You are an expert career counselor specializing in RIASEC assessments and skills-based career matching.'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ]
        
        response = self._make_request(messages, 2000)
        return self._parse_career_recommendations(response)
    
    def _build_career_recommendations_prompt(self, user_profile: Dict, top_types: List[Tuple], uploaded_frameworks: Dict = None) -> str:
        prompt = f"""
Generate 5-7 personalized career recommendations based on this profile:

RIASEC Profile:
{chr(10).join([f"- {type_name.capitalize()}: {score}%" for type_name, score in top_types])}

Top Skills (confidence 1-100):
{chr(10).join([f"- {skill}: {conf}%" for skill, conf in sorted(user_profile['skills_confidence'].items(), key=lambda x: x[1], reverse=True)[:10]])}

Work Values:
{chr(10).join([f"- {value}" for value in user_profile['work_values'][:5]])}
"""
        
        # Add uploaded frameworks context if available
        if uploaded_frameworks:
            prompt += f"""

Additional Context from Uploaded Frameworks:
"""
            for framework_name, framework_data in uploaded_frameworks.items():
                if isinstance(framework_data, dict):
                    skills = framework_data.get('skills', [])
                    if skills:
                        prompt += f"- {framework_name}: {', '.join(skills[:5])}\n"
                    
                    # Add any additional framework details
                    if 'categories' in framework_data:
                        for category, items in framework_data['categories'].items():
                            prompt += f"  - {category}: {', '.join(items[:3])}\n"
        
        prompt += """

For each career recommendation, provide:
TITLE: [Career title]
MATCH: [Match percentage 0-100]
DESCRIPTION: [2-3 sentence description]
ACTIVITIES: [4-5 key daily activities separated by |]
DEVELOPMENT: [3-4 skills to develop separated by |]
NEXT_STEPS: [4 concrete next steps separated by |]

Focus on careers that:
1. Align with their top RIASEC types
2. Leverage their strongest skills
3. Match their work values
4. Consider any uploaded skill frameworks
"""
        return prompt
    
    def _parse_career_recommendations(self, response: str) -> List[Dict]:
        """Parse career recommendations from response"""
        recommendations = []
        sections = response.split('TITLE:')[1:] if 'TITLE:' in response else []
        
        for section in sections:
            lines = section.strip().split('\n')
            title = lines[0].strip()
            
            recommendation = {
                'title': title,
                'match_score': 75,  # Default
                'description': '',
                'activities': [],
                'skills_to_develop': [],
                'next_steps': []
            }
            
            for line in lines[1:]:
                if line.startswith('MATCH:'):
                    try:
                        recommendation['match_score'] = int(line.replace('MATCH:', '').strip().replace('%', ''))
                    except:
                        pass
                elif line.startswith('DESCRIPTION:'):
                    recommendation['description'] = line.replace('DESCRIPTION:', '').strip()
                elif line.startswith('ACTIVITIES:'):
                    recommendation['activities'] = [a.strip() for a in line.replace('ACTIVITIES:', '').split('|')]
                elif line.startswith('DEVELOPMENT:'):
                    recommendation['skills_to_develop'] = [s.strip() for s in line.replace('DEVELOPMENT:', '').split('|')]
                elif line.startswith('NEXT_STEPS:'):
                    recommendation['next_steps'] = [s.strip() for s in line.replace('NEXT_STEPS:', '').split('|')]
            
            if recommendation['title'] and recommendation['description']:
                recommendations.append(recommendation)
        
        return recommendations if recommendations else self._get_fallback_career_recommendations()
    
    def _get_fallback_career_recommendations(self) -> List[Dict]:
        """Return fallback career recommendations"""
        return [
            {
                'title': 'Data Analyst',
                'match_score': 85,
                'description': 'Analyze complex datasets to help organizations make data-driven decisions. Combines investigative thinking with practical problem-solving.',
                'activities': ['Analyzing data patterns', 'Creating visualizations', 'Writing reports', 'Presenting findings'],
                'skills_to_develop': ['Statistical analysis', 'Data visualization tools', 'Business acumen'],
                'next_steps': ['Learn SQL and Python', 'Take statistics course', 'Build portfolio projects', 'Network with data professionals']
            },
            {
                'title': 'UX Researcher',
                'match_score': 80,
                'description': 'Study user behavior and preferences to improve product design. Blends investigative research with creative problem-solving.',
                'activities': ['Conducting user interviews', 'Analyzing usage data', 'Creating personas', 'Testing prototypes'],
                'skills_to_develop': ['Research methodologies', 'Data analysis', 'Communication skills'],
                'next_steps': ['Learn UX research methods', 'Practice user interviews', 'Study human-computer interaction', 'Join UX communities']
            },
            {
                'title': 'Project Manager',
                'match_score': 78,
                'description': 'Lead cross-functional teams to deliver projects on time and within budget. Combines organizational skills with people management.',
                'activities': ['Planning project timelines', 'Coordinating team members', 'Managing budgets', 'Reporting progress'],
                'skills_to_develop': ['Agile methodologies', 'Risk management', 'Stakeholder communication'],
                'next_steps': ['Get PMP certification', 'Learn project management software', 'Practice leadership skills', 'Build project portfolio']
            }
        ]
    
    def _generate_fallback_response(self, messages: List[Dict]) -> str:
        """Generate fallback responses when API is unavailable"""
        user_message = messages[-1]['content'] if messages else ''
        
        if 'coaching questions' in user_message.lower():
            return self._generate_fallback_coaching_questions()
        elif 'reflection questions' in user_message.lower():
            return self._generate_fallback_reflection_questions()
        elif 'career recommendations' in user_message.lower():
            return self._generate_fallback_career_recommendations_text()
        elif 'development plan' in user_message.lower():
            return self._generate_fallback_development_plan()
        
        return "Unable to generate AI response. Please check your API configuration."
    
    def _generate_fallback_career_recommendations_text(self) -> str:
        return """TITLE: Data Analyst
MATCH: 85
DESCRIPTION: Analyze complex datasets to help organizations make data-driven decisions. Combines investigative thinking with practical problem-solving.
ACTIVITIES: Analyzing data patterns | Creating visualizations | Writing reports | Presenting findings
DEVELOPMENT: Statistical analysis | Data visualization tools | Business acumen
NEXT_STEPS: Learn SQL and Python | Take statistics course | Build portfolio projects | Network with data professionals

TITLE: UX Researcher
MATCH: 80
DESCRIPTION: Study user behavior and preferences to improve product design. Blends investigative research with creative problem-solving.
ACTIVITIES: Conducting user interviews | Analyzing usage data | Creating personas | Testing prototypes
DEVELOPMENT: Research methodologies | Data analysis | Communication skills
NEXT_STEPS: Learn UX research methods | Practice user interviews | Study human-computer interaction | Join UX communities

TITLE: Project Manager
MATCH: 78
DESCRIPTION: Lead cross-functional teams to deliver projects on time and within budget. Combines organizational skills with people management.
ACTIVITIES: Planning project timelines | Coordinating team members | Managing budgets | Reporting progress
DEVELOPMENT: Agile methodologies | Risk management | Stakeholder communication
NEXT_STEPS: Get PMP certification | Learn project management software | Practice leadership skills | Build project portfolio"""
    
    def _generate_fallback_coaching_questions(self) -> str:
        return """QUESTION: What aspects of your current role align most closely with your top RIASEC types?
CATEGORY: exploration
PURPOSE: Help identify areas where natural interests and current work intersect
FOLLOW-UP: How could you incorporate more of these elements? | What barriers prevent fuller alignment? | Which aligned activities energize you most?

QUESTION: Looking at your skill confidence levels, which areas would you like to develop further?
CATEGORY: development
PURPOSE: Identify skill gaps and growth opportunities based on self-assessment
FOLLOW-UP: What resources would help you build these skills? | How might these skills benefit your career? | What's your timeline for development?

QUESTION: What are your top three career goals for the next 2-3 years?
CATEGORY: goal-setting
PURPOSE: Establish clear career objectives aligned with RIASEC profile
FOLLOW-UP: How do these goals align with your interests? | What steps are needed to achieve them? | Who could support you in reaching these goals?

QUESTION: When do you feel most engaged and fulfilled in your work?
CATEGORY: reflection
PURPOSE: Identify intrinsic motivators and optimal work conditions
FOLLOW-UP: How often do you experience this state? | What conditions enable it? | How could you create more of these moments?"""
    
    def _generate_fallback_reflection_questions(self) -> str:
        return """QUESTION: How well does your team member's current role align with their RIASEC profile strengths?
CONTEXT: development
GUIDANCE: Use this to explore role crafting opportunities and identify tasks that could be delegated or expanded to better match their interests.

QUESTION: What projects or initiatives have brought out the best in this team member's performance?
CONTEXT: performance
GUIDANCE: Look for patterns that connect to their RIASEC types and use these insights to assign future projects that leverage their natural interests.

QUESTION: Where do you see the greatest potential for this person's career growth based on their profile?
CONTEXT: career_planning
GUIDANCE: Consider both vertical and lateral moves that would align with their dominant RIASEC types while building on existing skills."""
    
    def _generate_fallback_development_plan(self) -> str:
        return """SHORT_TERM_GOALS (3-6 months):
GOAL: Build foundational skills in your top RIASEC area | ACTIONS: Take online course|Practice daily|Join relevant community | TIMELINE: 3 months
GOAL: Expand professional network in target field | ACTIONS: Attend 2 events monthly|Connect on LinkedIn|Schedule informational interviews | TIMELINE: Ongoing

LONG_TERM_GOALS (1-2 years):
GOAL: Transition to role aligned with RIASEC profile | ACTIONS: Update resume|Apply strategically|Leverage network | TIMELINE: 12-18 months

SKILL_GAPS:
Technical skills in primary interest area | Leadership and communication | Industry-specific knowledge

RESOURCES:
Coursera or edX courses | Professional associations | Industry publications | LinkedIn Learning"""
    
    def generate_coaching_questions(self, user_profile: Dict) -> List[Dict]:
        """Generate personalized coaching questions"""
        from utils.career_matcher import get_top_riasec_types
        
        top_types = get_top_riasec_types(user_profile['riasec_scores'])
        prompt = self._build_coaching_prompt(user_profile, top_types)
        
        messages = [
            {
                'role': 'system',
                'content': 'You are an expert career coach specializing in RIASEC personality assessments.'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ]
        
        response = self._make_request(messages, 1500)
        return self._parse_coaching_questions(response)
    
    def generate_reflection_questions(self, user_profile: Dict) -> List[Dict]:
        """Generate reflection questions for managers"""
        from utils.career_matcher import get_top_riasec_types
        
        top_types = get_top_riasec_types(user_profile['riasec_scores'])
        prompt = self._build_reflection_prompt(user_profile, top_types)
        
        messages = [
            {
                'role': 'system',
                'content': 'You are an expert in organizational psychology and team management.'
            },
            {
                'role': 'user',
                'content': prompt
            }
        ]
        
        response = self._make_request(messages, 1500)
        return self._parse_reflection_questions(response)
    
    def _build_coaching_prompt(self, user_profile: Dict, top_types: List[Tuple]) -> str:
        return f"""
Generate 8-10 personalized coaching questions for an individual with the following profile:

RIASEC Scores:
{chr(10).join([f"- {type_name.capitalize()}: {score}%" for type_name, score in top_types])}

Top Skills (confidence level 1-100):
{chr(10).join([f"- {skill}: {conf}%" for skill, conf in sorted(user_profile['skills_confidence'].items(), key=lambda x: x[1], reverse=True)[:5]])}

Work Values:
{chr(10).join([f"- {value}" for value in user_profile['work_values'][:5]])}

Please generate questions in the following categories:
1. Career Exploration (2-3 questions)
2. Skill Development (2-3 questions)  
3. Goal Setting (2-3 questions)
4. Self Reflection (2-3 questions)

Format each question as:
QUESTION: [The coaching question]
CATEGORY: [exploration/development/goal-setting/reflection]
PURPOSE: [Why this question is valuable for this person]
FOLLOW-UP: [2-3 follow-up questions separated by |]
"""
    
    def _build_reflection_prompt(self, user_profile: Dict, top_types: List[Tuple]) -> str:
        return f"""
Generate 8-10 reflection questions that a manager can use with a team member who has this profile:

RIASEC Scores:
{chr(10).join([f"- {type_name.capitalize()}: {score}%" for type_name, score in top_types])}

Top Skills:
{chr(10).join([f"- {skill}: {conf}%" for skill, conf in sorted(user_profile['skills_confidence'].items(), key=lambda x: x[1], reverse=True)[:5]])}

Work Values:
{chr(10).join([f"- {value}" for value in user_profile['work_values'][:5]])}

Generate questions for these contexts:
1. Development Conversations (3-4 questions)
2. Performance Reviews (3-4 questions)
3. Career Planning (2-3 questions)

Format each question as:
QUESTION: [The reflection question]
CONTEXT: [development/performance/career_planning]
GUIDANCE: [Specific guidance for the manager on how to use this question effectively]
"""
    
    def _parse_coaching_questions(self, response: str) -> List[Dict]:
        """Parse coaching questions from response"""
        questions = []
        sections = response.split('QUESTION:')[1:]
        
        for section in sections:
            lines = section.strip().split('\n')
            question = lines[0].strip()
            
            category_match = None
            purpose_match = None
            followup_match = None
            
            for line in lines[1:]:
                if line.startswith('CATEGORY:'):
                    category_match = line.replace('CATEGORY:', '').strip()
                elif line.startswith('PURPOSE:'):
                    purpose_match = line.replace('PURPOSE:', '').strip()
                elif line.startswith('FOLLOW-UP:'):
                    followup_match = line.replace('FOLLOW-UP:', '').strip()
            
            if question and category_match and purpose_match:
                questions.append({
                    'question': question,
                    'category': category_match,
                    'purpose': purpose_match,
                    'follow_up': followup_match.split('|') if followup_match else []
                })
        
        return questions if questions else self._get_default_coaching_questions()
    
    def _parse_reflection_questions(self, response: str) -> List[Dict]:
        """Parse reflection questions from response"""
        questions = []
        sections = response.split('QUESTION:')[1:]
        
        for section in sections:
            lines = section.strip().split('\n')
            question = lines[0].strip()
            
            context_match = None
            guidance_match = None
            
            for line in lines[1:]:
                if line.startswith('CONTEXT:'):
                    context_match = line.replace('CONTEXT:', '').strip()
                elif line.startswith('GUIDANCE:'):
                    guidance_match = line.replace('GUIDANCE:', '').strip()
            
            if question and context_match and guidance_match:
                questions.append({
                    'question': question,
                    'context': context_match,
                    'manager_guidance': guidance_match
                })
        
        return questions if questions else self._get_default_reflection_questions()
    
    def _get_default_coaching_questions(self) -> List[Dict]:
        """Return default coaching questions"""
        return [
            {
                'question': "What aspects of your work bring you the most satisfaction?",
                'category': "reflection",
                'purpose': "Identify intrinsic motivators aligned with RIASEC profile",
                'follow_up': ["How could you incorporate more of these elements?", "What barriers exist?"]
            },
            {
                'question': "Which skills would you like to develop further in the next year?",
                'category': "development",
                'purpose': "Focus skill development on areas aligned with career interests",
                'follow_up': ["What resources would help?", "How will these skills benefit your career?"]
            }
        ]
    
    def _get_default_reflection_questions(self) -> List[Dict]:
        """Return default reflection questions"""
        return [
            {
                'question': "How well does your current role align with your team member's interests?",
                'context': "development",
                'manager_guidance': "Use this to explore role crafting opportunities"
            },
            {
                'question': "What projects have brought out the best in their performance?",
                'context': "performance", 
                'manager_guidance': "Look for patterns that connect to their RIASEC profile"
            }
        ]
