"""
Upskilling Simulation and Course Recommendation Engine
Estimates impact of acquiring skills and suggests relevant courses
"""

import json
import logging
import requests
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import numpy as np
from collections import defaultdict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class CourseRecommendation:
    """Represents a course recommendation"""
    title: str
    provider: str
    url: str
    duration: str
    difficulty: str
    rating: float
    price: str
    skills_covered: List[str]
    description: str
    relevance_score: float

@dataclass
class SkillImpactSimulation:
    """Simulation results for acquiring a skill"""
    skill: str
    current_probability: float
    projected_probability: float
    probability_increase: float
    time_to_acquire: str
    difficulty_level: str
    recommended_courses: List[CourseRecommendation]
    learning_path: List[str]
    roi_score: float  # Return on Investment score

@dataclass
class UpskillingPlan:
    """Complete upskilling plan with prioritized recommendations"""
    skill_simulations: List[SkillImpactSimulation]
    prioritized_skills: List[str]
    total_time_estimate: str
    budget_estimate: str
    quick_wins: List[str]  # Skills that can be acquired quickly with high impact
    long_term_goals: List[str]  # Skills requiring significant time investment

class UpskillingEngine:
    """Advanced upskilling simulation and course recommendation system"""
    
    def __init__(self):
        """Initialize the upskilling engine"""
        
        # Course databases (in production, these would be API calls)
        self.course_databases = {
            'coursera': self._get_coursera_courses(),
            'udemy': self._get_udemy_courses(),
            'edx': self._get_edx_courses(),
            'pluralsight': self._get_pluralsight_courses(),
            'linkedin_learning': self._get_linkedin_courses()
        }
        
        # Skill acquisition difficulty and time estimates
        self.skill_metadata = {
            'Python': {'difficulty': 'Beginner', 'time_weeks': 8, 'impact_multiplier': 1.3},
            'JavaScript': {'difficulty': 'Beginner', 'time_weeks': 6, 'impact_multiplier': 1.25},
            'React': {'difficulty': 'Intermediate', 'time_weeks': 10, 'impact_multiplier': 1.4},
            'Angular': {'difficulty': 'Intermediate', 'time_weeks': 12, 'impact_multiplier': 1.35},
            'Node.js': {'difficulty': 'Intermediate', 'time_weeks': 8, 'impact_multiplier': 1.2},
            'AWS': {'difficulty': 'Intermediate', 'time_weeks': 16, 'impact_multiplier': 1.5},
            'Docker': {'difficulty': 'Intermediate', 'time_weeks': 6, 'impact_multiplier': 1.3},
            'Kubernetes': {'difficulty': 'Advanced', 'time_weeks': 20, 'impact_multiplier': 1.6},
            'Machine Learning': {'difficulty': 'Advanced', 'time_weeks': 24, 'impact_multiplier': 1.7},
            'Deep Learning': {'difficulty': 'Advanced', 'time_weeks': 28, 'impact_multiplier': 1.8},
            'SQL': {'difficulty': 'Beginner', 'time_weeks': 4, 'impact_multiplier': 1.2},
            'MongoDB': {'difficulty': 'Intermediate', 'time_weeks': 6, 'impact_multiplier': 1.15},
            'PostgreSQL': {'difficulty': 'Intermediate', 'time_weeks': 8, 'impact_multiplier': 1.25},
            'Git': {'difficulty': 'Beginner', 'time_weeks': 2, 'impact_multiplier': 1.1},
            'Jenkins': {'difficulty': 'Intermediate', 'time_weeks': 10, 'impact_multiplier': 1.3},
            'Terraform': {'difficulty': 'Advanced', 'time_weeks': 14, 'impact_multiplier': 1.4}
        }
        
        # Skill relationships and prerequisites
        self.skill_prerequisites = {
            'React': ['JavaScript', 'HTML', 'CSS'],
            'Angular': ['JavaScript', 'TypeScript', 'HTML', 'CSS'],
            'Node.js': ['JavaScript'],
            'Django': ['Python'],
            'Flask': ['Python'],
            'Spring': ['Java'],
            'Kubernetes': ['Docker', 'Linux'],
            'Deep Learning': ['Machine Learning', 'Python'],
            'TensorFlow': ['Python', 'Machine Learning'],
            'PyTorch': ['Python', 'Machine Learning']
        }
        
        # Market demand and salary impact data
        self.market_data = {
            'Python': {'demand_score': 0.95, 'salary_impact': 15000},
            'JavaScript': {'demand_score': 0.90, 'salary_impact': 12000},
            'React': {'demand_score': 0.85, 'salary_impact': 18000},
            'AWS': {'demand_score': 0.90, 'salary_impact': 25000},
            'Machine Learning': {'demand_score': 0.85, 'salary_impact': 30000},
            'Docker': {'demand_score': 0.80, 'salary_impact': 15000},
            'Kubernetes': {'demand_score': 0.75, 'salary_impact': 20000},
            'Angular': {'demand_score': 0.75, 'salary_impact': 16000},
            'Node.js': {'demand_score': 0.80, 'salary_impact': 14000},
            'SQL': {'demand_score': 0.90, 'salary_impact': 10000}
        }

    def _get_coursera_courses(self) -> Dict[str, List[CourseRecommendation]]:
        """Get Coursera course database (mock data)"""
        return {
            'Python': [
                CourseRecommendation(
                    title="Python for Everybody Specialization",
                    provider="Coursera",
                    url="https://coursera.org/specializations/python",
                    duration="8 months",
                    difficulty="Beginner",
                    rating=4.8,
                    price="$49/month",
                    skills_covered=["Python", "Data Structures", "Web Scraping", "Databases"],
                    description="Learn to program and analyze data with Python",
                    relevance_score=0.95
                )
            ],
            'React': [
                CourseRecommendation(
                    title="React Specialization",
                    provider="Coursera",
                    url="https://coursera.org/specializations/react",
                    duration="4 months",
                    difficulty="Intermediate",
                    rating=4.7,
                    price="$49/month",
                    skills_covered=["React", "Redux", "JavaScript", "Web Development"],
                    description="Build modern web applications with React",
                    relevance_score=0.92
                )
            ],
            'Machine Learning': [
                CourseRecommendation(
                    title="Machine Learning Specialization",
                    provider="Coursera",
                    url="https://coursera.org/specializations/machine-learning-introduction",
                    duration="3 months",
                    difficulty="Intermediate",
                    rating=4.9,
                    price="$49/month",
                    skills_covered=["Machine Learning", "Python", "TensorFlow", "Neural Networks"],
                    description="Learn the fundamentals of machine learning",
                    relevance_score=0.98
                )
            ]
        }

    def _get_udemy_courses(self) -> Dict[str, List[CourseRecommendation]]:
        """Get Udemy course database (mock data)"""
        return {
            'AWS': [
                CourseRecommendation(
                    title="AWS Certified Solutions Architect",
                    provider="Udemy",
                    url="https://udemy.com/course/aws-certified-solutions-architect",
                    duration="30 hours",
                    difficulty="Intermediate",
                    rating=4.6,
                    price="$89.99",
                    skills_covered=["AWS", "Cloud Computing", "EC2", "S3", "Lambda"],
                    description="Complete AWS certification preparation",
                    relevance_score=0.94
                )
            ],
            'Docker': [
                CourseRecommendation(
                    title="Docker Mastery: with Kubernetes +Swarm",
                    provider="Udemy",
                    url="https://udemy.com/course/docker-mastery",
                    duration="19 hours",
                    difficulty="Intermediate",
                    rating=4.7,
                    price="$94.99",
                    skills_covered=["Docker", "Kubernetes", "DevOps", "Containerization"],
                    description="Build, test, deploy containers with the best practices",
                    relevance_score=0.91
                )
            ]
        }

    def _get_edx_courses(self) -> Dict[str, List[CourseRecommendation]]:
        """Get edX course database (mock data)"""
        return {
            'JavaScript': [
                CourseRecommendation(
                    title="Introduction to JavaScript",
                    provider="edX",
                    url="https://edx.org/course/javascript-introduction",
                    duration="6 weeks",
                    difficulty="Beginner",
                    rating=4.5,
                    price="Free (Verified: $99)",
                    skills_covered=["JavaScript", "DOM", "ES6", "Async Programming"],
                    description="Learn JavaScript fundamentals and modern features",
                    relevance_score=0.88
                )
            ]
        }

    def _get_pluralsight_courses(self) -> Dict[str, List[CourseRecommendation]]:
        """Get Pluralsight course database (mock data)"""
        return {
            'Angular': [
                CourseRecommendation(
                    title="Angular: Getting Started",
                    provider="Pluralsight",
                    url="https://pluralsight.com/courses/angular-2-getting-started-update",
                    duration="6 hours",
                    difficulty="Intermediate",
                    rating=4.6,
                    price="$29/month",
                    skills_covered=["Angular", "TypeScript", "Components", "Services"],
                    description="Learn to build applications with Angular",
                    relevance_score=0.89
                )
            ]
        }

    def _get_linkedin_courses(self) -> Dict[str, List[CourseRecommendation]]:
        """Get LinkedIn Learning course database (mock data)"""
        return {
            'SQL': [
                CourseRecommendation(
                    title="SQL Essential Training",
                    provider="LinkedIn Learning",
                    url="https://linkedin.com/learning/sql-essential-training",
                    duration="3 hours",
                    difficulty="Beginner",
                    rating=4.7,
                    price="$29.99/month",
                    skills_covered=["SQL", "Database Design", "Queries", "Joins"],
                    description="Master SQL fundamentals for data analysis",
                    relevance_score=0.93
                )
            ]
        }

    def simulate_skill_impact(self, 
                            skill: str,
                            current_selection_probability: float,
                            skill_importance: float = 0.8) -> SkillImpactSimulation:
        """Simulate the impact of acquiring a specific skill"""
        
        # Get skill metadata
        metadata = self.skill_metadata.get(skill, {
            'difficulty': 'Intermediate',
            'time_weeks': 12,
            'impact_multiplier': 1.2
        })
        
        # Calculate projected probability increase
        base_increase = skill_importance * 0.3  # Base 30% increase for important skills
        multiplier_bonus = (metadata['impact_multiplier'] - 1.0) * 0.5
        total_increase = base_increase + multiplier_bonus
        
        # Apply diminishing returns for already high probabilities
        if current_selection_probability > 0.7:
            total_increase *= 0.7
        elif current_selection_probability > 0.5:
            total_increase *= 0.85
        
        projected_probability = min(0.95, current_selection_probability + total_increase)
        
        # Get course recommendations
        recommended_courses = self._get_skill_courses(skill)
        
        # Generate learning path
        learning_path = self._generate_learning_path(skill)
        
        # Calculate ROI score
        roi_score = self._calculate_roi_score(skill, total_increase, metadata['time_weeks'])
        
        # Format time estimate
        time_estimate = self._format_time_estimate(metadata['time_weeks'])
        
        return SkillImpactSimulation(
            skill=skill,
            current_probability=current_selection_probability,
            projected_probability=projected_probability,
            probability_increase=total_increase,
            time_to_acquire=time_estimate,
            difficulty_level=metadata['difficulty'],
            recommended_courses=recommended_courses,
            learning_path=learning_path,
            roi_score=roi_score
        )

    def _get_skill_courses(self, skill: str) -> List[CourseRecommendation]:
        """Get course recommendations for a specific skill"""
        
        all_courses = []
        
        # Search across all course databases
        for provider, courses_db in self.course_databases.items():
            if skill in courses_db:
                all_courses.extend(courses_db[skill])
        
        # If no specific courses found, generate generic recommendations
        if not all_courses:
            all_courses = [
                CourseRecommendation(
                    title=f"Learn {skill} - Complete Guide",
                    provider="Multiple Platforms",
                    url=f"https://search.com/courses/{skill.lower().replace(' ', '-')}",
                    duration="8-12 weeks",
                    difficulty=self.skill_metadata.get(skill, {}).get('difficulty', 'Intermediate'),
                    rating=4.5,
                    price="$50-100",
                    skills_covered=[skill],
                    description=f"Comprehensive {skill} training course",
                    relevance_score=0.8
                )
            ]
        
        # Sort by relevance score
        all_courses.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return all_courses[:3]  # Return top 3 courses

    def _generate_learning_path(self, skill: str) -> List[str]:
        """Generate a learning path for acquiring a skill"""
        
        learning_paths = {
            'Python': [
                "1. Python Basics & Syntax",
                "2. Data Structures & Algorithms",
                "3. Object-Oriented Programming",
                "4. Libraries & Frameworks",
                "5. Build Projects & Portfolio"
            ],
            'React': [
                "1. JavaScript ES6+ Fundamentals",
                "2. React Components & JSX",
                "3. State Management & Hooks",
                "4. Routing & Navigation",
                "5. Build Full-Stack Applications"
            ],
            'AWS': [
                "1. Cloud Computing Fundamentals",
                "2. Core AWS Services (EC2, S3, IAM)",
                "3. Networking & Security",
                "4. DevOps & Automation",
                "5. Certification & Advanced Services"
            ],
            'Machine Learning': [
                "1. Statistics & Linear Algebra",
                "2. Python for Data Science",
                "3. Supervised Learning Algorithms",
                "4. Unsupervised Learning & Deep Learning",
                "5. MLOps & Production Deployment"
            ],
            'Docker': [
                "1. Containerization Concepts",
                "2. Docker Basics & Commands",
                "3. Dockerfile & Image Creation",
                "4. Docker Compose & Networking",
                "5. Production Deployment & Orchestration"
            ]
        }
        
        # Default learning path for unlisted skills
        default_path = [
            f"1. {skill} Fundamentals",
            f"2. Core {skill} Concepts",
            f"3. Intermediate {skill} Topics",
            f"4. Advanced {skill} Applications",
            f"5. {skill} Projects & Portfolio"
        ]
        
        return learning_paths.get(skill, default_path)

    def _calculate_roi_score(self, skill: str, probability_increase: float, time_weeks: int) -> float:
        """Calculate Return on Investment score for learning a skill"""
        
        # Get market data
        market_info = self.market_data.get(skill, {
            'demand_score': 0.7,
            'salary_impact': 10000
        })
        
        # ROI factors
        impact_factor = probability_increase * 10  # Convert to 0-10 scale
        demand_factor = market_info['demand_score'] * 5  # Convert to 0-5 scale
        time_factor = max(1, 10 - (time_weeks / 4))  # Penalty for longer learning time
        salary_factor = min(5, market_info['salary_impact'] / 5000)  # Salary impact factor
        
        # Calculate weighted ROI score
        roi_score = (
            impact_factor * 0.3 +
            demand_factor * 0.25 +
            time_factor * 0.2 +
            salary_factor * 0.25
        )
        
        return min(10.0, roi_score)

    def _format_time_estimate(self, weeks: int) -> str:
        """Format time estimate in human-readable format"""
        
        if weeks <= 4:
            return f"{weeks} weeks (1 month)"
        elif weeks <= 12:
            months = round(weeks / 4)
            return f"{weeks} weeks ({months} months)"
        else:
            months = round(weeks / 4)
            return f"{weeks} weeks ({months} months)"

    def create_upskilling_plan(self,
                             missing_skills: List[str],
                             current_probability: float,
                             skill_importance_map: Dict[str, float],
                             time_constraint: Optional[int] = None) -> UpskillingPlan:
        """Create a comprehensive upskilling plan"""
        
        # Simulate impact for each missing skill
        skill_simulations = []
        for skill in missing_skills:
            importance = skill_importance_map.get(skill, 0.7)
            simulation = self.simulate_skill_impact(skill, current_probability, importance)
            skill_simulations.append(simulation)
        
        # Sort by ROI score
        skill_simulations.sort(key=lambda x: x.roi_score, reverse=True)
        
        # Prioritize skills based on multiple factors
        prioritized_skills = self._prioritize_skills(skill_simulations, time_constraint)
        
        # Identify quick wins (high impact, low time investment)
        quick_wins = [
            sim.skill for sim in skill_simulations
            if sim.roi_score > 7.0 and 'weeks' in sim.time_to_acquire and
            int(sim.time_to_acquire.split()[0]) <= 8
        ]
        
        # Identify long-term goals (high impact, high time investment)
        long_term_goals = [
            sim.skill for sim in skill_simulations
            if sim.probability_increase > 0.2 and 'weeks' in sim.time_to_acquire and
            int(sim.time_to_acquire.split()[0]) > 16
        ]
        
        # Calculate total time and budget estimates
        total_time_estimate = self._calculate_total_time(skill_simulations[:5])  # Top 5 skills
        budget_estimate = self._calculate_budget_estimate(skill_simulations[:5])
        
        return UpskillingPlan(
            skill_simulations=skill_simulations,
            prioritized_skills=prioritized_skills,
            total_time_estimate=total_time_estimate,
            budget_estimate=budget_estimate,
            quick_wins=quick_wins,
            long_term_goals=long_term_goals
        )

    def _prioritize_skills(self, 
                          simulations: List[SkillImpactSimulation],
                          time_constraint: Optional[int]) -> List[str]:
        """Prioritize skills based on ROI, prerequisites, and time constraints"""
        
        # Create dependency graph
        skill_deps = {}
        for sim in simulations:
            skill_deps[sim.skill] = self.skill_prerequisites.get(sim.skill, [])
        
        # If time constraint is specified, filter skills
        if time_constraint:
            filtered_sims = []
            for sim in simulations:
                weeks_needed = int(sim.time_to_acquire.split()[0])
                if weeks_needed <= time_constraint:
                    filtered_sims.append(sim)
            simulations = filtered_sims
        
        # Sort by ROI score and resolve dependencies
        prioritized = []
        remaining_skills = {sim.skill: sim for sim in simulations}
        
        while remaining_skills:
            # Find skills with no unmet dependencies
            ready_skills = []
            for skill, sim in remaining_skills.items():
                deps = skill_deps.get(skill, [])
                unmet_deps = [dep for dep in deps if dep in remaining_skills]
                if not unmet_deps:
                    ready_skills.append((skill, sim))
            
            if not ready_skills:
                # If circular dependencies, just pick highest ROI
                skill, sim = max(remaining_skills.items(), key=lambda x: x[1].roi_score)
                ready_skills = [(skill, sim)]
            
            # Sort ready skills by ROI and add the best one
            ready_skills.sort(key=lambda x: x[1].roi_score, reverse=True)
            best_skill, _ = ready_skills[0]
            
            prioritized.append(best_skill)
            del remaining_skills[best_skill]
        
        return prioritized

    def _calculate_total_time(self, simulations: List[SkillImpactSimulation]) -> str:
        """Calculate total time estimate for multiple skills"""
        
        total_weeks = 0
        for sim in simulations:
            weeks = int(sim.time_to_acquire.split()[0])
            total_weeks += weeks
        
        # Assume 25% overlap/parallel learning
        adjusted_weeks = int(total_weeks * 0.75)
        
        return self._format_time_estimate(adjusted_weeks)

    def _calculate_budget_estimate(self, simulations: List[SkillImpactSimulation]) -> str:
        """Calculate budget estimate for course recommendations"""
        
        total_cost = 0
        cost_ranges = []
        
        for sim in simulations:
            if sim.recommended_courses:
                course = sim.recommended_courses[0]  # Use first recommended course
                price_str = course.price
                
                # Extract numeric cost (simplified parsing)
                if 'free' in price_str.lower():
                    cost = 0
                elif '$' in price_str:
                    # Extract first number after $
                    import re
                    numbers = re.findall(r'\$(\d+(?:\.\d+)?)', price_str)
                    if numbers:
                        cost = float(numbers[0])
                        # If it's monthly, assume 3 months
                        if 'month' in price_str.lower():
                            cost *= 3
                    else:
                        cost = 100  # Default estimate
                else:
                    cost = 100  # Default estimate
                
                total_cost += cost
                cost_ranges.append(cost)
        
        if not cost_ranges:
            return "$500 - $1,500"
        
        min_cost = int(total_cost * 0.7)
        max_cost = int(total_cost * 1.3)
        
        return f"${min_cost} - ${max_cost}"

    def get_skill_alternatives(self, skill: str) -> List[str]:
        """Get alternative skills that provide similar value"""
        
        alternatives = {
            'React': ['Angular', 'Vue.js', 'Svelte'],
            'Angular': ['React', 'Vue.js'],
            'Vue.js': ['React', 'Angular'],
            'AWS': ['Azure', 'Google Cloud'],
            'Azure': ['AWS', 'Google Cloud'],
            'MySQL': ['PostgreSQL', 'SQLite'],
            'MongoDB': ['Redis', 'CouchDB'],
            'Docker': ['Podman', 'LXC'],
            'Jenkins': ['GitLab CI', 'GitHub Actions', 'Travis CI'],
            'Python': ['Java', 'JavaScript', 'Go'],
            'Java': ['Python', 'C#', 'Kotlin']
        }
        
        return alternatives.get(skill, [])

    def export_plan(self, plan: UpskillingPlan, format: str = 'json') -> str:
        """Export upskilling plan in specified format"""
        
        if format == 'json':
            return json.dumps(asdict(plan), indent=2, default=str)
        
        elif format == 'summary':
            summary = f"""
UPSKILLING PLAN SUMMARY
======================

QUICK WINS (High Impact, Short Time):
{', '.join(plan.quick_wins) if plan.quick_wins else 'None identified'}

PRIORITIZED LEARNING ORDER:
{chr(10).join([f"{i+1}. {skill}" for i, skill in enumerate(plan.prioritized_skills[:5])])}

LONG-TERM GOALS:
{', '.join(plan.long_term_goals) if plan.long_term_goals else 'None identified'}

TIME ESTIMATE: {plan.total_time_estimate}
BUDGET ESTIMATE: {plan.budget_estimate}

TOP 3 SKILL RECOMMENDATIONS:
{chr(10).join([f"• {sim.skill}: +{sim.probability_increase:.1%} selection probability ({sim.time_to_acquire})" 
               for sim in plan.skill_simulations[:3]])}
            """
            return summary.strip()
        
        return str(plan)
