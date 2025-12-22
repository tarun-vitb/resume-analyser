"""
NLP & Embedding Engine
Optimized for semantic similarity and efficient embedding generation
"""

import os
import logging
import numpy as np
import pickle
from typing import List, Dict, Tuple, Optional, Union
from sentence_transformers import SentenceTransformer
import torch
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import hashlib
import json
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmbeddingCache:
    """Efficient caching system for embeddings to optimize API usage"""
    
    def __init__(self, cache_dir: str = "cache/embeddings"):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.cache_file = self.cache_dir / "embedding_cache.pkl"
        self.cache = self._load_cache()
    
    def _load_cache(self) -> Dict:
        """Load existing cache or create new one"""
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'rb') as f:
                    return pickle.load(f)
            except Exception as e:
                logger.warning(f"Could not load cache: {e}")
        return {}
    
    def _save_cache(self):
        """Save cache to disk"""
        try:
            with open(self.cache_file, 'wb') as f:
                pickle.dump(self.cache, f)
        except Exception as e:
            logger.error(f"Could not save cache: {e}")
    
    def _get_text_hash(self, text: str) -> str:
        """Generate hash for text to use as cache key"""
        return hashlib.md5(text.encode()).hexdigest()
    
    def get_embedding(self, text: str) -> Optional[np.ndarray]:
        """Get cached embedding if available"""
        text_hash = self._get_text_hash(text)
        return self.cache.get(text_hash)
    
    def store_embedding(self, text: str, embedding: np.ndarray):
        """Store embedding in cache"""
        text_hash = self._get_text_hash(text)
        self.cache[text_hash] = embedding
        
        # Save cache every 10 new embeddings to avoid frequent I/O
        if len(self.cache) % 10 == 0:
            self._save_cache()
    
    def clear_cache(self):
        """Clear all cached embeddings"""
        self.cache.clear()
        if self.cache_file.exists():
            self.cache_file.unlink()

