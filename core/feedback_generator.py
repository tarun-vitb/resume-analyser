"""
Personalized Feedback Generation System
Provides actionable recommendations for resume improvement using NLP analysis
"""

import re
import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from collections import Counter, defaultdict
import language_tool_python
from datetime import datetime


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class FeedbackItem:
    """Individual feedback item"""
    category: str
    severity: str  # 'critical', 'important', 'suggestion'
    title: str
    description: str
    suggestion: str
    examples: List[str] = None
    priority: int = 1  # 1-10 scale

@dataclass
class ResumeAnalysis:
    """Complete resume analysis results"""
    overall_score: float  # 0-100 scale
    strengths: List[str]
    weaknesses: List[str]
    feedback_items: List[FeedbackItem]
    keyword_optimization: Dict[str, Any]
    formatting_issues: List[str]
    content_suggestions: List[str]
    ats_compatibility: Dict[str, Any]

class FeedbackGenerator:
    """Advanced feedback generation system for resume optimization"""
    
    def __init__(self):
        """Initialize feedback generator with language tools"""
        
        # Initialize grammar checker
        try:
            self.grammar_tool = language_tool_python.LanguageTool('en-US')
        except Exception as e:
            logger.warning(f"Could not initialize grammar tool: {e}")
            self.grammar_tool = None
        
        # Action words for resume enhancement
        self.strong_action_words = [
            'achieved', 'administered', 'analyzed', 'architected', 'automated',
            'built', 'collaborated', 'created', 'delivered', 'designed',
            'developed', 'directed', 'engineered', 'enhanced', 'established',
            'executed', 'implemented', 'improved', 'increased', 'initiated',
            'launched', 'led', 'managed', 'optimized', 'orchestrated',
            'pioneered', 'reduced', 'resolved', 'spearheaded', 'streamlined',
            'transformed', 'utilized'
        ]
        
        # Weak words to avoid
        self.weak_words = [
            'responsible for', 'duties included', 'worked on', 'helped with',
            'assisted in', 'participated in', 'involved in', 'contributed to',
            'familiar with', 'exposure to', 'knowledge of'
        ]
        
        # Professional sections that should be present
        self.required_sections = [
            'contact information', 'professional summary', 'experience',
            'education', 'skills'
        ]
        
        # ATS-friendly formatting rules
        self.ats_rules = {
            'file_format': ['pdf', 'docx'],
            'font_types': ['arial', 'calibri', 'times new roman', 'helvetica'],
            'avoid_elements': ['tables', 'text boxes', 'images', 'graphics'],
            'section_headers': ['clear', 'standard', 'consistent']
        }
        
        # Industry-specific keywords
        self.industry_keywords = {
            'software_engineering': [
                'agile', 'scrum', 'ci/cd', 'microservices', 'api', 'database',
                'testing', 'debugging', 'version control', 'code review'
            ],
            'data_science': [
                'machine learning', 'statistical analysis', 'data visualization',
                'predictive modeling', 'big data', 'etl', 'data pipeline'
            ],
            'product_management': [
                'roadmap', 'stakeholder management', 'user research', 'metrics',
                'a/b testing', 'product strategy', 'cross-functional'
            ],
            'marketing': [
                'campaign management', 'roi', 'conversion rate', 'lead generation',
                'brand awareness', 'market research', 'customer acquisition'
            ]
        }

    def analyze_resume(self, 
                      resume_text: str, 
                      job_description: str = None,
                      target_role: str = None) -> ResumeAnalysis:
        """Perform comprehensive resume analysis and generate feedback"""
        
        # Initialize analysis components
        feedback_items = []
        strengths = []
        weaknesses = []
        
        # 1. Content Analysis
        content_feedback = self._analyze_content_quality(resume_text)
        feedback_items.extend(content_feedback)
        
        # 2. Grammar and Language Analysis
        if self.grammar_tool:
            grammar_feedback = self._analyze_grammar(resume_text)
            feedback_items.extend(grammar_feedback)
        
        # 3. Keyword Optimization
        keyword_analysis = self._analyze_keywords(resume_text, job_description)
        keyword_feedback = self._generate_keyword_feedback(keyword_analysis)
        feedback_items.extend(keyword_feedback)
        
        # 4. Structure and Formatting Analysis
        formatting_feedback = self._analyze_formatting(resume_text)
        feedback_items.extend(formatting_feedback)
        
        # 5. ATS Compatibility Check
        ats_analysis = self._analyze_ats_compatibility(resume_text)
        ats_feedback = self._generate_ats_feedback(ats_analysis)
        feedback_items.extend(ats_feedback)
        
        # 6. Professional Impact Analysis
        impact_feedback = self._analyze_professional_impact(resume_text)
        feedback_items.extend(impact_feedback)
        
        # 7. Industry-Specific Analysis
        if target_role:
            industry_feedback = self._analyze_industry_alignment(resume_text, target_role)
            feedback_items.extend(industry_feedback)
        
        # Calculate overall score
        overall_score = self._calculate_overall_score(feedback_items, resume_text)
        
        # Identify strengths and weaknesses
        strengths, weaknesses = self._identify_strengths_weaknesses(feedback_items, resume_text)
        
        # Generate content suggestions
        content_suggestions = self._generate_content_suggestions(resume_text, job_description)
        
        # Format formatting issues
        formatting_issues = [item.description for item in feedback_items 
                           if item.category == 'formatting']
        
        return ResumeAnalysis(
            overall_score=overall_score,
            strengths=strengths,
            weaknesses=weaknesses,
            feedback_items=sorted(feedback_items, key=lambda x: x.priority, reverse=True),
            keyword_optimization=keyword_analysis,
            formatting_issues=formatting_issues,
            content_suggestions=content_suggestions,
            ats_compatibility=ats_analysis
        )

    def _analyze_content_quality(self, resume_text: str) -> List[FeedbackItem]:
        """Analyze content quality and structure"""
        
        feedback = []
        
        # Check resume length
        word_count = len(resume_text.split())
        if word_count < 200:
            feedback.append(FeedbackItem(
                category="content",
                severity="critical",
                title="Resume Too Short",
                description=f"Your resume has only {word_count} words, which may not provide enough detail.",
                suggestion="Expand your experience descriptions with specific achievements and quantifiable results.",
                examples=["Instead of 'Worked on projects' write 'Led 3 cross-functional projects resulting in 25% efficiency improvement'"],
                priority=9
            ))
        elif word_count > 800:
            feedback.append(FeedbackItem(
                category="content",
                severity="important",
                title="Resume Too Long",
                description=f"Your resume has {word_count} words, which may be too lengthy for recruiters.",
                suggestion="Condense your content to highlight only the most relevant and impactful experiences.",
                examples=["Focus on last 10-15 years of experience and most relevant achievements"],
                priority=6
            ))
        
        # Check for quantifiable achievements
        numbers_pattern = r'\d+(?:\.\d+)?(?:%|k|K|million|M|thousand|\+)?'
        numbers_found = re.findall(numbers_pattern, resume_text)
        
        if len(numbers_found) < 3:
            feedback.append(FeedbackItem(
                category="content",
                severity="important",
                title="Lack of Quantifiable Achievements",
                description="Your resume lacks specific numbers and metrics to demonstrate impact.",
                suggestion="Add quantifiable results wherever possible to show your concrete contributions.",
                examples=[
                    "Increased sales by 30%",
                    "Managed team of 8 developers",
                    "Reduced processing time by 2 hours daily"
                ],
                priority=8
            ))
        
        # Check for action words
        action_word_count = sum(1 for word in self.strong_action_words 
                               if word in resume_text.lower())
        
        if action_word_count < 5:
            feedback.append(FeedbackItem(
                category="content",
                severity="important",
                title="Weak Action Words",
                description="Your resume uses few strong action words to describe your experience.",
                suggestion="Start bullet points with powerful action words to make your achievements more impactful.",
                examples=self.strong_action_words[:5],
                priority=7
            ))
        
        # Check for weak phrases
        weak_phrases_found = [phrase for phrase in self.weak_words 
                             if phrase in resume_text.lower()]
        
        if weak_phrases_found:
            feedback.append(FeedbackItem(
                category="content",
                severity="important",
                title="Passive Language",
                description=f"Found passive phrases: {', '.join(weak_phrases_found[:3])}",
                suggestion="Replace passive language with active, achievement-focused statements.",
                examples=[
                    "Instead of 'responsible for managing' use 'managed'",
                    "Instead of 'helped with' use 'contributed to' or 'achieved'"
                ],
                priority=6
            ))
        
        return feedback

    def _analyze_grammar(self, resume_text: str) -> List[FeedbackItem]:
        """Analyze grammar and language quality"""
        
        feedback = []
        
        try:
            matches = self.grammar_tool.check(resume_text)
            
            if len(matches) > 10:
                feedback.append(FeedbackItem(
                    category="grammar",
                    severity="critical",
                    title="Multiple Grammar Issues",
                    description=f"Found {len(matches)} potential grammar and spelling issues.",
                    suggestion="Carefully proofread your resume and consider using grammar checking tools.",
                    examples=[match.message for match in matches[:3]],
                    priority=9
                ))
            elif len(matches) > 5:
                feedback.append(FeedbackItem(
                    category="grammar",
                    severity="important",
                    title="Grammar Issues Detected",
                    description=f"Found {len(matches)} potential grammar issues.",
                    suggestion="Review and correct grammar errors to maintain professionalism.",
                    examples=[match.message for match in matches[:2]],
                    priority=7
                ))
            elif len(matches) > 0:
                feedback.append(FeedbackItem(
                    category="grammar",
                    severity="suggestion",
                    title="Minor Grammar Issues",
                    description=f"Found {len(matches)} minor grammar suggestions.",
                    suggestion="Consider reviewing these minor language improvements.",
                    priority=3
                ))
                
        except Exception as e:
            logger.warning(f"Grammar analysis failed: {e}")
        
        return feedback

    def _analyze_keywords(self, resume_text: str, job_description: str = None) -> Dict[str, Any]:
        """Analyze keyword optimization"""
        
        resume_words = set(word.lower() for word in re.findall(r'\b\w+\b', resume_text))
        
        analysis = {
            'total_unique_words': len(resume_words),
            'technical_keywords': [],
            'missing_keywords': [],
            'keyword_density': {},
            'job_match_score': 0.0
        }
        
        # Extract technical keywords
        tech_keywords = []
        for category, keywords in self.industry_keywords.items():
            for keyword in keywords:
                if keyword.lower() in resume_text.lower():
                    tech_keywords.append(keyword)
        
        analysis['technical_keywords'] = tech_keywords
        
        # Analyze job description match if provided
        if job_description:
            job_words = set(word.lower() for word in re.findall(r'\b\w+\b', job_description))
            
            # Filter out common words
            common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'a', 'an'}
            job_keywords = job_words - common_words - {'experience', 'work', 'job', 'position', 'role'}
            
            # Find missing keywords
            missing = job_keywords - resume_words
            analysis['missing_keywords'] = list(missing)[:10]  # Top 10 missing
            
            # Calculate match score
            matched_keywords = job_keywords & resume_words
            analysis['job_match_score'] = len(matched_keywords) / len(job_keywords) if job_keywords else 0
        
        return analysis

    def _generate_keyword_feedback(self, keyword_analysis: Dict[str, Any]) -> List[FeedbackItem]:
        """Generate feedback based on keyword analysis"""
        
        feedback = []
        
        # Technical keywords feedback
        if len(keyword_analysis['technical_keywords']) < 5:
            feedback.append(FeedbackItem(
                category="keywords",
                severity="important",
                title="Limited Technical Keywords",
                description="Your resume has few industry-specific technical terms.",
                suggestion="Include more relevant technical skills and industry terminology.",
                examples=["Add specific technologies, tools, and methodologies you've used"],
                priority=7
            ))
        
        # Job match feedback
        if keyword_analysis['job_match_score'] < 0.3:
            feedback.append(FeedbackItem(
                category="keywords",
                severity="critical",
                title="Poor Job Description Match",
                description=f"Only {keyword_analysis['job_match_score']:.1%} keyword match with job requirements.",
                suggestion="Incorporate more keywords from the job description into your resume.",
                examples=keyword_analysis['missing_keywords'][:5],
                priority=9
            ))
        elif keyword_analysis['job_match_score'] < 0.5:
            feedback.append(FeedbackItem(
                category="keywords",
                severity="important",
                title="Moderate Job Description Match",
                description=f"{keyword_analysis['job_match_score']:.1%} keyword match with job requirements.",
                suggestion="Consider adding more relevant keywords to improve alignment.",
                examples=keyword_analysis['missing_keywords'][:3],
                priority=6
            ))
        
        return feedback

    def _analyze_formatting(self, resume_text: str) -> List[FeedbackItem]:
        """Analyze formatting and structure"""
        
        feedback = []
        
        # Check for section headers
        common_sections = ['experience', 'education', 'skills', 'summary', 'objective']
        found_sections = [section for section in common_sections 
                         if section in resume_text.lower()]
        
        if len(found_sections) < 3:
            feedback.append(FeedbackItem(
                category="formatting",
                severity="important",
                title="Missing Key Sections",
                description="Your resume appears to be missing standard sections.",
                suggestion="Include clear sections for Experience, Education, Skills, and Summary.",
                examples=["Professional Summary", "Work Experience", "Education", "Technical Skills"],
                priority=7
            ))
        
        # Check for consistent formatting (basic heuristics)
        lines = resume_text.split('\n')
        bullet_patterns = [line for line in lines if line.strip().startswith(('•', '-', '*'))]
        
        if len(bullet_patterns) < 3:
            feedback.append(FeedbackItem(
                category="formatting",
                severity="suggestion",
                title="Limited Use of Bullet Points",
                description="Consider using bullet points to improve readability.",
                suggestion="Use bullet points to list achievements and responsibilities clearly.",
                priority=4
            ))
        
        return feedback

    def _analyze_ats_compatibility(self, resume_text: str) -> Dict[str, Any]:
        """Analyze ATS (Applicant Tracking System) compatibility"""
        
        analysis = {
            'ats_score': 0.0,
            'issues': [],
            'recommendations': []
        }
        
        score = 100  # Start with perfect score and deduct points
        
        # Check for complex formatting indicators
        if re.search(r'[│┌┐└┘├┤┬┴┼]', resume_text):
            analysis['issues'].append("Contains table borders or special characters")
            analysis['recommendations'].append("Remove table borders and special formatting characters")
            score -= 20
        
        # Check for standard section headers
        standard_headers = ['experience', 'education', 'skills', 'summary']
        found_headers = sum(1 for header in standard_headers if header in resume_text.lower())
        
        if found_headers < 3:
            analysis['issues'].append("Missing standard section headers")
            analysis['recommendations'].append("Use clear, standard section headers like 'Work Experience', 'Education', 'Skills'")
            score -= 15
        
        # Check for contact information
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        
        if not re.search(email_pattern, resume_text):
            analysis['issues'].append("No email address found")
            analysis['recommendations'].append("Include a professional email address")
            score -= 10
        
        if not re.search(phone_pattern, resume_text):
            analysis['issues'].append("No phone number found")
            analysis['recommendations'].append("Include a phone number")
            score -= 10
        
        analysis['ats_score'] = max(0, score)
        
        return analysis

    def _generate_ats_feedback(self, ats_analysis: Dict[str, Any]) -> List[FeedbackItem]:
        """Generate ATS compatibility feedback"""
        
        feedback = []
        
        if ats_analysis['ats_score'] < 70:
            feedback.append(FeedbackItem(
                category="ats",
                severity="critical",
                title="Poor ATS Compatibility",
                description=f"ATS compatibility score: {ats_analysis['ats_score']}/100",
                suggestion="Address ATS issues to ensure your resume passes automated screening.",
                examples=ats_analysis['recommendations'][:3],
                priority=10
            ))
        elif ats_analysis['ats_score'] < 85:
            feedback.append(FeedbackItem(
                category="ats",
                severity="important",
                title="Moderate ATS Compatibility",
                description=f"ATS compatibility score: {ats_analysis['ats_score']}/100",
                suggestion="Improve ATS compatibility for better automated screening results.",
                examples=ats_analysis['recommendations'][:2],
                priority=6
            ))
        
        return feedback

    def _analyze_professional_impact(self, resume_text: str) -> List[FeedbackItem]:
        """Analyze professional impact and achievement presentation"""
        
        feedback = []
        
        # Check for leadership indicators
        leadership_terms = ['led', 'managed', 'directed', 'supervised', 'mentored', 'coordinated']
        leadership_count = sum(1 for term in leadership_terms if term in resume_text.lower())
        
        if leadership_count == 0:
            feedback.append(FeedbackItem(
                category="impact",
                severity="suggestion",
                title="Limited Leadership Examples",
                description="No clear leadership or management experience mentioned.",
                suggestion="Highlight any leadership roles, team management, or mentoring experience.",
                examples=["Led team of 5 developers", "Mentored junior staff", "Coordinated cross-functional projects"],
                priority=5
            ))
        
        # Check for problem-solving examples
        problem_solving_terms = ['solved', 'resolved', 'improved', 'optimized', 'streamlined', 'enhanced']
        problem_solving_count = sum(1 for term in problem_solving_terms if term in resume_text.lower())
        
        if problem_solving_count < 2:
            feedback.append(FeedbackItem(
                category="impact",
                severity="important",
                title="Limited Problem-Solving Examples",
                description="Few examples of problem-solving or process improvement.",
                suggestion="Include specific examples of problems you solved and improvements you made.",
                examples=["Resolved critical system issues", "Improved process efficiency by 40%", "Streamlined workflow reducing errors by 25%"],
                priority=6
            ))
        
        return feedback

    def _analyze_industry_alignment(self, resume_text: str, target_role: str) -> List[FeedbackItem]:
        """Analyze alignment with target industry/role"""
        
        feedback = []
        
        # Determine industry from target role
        role_lower = target_role.lower()
        industry = None
        
        if any(term in role_lower for term in ['software', 'developer', 'engineer', 'programmer']):
            industry = 'software_engineering'
        elif any(term in role_lower for term in ['data', 'analyst', 'scientist', 'ml', 'ai']):
            industry = 'data_science'
        elif any(term in role_lower for term in ['product', 'manager', 'pm']):
            industry = 'product_management'
        elif any(term in role_lower for term in ['marketing', 'digital', 'campaign']):
            industry = 'marketing'
        
        if industry and industry in self.industry_keywords:
            relevant_keywords = self.industry_keywords[industry]
            found_keywords = [kw for kw in relevant_keywords if kw in resume_text.lower()]
            
            if len(found_keywords) < len(relevant_keywords) * 0.3:
                feedback.append(FeedbackItem(
                    category="industry",
                    severity="important",
                    title=f"Limited {industry.replace('_', ' ').title()} Keywords",
                    description=f"Your resume has few keywords relevant to {target_role}.",
                    suggestion=f"Include more {industry.replace('_', ' ')} specific terms and concepts.",
                    examples=[kw for kw in relevant_keywords if kw not in found_keywords][:5],
                    priority=7
                ))
        
        return feedback

    def _calculate_overall_score(self, feedback_items: List[FeedbackItem], resume_text: str) -> float:
        """Calculate overall resume score"""
        
        base_score = 100.0
        
        # Deduct points based on feedback severity
        for item in feedback_items:
            if item.severity == 'critical':
                base_score -= 15
            elif item.severity == 'important':
                base_score -= 8
            elif item.severity == 'suggestion':
                base_score -= 3
        
        # Bonus points for positive indicators
        word_count = len(resume_text.split())
        if 300 <= word_count <= 600:  # Optimal length
            base_score += 5
        
        # Check for quantifiable achievements
        numbers_pattern = r'\d+(?:\.\d+)?(?:%|k|K|million|M|thousand|\+)?'
        numbers_found = len(re.findall(numbers_pattern, resume_text))
        if numbers_found >= 5:
            base_score += 10
        
        # Check for action words
        action_word_count = sum(1 for word in self.strong_action_words 
                               if word in resume_text.lower())
        if action_word_count >= 8:
            base_score += 5
        
        return max(0.0, min(100.0, base_score))

    def _identify_strengths_weaknesses(self, feedback_items: List[FeedbackItem], resume_text: str) -> Tuple[List[str], List[str]]:
        """Identify resume strengths and weaknesses"""
        
        strengths = []
        weaknesses = []
        
        # Analyze for strengths
        word_count = len(resume_text.split())
        if 300 <= word_count <= 600:
            strengths.append("Appropriate resume length")
        
        numbers_found = len(re.findall(r'\d+(?:\.\d+)?(?:%|k|K|million|M|thousand|\+)?', resume_text))
        if numbers_found >= 3:
            strengths.append("Includes quantifiable achievements")
        
        action_word_count = sum(1 for word in self.strong_action_words if word in resume_text.lower())
        if action_word_count >= 5:
            strengths.append("Uses strong action words")
        
        # Identify weaknesses from critical/important feedback
        critical_issues = [item for item in feedback_items if item.severity == 'critical']
        important_issues = [item for item in feedback_items if item.severity == 'important']
        
        for item in critical_issues[:3]:  # Top 3 critical issues
            weaknesses.append(item.title)
        
        for item in important_issues[:2]:  # Top 2 important issues
            weaknesses.append(item.title)
        
        return strengths, weaknesses

    def _generate_content_suggestions(self, resume_text: str, job_description: str = None) -> List[str]:
        """Generate specific content improvement suggestions"""
        
        suggestions = []
        
        # Length-based suggestions
        word_count = len(resume_text.split())
        if word_count < 250:
            suggestions.append("Add more detailed descriptions of your key achievements and responsibilities")
        
        # Structure suggestions
        if 'summary' not in resume_text.lower() and 'objective' not in resume_text.lower():
            suggestions.append("Add a professional summary at the top highlighting your key qualifications")
        
        # Content enhancement suggestions
        if len(re.findall(r'\d+', resume_text)) < 3:
            suggestions.append("Include specific numbers, percentages, and metrics to quantify your impact")
        
        # Industry-specific suggestions
        if job_description:
            job_words = set(re.findall(r'\b\w{4,}\b', job_description.lower()))
            resume_words = set(re.findall(r'\b\w{4,}\b', resume_text.lower()))
            missing_important = job_words - resume_words
            
            if missing_important:
                suggestions.append(f"Consider incorporating these job-relevant terms: {', '.join(list(missing_important)[:5])}")
        
        return suggestions

    def generate_improvement_report(self, analysis: ResumeAnalysis) -> str:
        """Generate a comprehensive improvement report"""
        
        report = f"""
RESUME ANALYSIS REPORT
=====================

OVERALL SCORE: {analysis.overall_score:.1f}/100

STRENGTHS:
{chr(10).join(['✓ ' + strength for strength in analysis.strengths])}

AREAS FOR IMPROVEMENT:
{chr(10).join(['✗ ' + weakness for weakness in analysis.weaknesses])}

PRIORITY ACTIONS:
{chr(10).join([f"{i+1}. {item.title}: {item.suggestion}" 
               for i, item in enumerate(analysis.feedback_items[:5])])}

ATS COMPATIBILITY: {analysis.ats_compatibility.get('ats_score', 'N/A')}/100

KEYWORD OPTIMIZATION:
- Technical Keywords Found: {len(analysis.keyword_optimization.get('technical_keywords', []))}
- Job Match Score: {analysis.keyword_optimization.get('job_match_score', 0):.1%}

CONTENT SUGGESTIONS:
{chr(10).join(['• ' + suggestion for suggestion in analysis.content_suggestions[:3]])}
        """
        
        return report.strip()

    def export_feedback(self, analysis: ResumeAnalysis, format: str = 'json') -> str:
        """Export feedback in specified format"""
        
        if format == 'json':
            return json.dumps(asdict(analysis), indent=2, default=str)
        elif format == 'report':
            return self.generate_improvement_report(analysis)
        else:
            return str(analysis)
