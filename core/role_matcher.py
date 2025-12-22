"""
Role Matching System for Multiple Job Descriptions
Compares resumes against multiple job descriptions and ranks matches
"""

import logging
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
import numpy as np
from collections import defaultdict
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class JobMatch:
    """Represents a match between resume and job description"""
    job_id: str
    job_title: str
    company: str
    match_score: float
    skill_overlap: float
    experience_match: float
    education_match: float
    semantic_similarity: float
    missing_skills: List[str]
    matched_skills: List[str]
    selection_probability: float
    recommendation: str
    priority_level: str  # 'high', 'medium', 'low'

@dataclass
class RoleMatchingResults:
    """Complete role matching analysis results"""
    total_jobs_analyzed: int
    best_matches: List[JobMatch]
    skill_gap_summary: Dict[str, int]
    recommended_actions: List[str]
    career_insights: Dict[str, Any]
    match_distribution: Dict[str, int]

class RoleMatcher:
    """Advanced role matching system for job recommendation"""
    
    def __init__(self, nlp_engine, skill_analyzer, prediction_model):
        """Initialize with required engines"""
        self.nlp_engine = nlp_engine
        self.skill_analyzer = skill_analyzer
        self.prediction_model = prediction_model
        
        # Job categories and their typical requirements
        self.job_categories = {
            'software_engineer': {
                'required_skills': ['programming', 'algorithms', 'data structures'],
                'preferred_skills': ['system design', 'testing', 'version control'],
                'experience_weight': 0.3,
                'skills_weight': 0.4,
                'education_weight': 0.2,
                'other_weight': 0.1
            },
            'data_scientist': {
                'required_skills': ['statistics', 'machine learning', 'programming'],
                'preferred_skills': ['data visualization', 'big data', 'domain expertise'],
                'experience_weight': 0.25,
                'skills_weight': 0.45,
                'education_weight': 0.25,
                'other_weight': 0.05
            },
            'product_manager': {
                'required_skills': ['product strategy', 'stakeholder management', 'analytics'],
                'preferred_skills': ['technical background', 'user research', 'agile'],
                'experience_weight': 0.4,
                'skills_weight': 0.3,
                'education_weight': 0.15,
                'other_weight': 0.15
            },
            'devops_engineer': {
                'required_skills': ['cloud platforms', 'automation', 'containerization'],
                'preferred_skills': ['monitoring', 'security', 'scripting'],
                'experience_weight': 0.35,
                'skills_weight': 0.4,
                'education_weight': 0.15,
                'other_weight': 0.1
            }
        }
        
        # Industry salary ranges (for prioritization)
        self.salary_ranges = {
            'software_engineer': {'min': 80000, 'max': 200000, 'median': 120000},
            'data_scientist': {'min': 90000, 'max': 250000, 'median': 140000},
            'product_manager': {'min': 100000, 'max': 300000, 'median': 150000},
            'devops_engineer': {'min': 85000, 'max': 220000, 'median': 130000},
            'marketing_manager': {'min': 70000, 'max': 180000, 'median': 100000}
        }

    def analyze_multiple_jobs(self, 
                            resume_data: Dict[str, Any],
                            job_descriptions: List[Dict[str, str]],
                            prioritize_by: str = 'match_score') -> RoleMatchingResults:
        """Analyze resume against multiple job descriptions"""
        
        job_matches = []
        skill_gaps = defaultdict(int)
        
        logger.info(f"Analyzing resume against {len(job_descriptions)} job descriptions")
        
        for job in job_descriptions:
            try:
                match = self._analyze_single_job_match(resume_data, job)
                job_matches.append(match)
                
                # Aggregate skill gaps
                for skill in match.missing_skills:
                    skill_gaps[skill] += 1
                    
            except Exception as e:
                logger.error(f"Error analyzing job {job.get('job_id', 'unknown')}: {e}")
                continue
        
        # Sort matches based on prioritization criteria
        if prioritize_by == 'match_score':
            job_matches.sort(key=lambda x: x.match_score, reverse=True)
        elif prioritize_by == 'selection_probability':
            job_matches.sort(key=lambda x: x.selection_probability, reverse=True)
        elif prioritize_by == 'skill_overlap':
            job_matches.sort(key=lambda x: x.skill_overlap, reverse=True)
        
        # Generate insights and recommendations
        career_insights = self._generate_career_insights(job_matches, resume_data)
        recommended_actions = self._generate_recommended_actions(job_matches, skill_gaps)
        match_distribution = self._calculate_match_distribution(job_matches)
        
        return RoleMatchingResults(
            total_jobs_analyzed=len(job_descriptions),
            best_matches=job_matches,
            skill_gap_summary=dict(skill_gaps),
            recommended_actions=recommended_actions,
            career_insights=career_insights,
            match_distribution=match_distribution
        )

    def _analyze_single_job_match(self, resume_data: Dict[str, Any], job: Dict[str, str]) -> JobMatch:
        """Analyze match between resume and single job description"""
        
        job_id = job.get('job_id', f"job_{hash(job.get('description', ''))}")
        job_title = job.get('title', 'Unknown Position')
        company = job.get('company', 'Unknown Company')
        job_description = job.get('description', '')
        
        resume_text = resume_data.get('cleaned_text', '')
        
        # 1. Calculate semantic similarity
        semantic_similarity = self.nlp_engine.compute_semantic_similarity(
            resume_text, job_description
        )
        
        # 2. Analyze skill gaps
        skill_analysis = self.skill_analyzer.analyze_skill_gaps(
            resume_text, job_description, resume_data.get('skills', [])
        )
        
        # 3. Calculate component scores
        skill_overlap = self._calculate_skill_overlap(skill_analysis)
        experience_match = self._calculate_experience_match(resume_data, job_description)
        education_match = self._calculate_education_match(resume_data, job_description)
        
        # 4. Calculate overall match score
        match_score = self._calculate_weighted_match_score(
            semantic_similarity, skill_overlap, experience_match, 
            education_match, job_title
        )
        
        # 5. Predict selection probability
        selection_probability = self._predict_selection_probability(
            resume_data, job_description, skill_analysis, match_score
        )
        
        # 6. Generate recommendation and priority
        recommendation, priority_level = self._generate_job_recommendation(
            match_score, selection_probability, skill_analysis
        )
        
        return JobMatch(
            job_id=job_id,
            job_title=job_title,
            company=company,
            match_score=match_score,
            skill_overlap=skill_overlap,
            experience_match=experience_match,
            education_match=education_match,
            semantic_similarity=semantic_similarity,
            missing_skills=skill_analysis.critical_gaps + 
                          [skill.skill for skill in skill_analysis.missing_skills[:5]],
            matched_skills=[skill.skill for skill in skill_analysis.matched_skills],
            selection_probability=selection_probability,
            recommendation=recommendation,
            priority_level=priority_level
        )

    def _calculate_skill_overlap(self, skill_analysis) -> float:
        """Calculate skill overlap percentage"""
        
        total_skills = len(skill_analysis.matched_skills) + len(skill_analysis.missing_skills)
        if total_skills == 0:
            return 0.0
        
        return len(skill_analysis.matched_skills) / total_skills

    def _calculate_experience_match(self, resume_data: Dict[str, Any], job_description: str) -> float:
        """Calculate experience match score"""
        
        experience_list = resume_data.get('experience', [])
        if not experience_list:
            return 0.0
        
        experience_text = ' '.join(experience_list).lower()
        job_desc_lower = job_description.lower()
        
        # Extract years of experience required
        import re
        years_required_pattern = r'(\d+)\+?\s*years?\s*(?:of\s+)?(?:experience|exp)'
        years_matches = re.findall(years_required_pattern, job_desc_lower)
        
        required_years = 0
        if years_matches:
            required_years = int(years_matches[0])
        
        # Estimate candidate's years of experience
        candidate_years = self._estimate_years_experience(experience_list)
        
        # Calculate experience match
        if required_years == 0:
            experience_score = 0.7  # No specific requirement
        elif candidate_years >= required_years:
            experience_score = 1.0
        elif candidate_years >= required_years * 0.7:
            experience_score = 0.8
        else:
            experience_score = candidate_years / required_years
        
        # Check for relevant experience keywords
        job_keywords = set(re.findall(r'\b\w{4,}\b', job_desc_lower))
        exp_keywords = set(re.findall(r'\b\w{4,}\b', experience_text))
        
        keyword_overlap = len(job_keywords & exp_keywords) / len(job_keywords) if job_keywords else 0
        
        # Combine experience length and relevance
        final_score = (experience_score * 0.6) + (keyword_overlap * 0.4)
        
        return min(1.0, final_score)

    def _calculate_education_match(self, resume_data: Dict[str, Any], job_description: str) -> float:
        """Calculate education match score"""
        
        education_list = resume_data.get('education', [])
        if not education_list:
            return 0.3  # Some score for missing education
        
        education_text = ' '.join(education_list).lower()
        job_desc_lower = job_description.lower()
        
        # Education level mapping
        education_levels = {
            'phd': 4, 'doctorate': 4, 'ph.d': 4,
            'master': 3, 'mba': 3, 'ms': 3, 'ma': 3,
            'bachelor': 2, 'bs': 2, 'ba': 2, 'btech': 2, 'be': 2,
            'associate': 1, 'diploma': 1, 'certificate': 1
        }
        
        # Determine candidate's education level
        candidate_level = 0
        for degree, level in education_levels.items():
            if degree in education_text:
                candidate_level = max(candidate_level, level)
        
        # Determine required education level
        required_level = 0
        for degree, level in education_levels.items():
            if degree in job_desc_lower:
                required_level = max(required_level, level)
        
        # Calculate match score
        if required_level == 0:
            return 0.7  # No specific requirement
        elif candidate_level >= required_level:
            return 1.0
        elif candidate_level == required_level - 1:
            return 0.8
        else:
            return max(0.3, candidate_level / required_level)

    def _estimate_years_experience(self, experience_list: List[str]) -> float:
        """Estimate years of experience from experience descriptions"""
        
        import re
        total_years = 0.0
        
        for exp in experience_list:
            # Look for explicit year mentions
            year_patterns = [
                r'(\d+)\s*years?',
                r'(\d{4})\s*-\s*(\d{4})',
                r'(\d{4})\s*to\s*(\d{4})',
                r'(\d{4})\s*-\s*present',
                r'(\d{4})\s*-\s*current'
            ]
            
            for pattern in year_patterns:
                matches = re.findall(pattern, exp, re.IGNORECASE)
                for match in matches:
                    if isinstance(match, tuple):
                        if len(match) == 2:
                            try:
                                start_year = int(match[0])
                                if 'present' in match[1].lower() or 'current' in match[1].lower():
                                    end_year = 2024  # Current year
                                else:
                                    end_year = int(match[1])
                                years = end_year - start_year
                                total_years += max(0, years)
                            except ValueError:
                                continue
                    else:
                        try:
                            total_years += int(match)
                        except ValueError:
                            continue
        
        # If no explicit years found, estimate based on number of positions
        if total_years == 0:
            total_years = len(experience_list) * 2  # Assume 2 years per position
        
        return min(total_years, 25)  # Cap at 25 years

    def _calculate_weighted_match_score(self, 
                                      semantic_similarity: float,
                                      skill_overlap: float,
                                      experience_match: float,
                                      education_match: float,
                                      job_title: str) -> float:
        """Calculate weighted match score based on job category"""
        
        # Determine job category
        job_category = self._categorize_job(job_title)
        weights = self.job_categories.get(job_category, {
            'experience_weight': 0.3,
            'skills_weight': 0.4,
            'education_weight': 0.2,
            'other_weight': 0.1
        })
        
        # Calculate weighted score
        weighted_score = (
            semantic_similarity * weights['other_weight'] +
            skill_overlap * weights['skills_weight'] +
            experience_match * weights['experience_weight'] +
            education_match * weights['education_weight']
        )
        
        return min(1.0, weighted_score)

    def _categorize_job(self, job_title: str) -> str:
        """Categorize job based on title"""
        
        title_lower = job_title.lower()
        
        if any(term in title_lower for term in ['software', 'developer', 'engineer', 'programmer']):
            if any(term in title_lower for term in ['devops', 'sre', 'infrastructure', 'platform']):
                return 'devops_engineer'
            return 'software_engineer'
        elif any(term in title_lower for term in ['data scientist', 'ml engineer', 'ai']):
            return 'data_scientist'
        elif any(term in title_lower for term in ['product manager', 'pm', 'product owner']):
            return 'product_manager'
        elif any(term in title_lower for term in ['devops', 'sre', 'infrastructure']):
            return 'devops_engineer'
        else:
            return 'general'

    def _predict_selection_probability(self, 
                                     resume_data: Dict[str, Any],
                                     job_description: str,
                                     skill_analysis,
                                     match_score: float) -> float:
        """Predict selection probability using the prediction model"""
        
        try:
            # Extract features for prediction
            features = self.prediction_model.extract_features(
                resume_data, job_description, match_score, {
                    'matched_skills': [skill.skill for skill in skill_analysis.matched_skills],
                    'missing_skills': [skill.skill for skill in skill_analysis.missing_skills]
                }
            )
            
            # Get prediction
            probability = self.prediction_model.predict_selection_probability(features)
            return probability
            
        except Exception as e:
            logger.error(f"Error predicting selection probability: {e}")
            # Fallback to match score
            return match_score * 0.8

    def _generate_job_recommendation(self, 
                                   match_score: float,
                                   selection_probability: float,
                                   skill_analysis) -> Tuple[str, str]:
        """Generate recommendation and priority level for job"""
        
        # Determine priority level
        if match_score >= 0.8 and selection_probability >= 0.7:
            priority = 'high'
            recommendation = "Excellent match! Apply immediately. You meet most requirements."
        elif match_score >= 0.6 and selection_probability >= 0.5:
            priority = 'medium'
            missing_count = len(skill_analysis.missing_skills)
            if missing_count <= 2:
                recommendation = f"Good match. Consider applying after addressing {missing_count} missing skills."
            else:
                recommendation = f"Moderate match. Focus on acquiring key skills: {', '.join([s.skill for s in skill_analysis.missing_skills[:2]])}."
        else:
            priority = 'low'
            critical_gaps = len(skill_analysis.critical_gaps)
            if critical_gaps > 0:
                recommendation = f"Significant skill gaps. Focus on critical skills: {', '.join(skill_analysis.critical_gaps[:2])}."
            else:
                recommendation = "Limited match. Consider this role for future career growth after skill development."
        
        return recommendation, priority

    def _generate_career_insights(self, job_matches: List[JobMatch], resume_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate career insights from job matching results"""
        
        insights = {
            'top_matching_roles': [],
            'skill_demand_analysis': {},
            'career_progression_suggestions': [],
            'salary_potential': {},
            'market_readiness': ''
        }
        
        # Top matching roles
        insights['top_matching_roles'] = [
            {'title': match.job_title, 'score': match.match_score}
            for match in job_matches[:5]
        ]
        
        # Skill demand analysis
        all_missing_skills = []
        for match in job_matches:
            all_missing_skills.extend(match.missing_skills)
        
        skill_demand = {}
        for skill in set(all_missing_skills):
            count = all_missing_skills.count(skill)
            skill_demand[skill] = count
        
        # Sort by demand
        insights['skill_demand_analysis'] = dict(
            sorted(skill_demand.items(), key=lambda x: x[1], reverse=True)[:10]
        )
        
        # Career progression suggestions
        high_match_roles = [match for match in job_matches if match.match_score >= 0.7]
        medium_match_roles = [match for match in job_matches if 0.5 <= match.match_score < 0.7]
        
        if high_match_roles:
            insights['career_progression_suggestions'].append(
                f"You're ready for {len(high_match_roles)} roles. Focus on applications."
            )
        
        if medium_match_roles:
            insights['career_progression_suggestions'].append(
                f"With skill development, you could qualify for {len(medium_match_roles)} additional roles."
            )
        
        # Market readiness assessment
        avg_match_score = np.mean([match.match_score for match in job_matches]) if job_matches else 0
        
        if avg_match_score >= 0.7:
            insights['market_readiness'] = 'High - You are competitive for most analyzed roles'
        elif avg_match_score >= 0.5:
            insights['market_readiness'] = 'Medium - Some skill development recommended'
        else:
            insights['market_readiness'] = 'Low - Significant upskilling needed'
        
        return insights

    def _generate_recommended_actions(self, job_matches: List[JobMatch], skill_gaps: Dict[str, int]) -> List[str]:
        """Generate recommended actions based on analysis"""
        
        actions = []
        
        # High priority applications
        high_priority_jobs = [match for match in job_matches if match.priority_level == 'high']
        if high_priority_jobs:
            actions.append(f"Apply immediately to {len(high_priority_jobs)} high-match positions")
        
        # Skill development priorities
        top_missing_skills = sorted(skill_gaps.items(), key=lambda x: x[1], reverse=True)[:3]
        if top_missing_skills:
            skills_list = [skill for skill, count in top_missing_skills]
            actions.append(f"Prioritize learning: {', '.join(skills_list)}")
        
        # Medium priority preparation
        medium_priority_jobs = [match for match in job_matches if match.priority_level == 'medium']
        if medium_priority_jobs:
            actions.append(f"Prepare for {len(medium_priority_jobs)} medium-match roles through targeted skill development")
        
        # Resume optimization
        avg_selection_prob = np.mean([match.selection_probability for match in job_matches]) if job_matches else 0
        if avg_selection_prob < 0.6:
            actions.append("Optimize resume content and keywords to improve ATS compatibility")
        
        return actions

    def _calculate_match_distribution(self, job_matches: List[JobMatch]) -> Dict[str, int]:
        """Calculate distribution of match scores"""
        
        distribution = {'high': 0, 'medium': 0, 'low': 0}
        
        for match in job_matches:
            if match.match_score >= 0.7:
                distribution['high'] += 1
            elif match.match_score >= 0.5:
                distribution['medium'] += 1
            else:
                distribution['low'] += 1
        
        return distribution

    def export_results(self, results: RoleMatchingResults, format: str = 'json') -> str:
        """Export role matching results"""
        
        if format == 'json':
            return json.dumps(asdict(results), indent=2, default=str)
        
        elif format == 'summary':
            summary = f"""
ROLE MATCHING ANALYSIS SUMMARY
==============================

Total Jobs Analyzed: {results.total_jobs_analyzed}

MATCH DISTRIBUTION:
- High Match (70%+): {results.match_distribution.get('high', 0)} jobs
- Medium Match (50-70%): {results.match_distribution.get('medium', 0)} jobs  
- Low Match (<50%): {results.match_distribution.get('low', 0)} jobs

TOP 5 MATCHES:
{chr(10).join([f"{i+1}. {match.job_title} at {match.company} - {match.match_score:.1%} match"
               for i, match in enumerate(results.best_matches[:5])])}

MOST IN-DEMAND SKILLS (Missing):
{chr(10).join([f"• {skill}: Required by {count} jobs"
               for skill, count in list(results.skill_gap_summary.items())[:5]])}

RECOMMENDED ACTIONS:
{chr(10).join(['• ' + action for action in results.recommended_actions])}

MARKET READINESS: {results.career_insights.get('market_readiness', 'Unknown')}
            """
            return summary.strip()
        
        return str(results)

    def get_job_recommendations_by_category(self, results: RoleMatchingResults) -> Dict[str, List[JobMatch]]:
        """Group job recommendations by category"""
        
        categories = defaultdict(list)
        
        for match in results.best_matches:
            category = self._categorize_job(match.job_title)
            categories[category].append(match)
        
        # Sort each category by match score
        for category in categories:
            categories[category].sort(key=lambda x: x.match_score, reverse=True)
        
        return dict(categories)