class NLPEngine:
    """Advanced NLP engine with optimized embedding generation"""
    
    def __init__(self, 
                 model_name: str = "all-MiniLM-L6-v2",
                 use_gpu: bool = None,
                 cache_embeddings: bool = True):
        """
        Initialize NLP engine with specified model
        
        Args:
            model_name: SentenceTransformer model name (optimized for speed/accuracy balance)
            use_gpu: Whether to use GPU (auto-detect if None)
            cache_embeddings: Whether to cache embeddings for efficiency
        """
        self.model_name = model_name
        self.cache_embeddings = cache_embeddings
        
        # Initialize embedding cache
        if cache_embeddings:
            self.cache = EmbeddingCache()
        
        # Auto-detect GPU availability
        if use_gpu is None:
            use_gpu = torch.cuda.is_available()
        
        self.device = "cuda" if use_gpu else "cpu"
        
        # Load SentenceTransformer model
        try:
            self.model = SentenceTransformer(model_name, device=self.device)
            logger.info(f"Loaded {model_name} on {self.device}")
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {e}")
            # Fallback to smaller model
            self.model_name = "all-MiniLM-L6-v2"
            self.model = SentenceTransformer(self.model_name, device=self.device)
            logger.info(f"Fallback to {self.model_name}")
        
        # Initialize TF-IDF for keyword extraction
        self.tfidf = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2),
            lowercase=True
        )
        
        # Common job-related keywords for enhanced matching
        self.job_keywords = {
            'technical_skills': [
                'python', 'java', 'javascript', 'react', 'angular', 'node.js',
                'sql', 'mongodb', 'aws', 'docker', 'kubernetes', 'git',
                'machine learning', 'data science', 'artificial intelligence'
            ],
            'soft_skills': [
                'leadership', 'communication', 'teamwork', 'problem solving',
                'project management', 'analytical thinking', 'creativity'
            ],
            'experience_indicators': [
                'years experience', 'senior', 'lead', 'manager', 'director',
                'developed', 'implemented', 'managed', 'led', 'designed'
            ]
        }

    def preprocess_text(self, text: str) -> str:
        """Preprocess text for better embedding quality"""
        if not text:
            return ""
        
        # Basic cleaning
        text = text.strip()
        
        # Remove excessive whitespace
        import re
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that don't add semantic value
        text = re.sub(r'[^\w\s.,!?-]', ' ', text)
        
        return text

    def generate_embedding(self, text: str, use_cache: bool = True) -> np.ndarray:
        """Generate embedding for text with caching support"""
        if not text:
            return np.zeros(self.model.get_sentence_embedding_dimension())
        
        # Preprocess text
        processed_text = self.preprocess_text(text)
        
        # Check cache first
        if use_cache and self.cache_embeddings:
            cached_embedding = self.cache.get_embedding(processed_text)
            if cached_embedding is not None:
                return cached_embedding
        
        # Generate new embedding
        try:
            embedding = self.model.encode(processed_text, convert_to_numpy=True)
            
            # Store in cache
            if use_cache and self.cache_embeddings:
                self.cache.store_embedding(processed_text, embedding)
            
            return embedding
            
        except Exception as e:
            logger.error(f"Error generating embedding: {e}")
            return np.zeros(self.model.get_sentence_embedding_dimension())

    def generate_batch_embeddings(self, texts: List[str], batch_size: int = 32) -> np.ndarray:
        """Generate embeddings for multiple texts efficiently"""
        if not texts:
            return np.array([])
        
        embeddings = []
        
        # Process in batches for memory efficiency
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i + batch_size]
            
            # Check cache for each text
            batch_embeddings = []
            uncached_texts = []
            uncached_indices = []
            
            for j, text in enumerate(batch_texts):
                processed_text = self.preprocess_text(text)
                
                if self.cache_embeddings:
                    cached_embedding = self.cache.get_embedding(processed_text)
                    if cached_embedding is not None:
                        batch_embeddings.append(cached_embedding)
                        continue
                
                # Text not in cache
                uncached_texts.append(processed_text)
                uncached_indices.append(len(batch_embeddings))
                batch_embeddings.append(None)  # Placeholder
            
            # Generate embeddings for uncached texts
            if uncached_texts:
                try:
                    new_embeddings = self.model.encode(uncached_texts, convert_to_numpy=True)
                    
                    # Fill in the placeholders and cache new embeddings
                    for idx, embedding in zip(uncached_indices, new_embeddings):
                        batch_embeddings[idx] = embedding
                        
                        if self.cache_embeddings:
                            self.cache.store_embedding(uncached_texts[uncached_indices.index(idx)], embedding)
                
                except Exception as e:
                    logger.error(f"Error in batch embedding generation: {e}")
                    # Fill remaining placeholders with zeros
                    dim = self.model.get_sentence_embedding_dimension()
                    for i, emb in enumerate(batch_embeddings):
                        if emb is None:
                            batch_embeddings[i] = np.zeros(dim)
            
            embeddings.extend(batch_embeddings)
        
        return np.array(embeddings)

    def compute_semantic_similarity(self, 
                                  text1: str, 
                                  text2: str, 
                                  method: str = "cosine") -> float:
        """Compute semantic similarity between two texts"""
        
        # Generate embeddings
        emb1 = self.generate_embedding(text1)
        emb2 = self.generate_embedding(text2)
        
        if method == "cosine":
            # Reshape for sklearn
            emb1 = emb1.reshape(1, -1)
            emb2 = emb2.reshape(1, -1)
            similarity = cosine_similarity(emb1, emb2)[0][0]
        else:
            # Dot product similarity
            similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
        
        # Ensure similarity is between 0 and 1
        return max(0.0, min(1.0, similarity))

    def compute_multi_similarity(self, 
                               resume_text: str, 
                               job_descriptions: List[str]) -> List[float]:
        """Compute similarity between resume and multiple job descriptions"""
        
        resume_embedding = self.generate_embedding(resume_text)
        job_embeddings = self.generate_batch_embeddings(job_descriptions)
        
        similarities = []
        for job_emb in job_embeddings:
            # Reshape for sklearn
            resume_emb_reshaped = resume_embedding.reshape(1, -1)
            job_emb_reshaped = job_emb.reshape(1, -1)
            
            similarity = cosine_similarity(resume_emb_reshaped, job_emb_reshaped)[0][0]
            similarities.append(max(0.0, min(1.0, similarity)))
        
        return similarities

    def extract_keywords(self, text: str, top_k: int = 20) -> List[Tuple[str, float]]:
        """Extract important keywords using TF-IDF"""
        try:
            # Fit TF-IDF on the text (treating it as a single document)
            tfidf_matrix = self.tfidf.fit_transform([text])
            feature_names = self.tfidf.get_feature_names_out()
            
            # Get TF-IDF scores
            scores = tfidf_matrix.toarray()[0]
            
            # Create keyword-score pairs
            keyword_scores = list(zip(feature_names, scores))
            
            # Sort by score and return top k
            keyword_scores.sort(key=lambda x: x[1], reverse=True)
            
            return keyword_scores[:top_k]
            
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return []

    def analyze_text_quality(self, text: str) -> Dict[str, Union[float, int, bool]]:
        """Analyze text quality for resume optimization"""
        
        analysis = {
            'word_count': len(text.split()),
            'sentence_count': len([s for s in text.split('.') if s.strip()]),
            'avg_sentence_length': 0,
            'has_action_words': False,
            'has_quantifiable_achievements': False,
            'readability_score': 0.0,
            'technical_keyword_density': 0.0,
            'soft_skill_mentions': 0
        }
        
        words = text.split()
        sentences = [s.strip() for s in text.split('.') if s.strip()]
        
        if len(sentences) > 0:
            analysis['avg_sentence_length'] = len(words) / len(sentences)
        
        # Check for action words
        action_words = ['developed', 'implemented', 'managed', 'led', 'created', 
                       'designed', 'improved', 'optimized', 'achieved', 'delivered']
        analysis['has_action_words'] = any(word in text.lower() for word in action_words)
        
        # Check for quantifiable achievements (numbers, percentages)
        import re
        numbers = re.findall(r'\d+%?', text)
        analysis['has_quantifiable_achievements'] = len(numbers) > 0
        
        # Simple readability (Flesch-like approximation)
        if len(sentences) > 0 and len(words) > 0:
            avg_sentence_len = len(words) / len(sentences)
            # Simplified readability score
            analysis['readability_score'] = max(0, min(100, 100 - avg_sentence_len * 2))
        
        # Technical keyword density
        tech_keywords = self.job_keywords['technical_skills']
        tech_mentions = sum(1 for keyword in tech_keywords if keyword in text.lower())
        analysis['technical_keyword_density'] = tech_mentions / len(words) * 100 if words else 0
        
        # Soft skill mentions
        soft_skills = self.job_keywords['soft_skills']
        analysis['soft_skill_mentions'] = sum(1 for skill in soft_skills if skill in text.lower())
        
        return analysis

    def suggest_improvements(self, resume_text: str, job_description: str) -> List[str]:
        """Generate improvement suggestions based on text analysis"""
        suggestions = []
        
        # Analyze resume quality
        quality_analysis = self.analyze_text_quality(resume_text)
        
        # Extract keywords from job description
        job_keywords = self.extract_keywords(job_description, top_k=15)
        job_keyword_set = {kw[0].lower() for kw in job_keywords}
        
        # Check for missing important keywords
        resume_lower = resume_text.lower()
        missing_keywords = [kw for kw in job_keyword_set if kw not in resume_lower]
        
        if len(missing_keywords) > 5:
            suggestions.append(f"Consider including these relevant keywords: {', '.join(missing_keywords[:5])}")
        
        # Word count suggestions
        if quality_analysis['word_count'] < 200:
            suggestions.append("Your resume seems brief. Consider adding more details about your experience and achievements.")
        elif quality_analysis['word_count'] > 800:
            suggestions.append("Your resume might be too lengthy. Consider condensing to highlight key achievements.")
        
        # Action words
        if not quality_analysis['has_action_words']:
            suggestions.append("Use more action words like 'developed', 'implemented', 'managed', or 'led' to make your experience more impactful.")
        
        # Quantifiable achievements
        if not quality_analysis['has_quantifiable_achievements']:
            suggestions.append("Include quantifiable achievements with numbers or percentages to demonstrate your impact.")
        
        # Technical keywords
        if quality_analysis['technical_keyword_density'] < 2.0:
            suggestions.append("Consider including more technical skills and tools relevant to the position.")
        
        # Readability
        if quality_analysis['readability_score'] < 50:
            suggestions.append("Consider using shorter sentences and simpler language for better readability.")
        
        return suggestions

    def get_model_info(self) -> Dict[str, str]:
        """Get information about the loaded model"""
        return {
            'model_name': self.model_name,
            'device': self.device,
            'embedding_dimension': str(self.model.get_sentence_embedding_dimension()),
            'cache_enabled': str(self.cache_embeddings)
        }
