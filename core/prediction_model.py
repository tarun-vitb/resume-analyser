"""
ML-based Selection Probability Prediction Model
Lightweight and efficient model for predicting job selection probability
"""

import numpy as np
import pandas as pd
import logging
from typing import Dict, List, Tuple, Optional, Any
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, mean_squared_error, classification_report
import xgboost as xgb
import pickle
from pathlib import Path
import json
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PredictionFeatures:
    """Features used for selection probability prediction"""
    semantic_similarity: float
    skill_match_ratio: float
    experience_match: float
    education_match: float
    keyword_density: float
    resume_quality_score: float
    missing_skills_count: int
    total_skills_count: int
    resume_length: int
    has_relevant_experience: bool
    years_experience: float
    education_level: int  # 0=High School, 1=Bachelor's, 2=Master's, 3=PhD
    certifications_count: int
    action_words_count: int
    quantifiable_achievements: bool

class SelectionPredictor:
    """ML model for predicting job selection probability"""
    
    def __init__(self, model_type: str = "xgboost"):
        """
        Initialize the selection predictor
        
        Args:
            model_type: Type of model to use ('xgboost', 'random_forest', 'gradient_boost')
        """
        self.model_type = model_type
        self.model = None
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.is_trained = False
        
        # Feature importance weights (based on domain knowledge)
        self.feature_weights = {
            'semantic_similarity': 0.25,
            'skill_match_ratio': 0.20,
            'experience_match': 0.15,
            'education_match': 0.10,
            'keyword_density': 0.10,
            'resume_quality_score': 0.08,
            'missing_skills_count': -0.05,  # Negative weight
            'years_experience': 0.07
        }
        
        # Initialize model based on type
        self._initialize_model()

    def _initialize_model(self):
        """Initialize the ML model based on specified type"""
        if self.model_type == "xgboost":
            self.model = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42,
                n_jobs=-1
            )
        elif self.model_type == "random_forest":
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42,
                n_jobs=-1
            )
        elif self.model_type == "gradient_boost":
            self.model = GradientBoostingRegressor(
                n_estimators=100,
                max_depth=6,
                learning_rate=0.1,
                random_state=42
            )
        else:
            raise ValueError(f"Unsupported model type: {self.model_type}")

    def extract_features(self, 
                        resume_data: Dict[str, Any], 
                        job_description: str,
                        similarity_score: float,
                        skill_analysis: Dict[str, Any]) -> PredictionFeatures:
        """Extract features for prediction from resume and job data"""
        
        # Basic similarity and skill matching
        semantic_similarity = similarity_score
        
        matched_skills = skill_analysis.get('matched_skills', [])
        missing_skills = skill_analysis.get('missing_skills', [])
        total_job_skills = len(matched_skills) + len(missing_skills)
        
        skill_match_ratio = len(matched_skills) / max(total_job_skills, 1)
        
        # Experience matching (simplified)
        experience_match = self._calculate_experience_match(
            resume_data.get('experience', []), 
            job_description
        )
        
        # Education matching
        education_match = self._calculate_education_match(
            resume_data.get('education', []), 
            job_description
        )
        
        # Keyword density
        resume_text = resume_data.get('cleaned_text', '')
        keyword_density = self._calculate_keyword_density(resume_text, job_description)
        
        # Resume quality score
        resume_quality_score = self._calculate_resume_quality(resume_data)
        
        # Extract years of experience
        years_experience = self._extract_years_experience(resume_data.get('experience', []))
        
        # Education level
        education_level = self._determine_education_level(resume_data.get('education', []))
        
        # Count certifications
        certifications_count = self._count_certifications(resume_text)
        
        # Count action words
        action_words_count = self._count_action_words(resume_text)
        
        # Check for quantifiable achievements
        quantifiable_achievements = self._has_quantifiable_achievements(resume_text)
        
        return PredictionFeatures(
            semantic_similarity=semantic_similarity,
            skill_match_ratio=skill_match_ratio,
            experience_match=experience_match,
            education_match=education_match,
            keyword_density=keyword_density,
            resume_quality_score=resume_quality_score,
            missing_skills_count=len(missing_skills),
            total_skills_count=len(resume_data.get('skills', [])),
            resume_length=len(resume_text.split()),
            has_relevant_experience=experience_match > 0.3,
            years_experience=years_experience,
            education_level=education_level,
            certifications_count=certifications_count,
            action_words_count=action_words_count,
            quantifiable_achievements=quantifiable_achievements
        )

    def _calculate_experience_match(self, experience_list: List[str], job_description: str) -> float:
        """Calculate how well experience matches job requirements"""
        if not experience_list:
            return 0.0
        
        job_desc_lower = job_description.lower()
        experience_text = ' '.join(experience_list).lower()
        
        # Look for common experience indicators
        experience_keywords = [
            'python', 'java', 'javascript', 'react', 'angular', 'node',
            'sql', 'database', 'api', 'web development', 'software',
            'project management', 'team lead', 'senior', 'manager'
        ]
        
        matches = 0
        total_keywords = 0
        
        for keyword in experience_keywords:
            if keyword in job_desc_lower:
                total_keywords += 1
                if keyword in experience_text:
                    matches += 1
        
        return matches / max(total_keywords, 1)

    def _calculate_education_match(self, education_list: List[str], job_description: str) -> float:
        """Calculate education match score"""
        if not education_list:
            return 0.0
        
        education_text = ' '.join(education_list).lower()
        job_desc_lower = job_description.lower()
        
        # Education level matching
        education_levels = {
            'phd': 4, 'doctorate': 4, 'ph.d': 4,
            'master': 3, 'mba': 3, 'ms': 3, 'ma': 3,
            'bachelor': 2, 'bs': 2, 'ba': 2, 'btech': 2,
            'associate': 1, 'diploma': 1
        }
        
        candidate_level = 0
        required_level = 0
        
        for degree, level in education_levels.items():
            if degree in education_text:
                candidate_level = max(candidate_level, level)
            if degree in job_desc_lower:
                required_level = max(required_level, level)
        
        if required_level == 0:
            return 0.5  # No specific requirement
        
        # Calculate match based on education level
        if candidate_level >= required_level:
            return 1.0
        elif candidate_level == required_level - 1:
            return 0.7
        else:
            return 0.3

    def _calculate_keyword_density(self, resume_text: str, job_description: str) -> float:
        """Calculate keyword density match"""
        resume_words = set(resume_text.lower().split())
        job_words = set(job_description.lower().split())
        
        # Filter out common words
        common_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        job_words = job_words - common_words
        
        if not job_words:
            return 0.0
        
        matches = len(resume_words.intersection(job_words))
        return matches / len(job_words)

    def _calculate_resume_quality(self, resume_data: Dict[str, Any]) -> float:
        """Calculate overall resume quality score"""
        score = 0.0
        
        # Check for completeness
        if resume_data.get('name'):
            score += 0.1
        if resume_data.get('email'):
            score += 0.1
        if resume_data.get('phone'):
            score += 0.1
        if resume_data.get('skills'):
            score += 0.2
        if resume_data.get('experience'):
            score += 0.3
        if resume_data.get('education'):
            score += 0.2
        
        return score

    def _extract_years_experience(self, experience_list: List[str]) -> float:
        """Extract years of experience from experience text"""
        import re
        
        total_years = 0.0
        experience_text = ' '.join(experience_list)
        
        # Look for year patterns
        year_patterns = [
            r'(\d+)\s*years?',
            r'(\d+)\s*yrs?',
            r'(\d{4})\s*-\s*(\d{4})',
            r'(\d{4})\s*to\s*(\d{4})'
        ]
        
        for pattern in year_patterns:
            matches = re.findall(pattern, experience_text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple) and len(match) == 2:
                    # Date range
                    try:
                        years = int(match[1]) - int(match[0])
                        total_years += years
                    except ValueError:
                        continue
                else:
                    # Direct year mention
                    try:
                        total_years += int(match)
                    except ValueError:
                        continue
        
        return min(total_years, 20)  # Cap at 20 years

    def _determine_education_level(self, education_list: List[str]) -> int:
        """Determine education level (0-3 scale)"""
        if not education_list:
            return 0
        
        education_text = ' '.join(education_list).lower()
        
        if any(word in education_text for word in ['phd', 'doctorate', 'ph.d']):
            return 3
        elif any(word in education_text for word in ['master', 'mba', 'ms', 'ma']):
            return 2
        elif any(word in education_text for word in ['bachelor', 'bs', 'ba', 'btech']):
            return 1
        else:
            return 0

    def _count_certifications(self, resume_text: str) -> int:
        """Count certifications mentioned in resume"""
        cert_keywords = [
            'certified', 'certification', 'certificate', 'aws certified',
            'google certified', 'microsoft certified', 'cisco', 'comptia',
            'pmp', 'scrum master', 'agile'
        ]
        
        count = 0
        resume_lower = resume_text.lower()
        
        for keyword in cert_keywords:
            if keyword in resume_lower:
                count += 1
        
        return count

    def _count_action_words(self, resume_text: str) -> int:
        """Count action words in resume"""
        action_words = [
            'developed', 'implemented', 'managed', 'led', 'created',
            'designed', 'improved', 'optimized', 'achieved', 'delivered',
            'built', 'established', 'coordinated', 'executed', 'launched'
        ]
        
        count = 0
        resume_lower = resume_text.lower()
        
        for word in action_words:
            count += resume_lower.count(word)
        
        return count

    def _has_quantifiable_achievements(self, resume_text: str) -> bool:
        """Check if resume has quantifiable achievements"""
        import re
        
        # Look for numbers and percentages
        number_patterns = [
            r'\d+%',
            r'\$\d+',
            r'\d+\s*(million|thousand|k|m)',
            r'increased.*\d+',
            r'reduced.*\d+',
            r'improved.*\d+'
        ]
        
        for pattern in number_patterns:
            if re.search(pattern, resume_text, re.IGNORECASE):
                return True
        
        return False

    def features_to_array(self, features: PredictionFeatures) -> np.ndarray:
        """Convert features to numpy array for model input"""
        return np.array([
            features.semantic_similarity,
            features.skill_match_ratio,
            features.experience_match,
            features.education_match,
            features.keyword_density,
            features.resume_quality_score,
            features.missing_skills_count,
            features.total_skills_count,
            features.resume_length / 1000,  # Normalize
            float(features.has_relevant_experience),
            features.years_experience / 10,  # Normalize
            features.education_level / 3,  # Normalize
            features.certifications_count / 5,  # Normalize
            features.action_words_count / 10,  # Normalize
            float(features.quantifiable_achievements)
        ])

    def predict_selection_probability(self, features: PredictionFeatures) -> float:
        """Predict selection probability using rule-based approach if model not trained"""
        
        if self.is_trained and self.model is not None:
            # Use trained ML model
            feature_array = self.features_to_array(features).reshape(1, -1)
            feature_array_scaled = self.scaler.transform(feature_array)
            
            if self.model_type == "random_forest":
                # For classification, get probability of positive class
                probabilities = self.model.predict_proba(feature_array_scaled)
                return float(probabilities[0][1])
            else:
                # For regression models
                prediction = self.model.predict(feature_array_scaled)
                return max(0.0, min(1.0, float(prediction[0])))
        
        else:
            # Use rule-based prediction as fallback
            return self._rule_based_prediction(features)

    def _rule_based_prediction(self, features: PredictionFeatures) -> float:
        """Rule-based prediction when ML model is not available"""
        
        # Base score from semantic similarity
        score = features.semantic_similarity * 0.3
        
        # Skill matching contribution
        score += features.skill_match_ratio * 0.25
        
        # Experience matching
        score += features.experience_match * 0.2
        
        # Education matching
        score += features.education_match * 0.1
        
        # Resume quality
        score += features.resume_quality_score * 0.1
        
        # Penalties for missing elements
        if features.missing_skills_count > 5:
            score -= 0.1
        
        if not features.has_relevant_experience:
            score -= 0.15
        
        # Bonuses
        if features.quantifiable_achievements:
            score += 0.05
        
        if features.certifications_count > 0:
            score += 0.05
        
        # Ensure score is between 0 and 1
        return max(0.0, min(1.0, score))

    def generate_synthetic_training_data(self, n_samples: int = 1000) -> Tuple[np.ndarray, np.ndarray]:
        """Generate synthetic training data for model training"""
        
        np.random.seed(42)
        
        # Generate random features
        features_list = []
        labels = []
        
        for _ in range(n_samples):
            # Generate realistic feature values
            semantic_sim = np.random.beta(2, 3)  # Skewed towards lower values
            skill_match = np.random.beta(2, 2)
            exp_match = np.random.beta(2, 2)
            edu_match = np.random.beta(1.5, 2)
            keyword_density = np.random.beta(1.5, 3)
            quality_score = np.random.beta(3, 2)  # Skewed towards higher values
            
            missing_skills = np.random.poisson(3)
            total_skills = np.random.poisson(8) + 5
            resume_length = np.random.normal(400, 150)
            has_exp = np.random.choice([0, 1], p=[0.2, 0.8])
            years_exp = np.random.exponential(3)
            edu_level = np.random.choice([0, 1, 2, 3], p=[0.1, 0.4, 0.4, 0.1])
            certs = np.random.poisson(1)
            action_words = np.random.poisson(5)
            quant_achievements = np.random.choice([0, 1], p=[0.4, 0.6])
            
            features = PredictionFeatures(
                semantic_similarity=semantic_sim,
                skill_match_ratio=skill_match,
                experience_match=exp_match,
                education_match=edu_match,
                keyword_density=keyword_density,
                resume_quality_score=quality_score,
                missing_skills_count=missing_skills,
                total_skills_count=total_skills,
                resume_length=int(resume_length),
                has_relevant_experience=bool(has_exp),
                years_experience=years_exp,
                education_level=edu_level,
                certifications_count=certs,
                action_words_count=action_words,
                quantifiable_achievements=bool(quant_achievements)
            )
            
            # Generate label based on rule-based prediction with noise
            base_prob = self._rule_based_prediction(features)
            # Add some noise to make it more realistic
            noise = np.random.normal(0, 0.1)
            final_prob = max(0.0, min(1.0, base_prob + noise))
            
            features_list.append(self.features_to_array(features))
            labels.append(final_prob)
        
        return np.array(features_list), np.array(labels)

    def train_model(self, X: Optional[np.ndarray] = None, y: Optional[np.ndarray] = None):
        """Train the ML model"""
        
        if X is None or y is None:
            logger.info("No training data provided. Generating synthetic data...")
            X, y = self.generate_synthetic_training_data(1000)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        if self.model_type == "random_forest":
            # Convert to binary classification
            y_train_binary = (y_train > 0.5).astype(int)
            y_test_binary = (y_test > 0.5).astype(int)
            
            self.model.fit(X_train_scaled, y_train_binary)
            
            # Evaluate
            y_pred = self.model.predict(X_test_scaled)
            accuracy = accuracy_score(y_test_binary, y_pred)
            logger.info(f"Model accuracy: {accuracy:.3f}")
            
        else:
            # Regression models
            self.model.fit(X_train_scaled, y_train)
            
            # Evaluate
            y_pred = self.model.predict(X_test_scaled)
            mse = mean_squared_error(y_test, y_pred)
            logger.info(f"Model MSE: {mse:.3f}")
        
        self.is_trained = True
        logger.info("Model training completed successfully")

    def save_model(self, filepath: str):
        """Save the trained model"""
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'model_type': self.model_type,
            'is_trained': self.is_trained
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(model_data, f)
        
        logger.info(f"Model saved to {filepath}")

    def load_model(self, filepath: str):
        """Load a trained model"""
        try:
            with open(filepath, 'rb') as f:
                model_data = pickle.load(f)
            
            self.model = model_data['model']
            self.scaler = model_data['scaler']
            self.model_type = model_data['model_type']
            self.is_trained = model_data['is_trained']
            
            logger.info(f"Model loaded from {filepath}")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.is_trained = False
