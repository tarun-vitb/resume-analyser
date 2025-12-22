"""
Comprehensive Skill Gap Detection and Analysis System
Identifies missing skills, skill levels, and provides intelligent recommendations
"""

import re
import json
import logging
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, asdict
from pathlib import Path
import numpy as np
from collections import defaultdict, Counter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class SkillMatch:
    """Represents a skill match between resume and job requirements"""
    skill: str
    category: str
    confidence: float
    found_in_resume: bool
    importance: float  # 0-1 scale based on job requirements
    alternatives: List[str] = None  # Alternative/related skills found

@dataclass
class SkillGapAnalysis:
    """Complete skill gap analysis results"""
    matched_skills: List[SkillMatch]
    missing_skills: List[SkillMatch]
    skill_categories: Dict[str, List[str]]
    overall_match_score: float
    critical_gaps: List[str]
    recommendations: List[str]
    skill_level_assessment: Dict[str, str]  # skill -> level (beginner/intermediate/advanced)

class SkillAnalyzer:
    """Advanced skill detection and gap analysis system"""
    
    def __init__(self):
        """Initialize with comprehensive skill database"""
        
        # Load comprehensive skill database
        self.skill_database = self._load_skill_database()
        
        # Skill categories with hierarchical relationships
        self.skill_categories = {
            'programming_languages': {
                'primary': ['Python', 'Java', 'JavaScript', 'C++', 'C#', 'Go', 'Rust', 'Swift', 'Kotlin'],
                'web': ['HTML', 'CSS', 'TypeScript', 'PHP', 'Ruby'],
                'data': ['R', 'SQL', 'Scala', 'Julia', 'MATLAB'],
                'mobile': ['Swift', 'Kotlin', 'Dart', 'Objective-C'],
                'systems': ['C', 'C++', 'Rust', 'Assembly', 'Go']
            },
            'frameworks_libraries': {
                'web_frontend': ['React', 'Angular', 'Vue.js', 'Svelte', 'Next.js', 'Nuxt.js'],
                'web_backend': ['Django', 'Flask', 'Express.js', 'Spring', 'Laravel', 'Ruby on Rails'],
                'mobile': ['React Native', 'Flutter', 'Xamarin', 'Ionic'],
                'data_science': ['Pandas', 'NumPy', 'Scikit-learn', 'TensorFlow', 'PyTorch', 'Keras'],
                'testing': ['Jest', 'Pytest', 'JUnit', 'Selenium', 'Cypress']
            },
            'databases': {
                'relational': ['MySQL', 'PostgreSQL', 'SQLite', 'Oracle', 'SQL Server'],
                'nosql': ['MongoDB', 'Redis', 'Cassandra', 'DynamoDB', 'Neo4j'],
                'big_data': ['Hadoop', 'Spark', 'Kafka', 'Elasticsearch']
            },
            'cloud_devops': {
                'cloud_platforms': ['AWS', 'Azure', 'Google Cloud', 'IBM Cloud'],
                'containers': ['Docker', 'Kubernetes', 'OpenShift'],
                'ci_cd': ['Jenkins', 'GitLab CI', 'GitHub Actions', 'Travis CI'],
                'infrastructure': ['Terraform', 'Ansible', 'Chef', 'Puppet'],
                'monitoring': ['Prometheus', 'Grafana', 'ELK Stack', 'New Relic']
            },
            'data_ai_ml': {
                'machine_learning': ['Machine Learning', 'Deep Learning', 'Neural Networks', 'Computer Vision', 'NLP'],
                'data_processing': ['ETL', 'Data Pipeline', 'Apache Airflow', 'Apache Spark'],
                'analytics': ['Data Analysis', 'Statistical Analysis', 'A/B Testing', 'Business Intelligence'],
                'tools': ['Jupyter', 'Tableau', 'Power BI', 'Apache Superset']
            },
            'soft_skills': {
                'leadership': ['Team Leadership', 'Project Management', 'Mentoring', 'Strategic Planning'],
                'communication': ['Technical Writing', 'Presentation Skills', 'Cross-functional Collaboration'],
                'problem_solving': ['Analytical Thinking', 'Creative Problem Solving', 'Debugging', 'Troubleshooting'],
                'agile': ['Scrum', 'Kanban', 'Agile Methodology', 'Sprint Planning']
            },
            'tools_platforms': {
                'version_control': ['Git', 'GitHub', 'GitLab', 'Bitbucket', 'SVN'],
                'ides': ['VS Code', 'IntelliJ', 'Eclipse', 'PyCharm', 'Xcode'],
                'design': ['Figma', 'Adobe XD', 'Sketch', 'Photoshop', 'Illustrator'],
                'project_management': ['Jira', 'Trello', 'Asana', 'Monday.com', 'Notion']
            }
        }
        
        # Skill synonyms and variations
        self.skill_synonyms = {
            'JavaScript': ['JS', 'Javascript', 'ECMAScript'],
            'TypeScript': ['TS', 'Typescript'],
            'React': ['ReactJS', 'React.js'],
            'Angular': ['AngularJS', 'Angular.js'],
            'Vue.js': ['Vue', 'VueJS'],
            'Node.js': ['NodeJS', 'Node'],
            'Express.js': ['Express', 'ExpressJS'],
            'MongoDB': ['Mongo', 'Mongo DB'],
            'PostgreSQL': ['Postgres', 'PostGres'],
            'Machine Learning': ['ML', 'Machine-Learning'],
            'Deep Learning': ['DL', 'Deep-Learning'],
            'Natural Language Processing': ['NLP', 'Natural Language Processing'],
            'Computer Vision': ['CV', 'Image Processing'],
            'Amazon Web Services': ['AWS'],
            'Google Cloud Platform': ['GCP', 'Google Cloud'],
            'Microsoft Azure': ['Azure']
        }
        
        # Skill importance weights based on job market demand
        self.skill_importance = {
            'Python': 0.95, 'JavaScript': 0.90, 'React': 0.85, 'AWS': 0.90,
            'Docker': 0.80, 'Kubernetes': 0.75, 'Machine Learning': 0.85,
            'SQL': 0.90, 'Git': 0.95, 'Node.js': 0.80, 'Angular': 0.75,
            'Java': 0.85, 'C++': 0.70, 'MongoDB': 0.70, 'PostgreSQL': 0.75
        }

    def _load_skill_database(self) -> Dict[str, Dict]:
        """Load or create comprehensive skill database"""
        
        # This could be loaded from a JSON file in production
        # For now, we'll create it programmatically
        
        skill_db = {
            'technical_skills': {
                'programming': [
                    'Python', 'Java', 'JavaScript', 'TypeScript', 'C++', 'C#', 'Go', 'Rust',
                    'Swift', 'Kotlin', 'PHP', 'Ruby', 'R', 'Scala', 'HTML', 'CSS'
                ],
                'frameworks': [
                    'React', 'Angular', 'Vue.js', 'Django', 'Flask', 'Spring', 'Express.js',
                    'Laravel', 'Ruby on Rails', 'Next.js', 'Nuxt.js', 'React Native', 'Flutter'
                ],
                'databases': [
                    'MySQL', 'PostgreSQL', 'MongoDB', 'Redis', 'SQLite', 'Oracle',
                    'Cassandra', 'DynamoDB', 'Neo4j', 'Elasticsearch'
                ],
                'cloud': [
                    'AWS', 'Azure', 'Google Cloud', 'Docker', 'Kubernetes', 'Jenkins',
                    'Terraform', 'Ansible', 'GitLab CI', 'GitHub Actions'
                ],
                'data_science': [
                    'Machine Learning', 'Deep Learning', 'Data Science', 'Pandas', 'NumPy',
                    'Scikit-learn', 'TensorFlow', 'PyTorch', 'Jupyter', 'Tableau'
                ]
            },
            'soft_skills': [
                'Leadership', 'Communication', 'Problem Solving', 'Team Collaboration',
                'Project Management', 'Analytical Thinking', 'Creativity', 'Adaptability'
            ],
            'certifications': [
                'AWS Certified', 'Google Cloud Certified', 'Microsoft Certified',
                'Cisco Certified', 'CompTIA', 'PMP', 'Scrum Master', 'Six Sigma'
            ]
        }
        
        return skill_db

    def normalize_skill_name(self, skill: str) -> str:
        """Normalize skill name to standard format"""
        skill = skill.strip()
        
        # Check synonyms
        for standard_name, synonyms in self.skill_synonyms.items():
            if skill.lower() in [s.lower() for s in synonyms]:
                return standard_name
        
        # Basic normalization
        skill = re.sub(r'[^\w\s.-]', '', skill)
        skill = ' '.join(word.capitalize() for word in skill.split())
        
        return skill

    def extract_skills_from_text(self, text: str) -> Dict[str, List[Tuple[str, float]]]:
        """Extract skills from text with confidence scores"""
        
        text_lower = text.lower()
        found_skills = defaultdict(list)
        
        # Extract skills by category
        for main_category, subcategories in self.skill_categories.items():
            if isinstance(subcategories, dict):
                for sub_category, skills in subcategories.items():
                    for skill in skills:
                        confidence = self._calculate_skill_confidence(skill, text_lower)
                        if confidence > 0.3:  # Threshold for skill detection
                            found_skills[main_category].append((skill, confidence))
            else:
                for skill in subcategories:
                    confidence = self._calculate_skill_confidence(skill, text_lower)
                    if confidence > 0.3:
                        found_skills[main_category].append((skill, confidence))
        
        # Sort by confidence
        for category in found_skills:
            found_skills[category].sort(key=lambda x: x[1], reverse=True)
        
        return dict(found_skills)

    def _calculate_skill_confidence(self, skill: str, text: str) -> float:
        """Calculate confidence score for skill detection"""
        
        skill_lower = skill.lower()
        confidence = 0.0
        
        # Exact match (highest confidence)
        if skill_lower in text:
            confidence = 0.9
        
        # Check synonyms
        synonyms = self.skill_synonyms.get(skill, [])
        for synonym in synonyms:
            if synonym.lower() in text:
                confidence = max(confidence, 0.8)
        
        # Partial match with word boundaries
        skill_words = skill_lower.split()
        if len(skill_words) > 1:
            # Multi-word skill
            pattern = r'\b' + r'\s+'.join(skill_words) + r'\b'
            if re.search(pattern, text):
                confidence = max(confidence, 0.85)
        else:
            # Single word skill with word boundaries
            pattern = r'\b' + skill_lower + r'\b'
            if re.search(pattern, text):
                confidence = max(confidence, 0.7)
        
        # Context-based confidence adjustment
        context_patterns = {
            'experience': [r'experience\s+with\s+' + skill_lower, r'worked\s+with\s+' + skill_lower],
            'proficient': [r'proficient\s+in\s+' + skill_lower, r'expert\s+in\s+' + skill_lower],
            'years': [r'\d+\s+years?\s+of\s+' + skill_lower, skill_lower + r'\s+for\s+\d+\s+years?']
        }
        
        for context_type, patterns in context_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    confidence = min(1.0, confidence + 0.1)
        
        return confidence

    def extract_job_requirements(self, job_description: str) -> Dict[str, List[Tuple[str, float]]]:
        """Extract required skills from job description with importance scores"""
        
        # Preprocess job description
        job_desc_lower = job_description.lower()
        
        # Extract skills
        required_skills = self.extract_skills_from_text(job_description)
        
        # Adjust importance based on context in job description
        for category, skills in required_skills.items():
            adjusted_skills = []
            for skill, confidence in skills:
                importance = self._calculate_skill_importance(skill, job_desc_lower)
                adjusted_skills.append((skill, importance))
            required_skills[category] = adjusted_skills
        
        return required_skills

    def _calculate_skill_importance(self, skill: str, job_description: str) -> float:
        """Calculate skill importance based on job description context"""
        
        skill_lower = skill.lower()
        base_importance = self.skill_importance.get(skill, 0.5)
        
        # Context-based importance adjustment
        importance_indicators = {
            'required': [r'required?\s*:?\s*.*' + skill_lower, r'must\s+have.*' + skill_lower],
            'preferred': [r'preferred?\s*:?\s*.*' + skill_lower, r'nice\s+to\s+have.*' + skill_lower],
            'essential': [r'essential.*' + skill_lower, r'critical.*' + skill_lower],
            'experience': [r'\d+\+?\s+years?\s+.*' + skill_lower, skill_lower + r'.*\d+\+?\s+years?']
        }
        
        importance_multipliers = {
            'required': 1.2,
            'essential': 1.3,
            'experience': 1.1,
            'preferred': 0.9
        }
        
        final_importance = base_importance
        
        for indicator_type, patterns in importance_indicators.items():
            for pattern in patterns:
                if re.search(pattern, job_description):
                    multiplier = importance_multipliers.get(indicator_type, 1.0)
                    final_importance *= multiplier
                    break
        
        return min(1.0, final_importance)

    def analyze_skill_gaps(self, 
                          resume_text: str, 
                          job_description: str,
                          resume_skills: Optional[List[str]] = None) -> SkillGapAnalysis:
        """Perform comprehensive skill gap analysis"""
        
        # Extract skills from resume
        resume_skill_matches = self.extract_skills_from_text(resume_text)
        
        # Extract requirements from job description
        job_requirements = self.extract_job_requirements(job_description)
        
        # Flatten skills for easier comparison
        resume_skills_flat = set()
        for category, skills in resume_skill_matches.items():
            for skill, _ in skills:
                resume_skills_flat.add(skill.lower())
        
        # Add manually provided skills
        if resume_skills:
            for skill in resume_skills:
                resume_skills_flat.add(skill.lower())
        
        matched_skills = []
        missing_skills = []
        skill_categories = defaultdict(list)
        
        # Analyze each required skill
        for category, required_skills in job_requirements.items():
            for skill, importance in required_skills:
                skill_lower = skill.lower()
                
                # Check if skill is present in resume
                is_present = (skill_lower in resume_skills_flat or 
                            any(synonym.lower() in resume_skills_flat 
                                for synonym in self.skill_synonyms.get(skill, [])))
                
                # Find alternatives/related skills
                alternatives = self._find_alternative_skills(skill, resume_skills_flat)
                
                skill_match = SkillMatch(
                    skill=skill,
                    category=category,
                    confidence=importance,
                    found_in_resume=is_present,
                    importance=importance,
                    alternatives=alternatives
                )
                
                if is_present:
                    matched_skills.append(skill_match)
                    skill_categories['matched'].append(skill)
                else:
                    missing_skills.append(skill_match)
                    skill_categories['missing'].append(skill)
        
        # Calculate overall match score
        total_importance = sum(skill.importance for skill in matched_skills + missing_skills)
        matched_importance = sum(skill.importance for skill in matched_skills)
        overall_match_score = matched_importance / total_importance if total_importance > 0 else 0
        
        # Identify critical gaps (high importance missing skills)
        critical_gaps = [
            skill.skill for skill in missing_skills 
            if skill.importance > 0.7
        ]
        
        # Generate recommendations
        recommendations = self._generate_skill_recommendations(
            missing_skills, matched_skills, critical_gaps
        )
        
        # Assess skill levels
        skill_level_assessment = self._assess_skill_levels(resume_text, matched_skills)
        
        return SkillGapAnalysis(
            matched_skills=matched_skills,
            missing_skills=missing_skills,
            skill_categories=dict(skill_categories),
            overall_match_score=overall_match_score,
            critical_gaps=critical_gaps,
            recommendations=recommendations,
            skill_level_assessment=skill_level_assessment
        )

    def _find_alternative_skills(self, target_skill: str, resume_skills: Set[str]) -> List[str]:
        """Find alternative or related skills in resume"""
        
        alternatives = []
        target_lower = target_skill.lower()
        
        # Define skill relationships
        skill_relationships = {
            'react': ['angular', 'vue.js', 'javascript', 'typescript'],
            'angular': ['react', 'vue.js', 'typescript', 'javascript'],
            'vue.js': ['react', 'angular', 'javascript', 'typescript'],
            'python': ['java', 'javascript', 'c++', 'go'],
            'mysql': ['postgresql', 'sqlite', 'oracle', 'sql server'],
            'mongodb': ['redis', 'cassandra', 'dynamodb'],
            'aws': ['azure', 'google cloud', 'docker', 'kubernetes'],
            'docker': ['kubernetes', 'aws', 'azure', 'containerization'],
            'machine learning': ['deep learning', 'data science', 'ai', 'tensorflow', 'pytorch']
        }
        
        related_skills = skill_relationships.get(target_lower, [])
        
        for skill in resume_skills:
            if skill in related_skills:
                alternatives.append(skill)
        
        return alternatives

    def _generate_skill_recommendations(self, 
                                     missing_skills: List[SkillMatch],
                                     matched_skills: List[SkillMatch],
                                     critical_gaps: List[str]) -> List[str]:
        """Generate actionable skill improvement recommendations"""
        
        recommendations = []
        
        # Critical skills recommendations
        if critical_gaps:
            recommendations.append(
                f"Priority: Focus on acquiring these critical skills: {', '.join(critical_gaps[:3])}"
            )
        
        # Category-based recommendations
        missing_by_category = defaultdict(list)
        for skill in missing_skills:
            missing_by_category[skill.category].append(skill.skill)
        
        for category, skills in missing_by_category.items():
            if len(skills) >= 2:
                recommendations.append(
                    f"Consider strengthening your {category.replace('_', ' ')} skills, "
                    f"particularly: {', '.join(skills[:2])}"
                )
        
        # Skill level improvement recommendations
        matched_skill_names = [skill.skill for skill in matched_skills]
        if len(matched_skill_names) > 0:
            recommendations.append(
                f"Enhance your existing skills in {', '.join(matched_skill_names[:3])} "
                "by working on advanced projects or obtaining certifications"
            )
        
        # Alternative skills recommendations
        alternatives_found = []
        for skill in missing_skills:
            if skill.alternatives:
                alternatives_found.extend(skill.alternatives)
        
        if alternatives_found:
            recommendations.append(
                f"Leverage your experience in {', '.join(set(alternatives_found[:2]))} "
                "to transition into the missing skills"
            )
        
        return recommendations

    def _assess_skill_levels(self, 
                           resume_text: str, 
                           matched_skills: List[SkillMatch]) -> Dict[str, str]:
        """Assess skill levels based on resume context"""
        
        skill_levels = {}
        resume_lower = resume_text.lower()
        
        for skill_match in matched_skills:
            skill = skill_match.skill
            skill_lower = skill.lower()
            
            # Look for experience indicators
            level_indicators = {
                'advanced': [
                    f'expert in {skill_lower}',
                    f'senior {skill_lower}',
                    f'lead {skill_lower}',
                    f'{skill_lower} architect',
                    f'mastery of {skill_lower}',
                    f'\\d+\\+? years of {skill_lower}'
                ],
                'intermediate': [
                    f'proficient in {skill_lower}',
                    f'experienced with {skill_lower}',
                    f'solid understanding of {skill_lower}',
                    f'worked with {skill_lower}',
                    f'familiar with {skill_lower}'
                ],
                'beginner': [
                    f'basic {skill_lower}',
                    f'introduction to {skill_lower}',
                    f'learning {skill_lower}',
                    f'exposure to {skill_lower}'
                ]
            }
            
            detected_level = 'intermediate'  # Default
            
            for level, patterns in level_indicators.items():
                for pattern in patterns:
                    if re.search(pattern, resume_lower):
                        detected_level = level
                        break
                if detected_level == level:
                    break
            
            skill_levels[skill] = detected_level
        
        return skill_levels

    def get_skill_learning_path(self, missing_skill: str) -> Dict[str, List[str]]:
        """Generate learning path for a missing skill"""
        
        learning_paths = {
            'React': {
                'prerequisites': ['JavaScript', 'HTML', 'CSS'],
                'core_concepts': ['Components', 'JSX', 'State Management', 'Props', 'Hooks'],
                'advanced_topics': ['Redux', 'Context API', 'Testing', 'Performance Optimization'],
                'projects': ['Todo App', 'Weather App', 'E-commerce Site']
            },
            'Python': {
                'prerequisites': ['Programming Basics'],
                'core_concepts': ['Syntax', 'Data Types', 'Functions', 'OOP', 'Modules'],
                'advanced_topics': ['Web Frameworks', 'Data Science', 'Machine Learning'],
                'projects': ['Calculator', 'Web Scraper', 'API Development']
            },
            'AWS': {
                'prerequisites': ['Cloud Computing Basics', 'Linux'],
                'core_concepts': ['EC2', 'S3', 'IAM', 'VPC', 'Lambda'],
                'advanced_topics': ['EKS', 'CloudFormation', 'DevOps', 'Security'],
                'projects': ['Static Website Hosting', 'Serverless API', 'CI/CD Pipeline']
            },
            'Machine Learning': {
                'prerequisites': ['Python', 'Statistics', 'Linear Algebra'],
                'core_concepts': ['Supervised Learning', 'Unsupervised Learning', 'Model Evaluation'],
                'advanced_topics': ['Deep Learning', 'NLP', 'Computer Vision'],
                'projects': ['Iris Classification', 'House Price Prediction', 'Image Recognition']
            }
        }
        
        return learning_paths.get(missing_skill, {
            'prerequisites': ['Research the skill requirements'],
            'core_concepts': ['Start with fundamentals'],
            'advanced_topics': ['Explore advanced applications'],
            'projects': ['Build practical projects']
        })

    def export_analysis(self, analysis: SkillGapAnalysis, format: str = 'json') -> str:
        """Export skill gap analysis in specified format"""
        
        if format == 'json':
            return json.dumps(asdict(analysis), indent=2, default=str)
        elif format == 'summary':
            summary = f"""
SKILL GAP ANALYSIS SUMMARY
==========================

Overall Match Score: {analysis.overall_match_score:.1%}

MATCHED SKILLS ({len(analysis.matched_skills)}):
{', '.join([skill.skill for skill in analysis.matched_skills])}

MISSING SKILLS ({len(analysis.missing_skills)}):
{', '.join([skill.skill for skill in analysis.missing_skills])}

CRITICAL GAPS:
{', '.join(analysis.critical_gaps) if analysis.critical_gaps else 'None'}

TOP RECOMMENDATIONS:
{chr(10).join(['- ' + rec for rec in analysis.recommendations[:3]])}
            """
            return summary.strip()
        
        return str(analysis)
