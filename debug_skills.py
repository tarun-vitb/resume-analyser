"""
Debug Skill Extraction
"""

import re
from typing import List, Dict, Any

# Sample skills database for testing
COMPREHENSIVE_SKILLS_DB = {
    "Programming Languages": [
        "Python", "JavaScript", "Java", "C++", "C#", "TypeScript", "Go", "Rust", 
        "PHP", "Ruby", "Swift", "Kotlin", "Scala", "R", "MATLAB", "Perl", "Dart"
    ],
    "Web Technologies": [
        "React", "Angular", "Vue.js", "HTML", "CSS", "Sass", "Less", "Bootstrap",
        "Tailwind CSS", "jQuery", "Node.js", "Express.js", "Next.js"
    ],
    "Data Science & ML": [
        "Machine Learning", "Deep Learning", "Data Analysis", "Pandas", "NumPy",
        "Scikit-learn", "TensorFlow", "PyTorch", "Keras", "OpenCV", "NLTK", "spaCy"
    ]
}

def extract_skills_enhanced(text: str):
    """Enhanced skill extraction with exact matching and categorization"""
    print(f"Input text: {text[:200]}...")
    
    text_lower = text.lower()
    print(f"Text lower: {text_lower[:200]}...")
    
    # Clean and normalize text
    text_normalized = re.sub(r'[^\w\s+#.-]', ' ', text_lower)
    text_normalized = re.sub(r'\s+', ' ', text_normalized)
    print(f"Text normalized: {text_normalized[:200]}...")
    
    categorized_skills = {}
    all_found_skills = []
    
    for category, skills_list in COMPREHENSIVE_SKILLS_DB.items():
        found_skills = []
        print(f"\nChecking category: {category}")
        
        for skill in skills_list:
            skill_lower = skill.lower()
            skill_patterns = [
                rf'\b{re.escape(skill_lower)}\b',  # Exact word match
                rf'{re.escape(skill_lower)}(?:\s|$|,|\.|;)',  # Word boundary
                rf'(?:^|\s){re.escape(skill_lower)}(?:\s|$)',  # Start/end boundary
            ]
            
            # Special handling for compound skills
            if any(char in skill_lower for char in ['.', '+', '#', '-']):
                skill_patterns.append(re.escape(skill_lower))
            
            for pattern in skill_patterns:
                if re.search(pattern, text_normalized):
                    if skill not in found_skills:
                        found_skills.append(skill)
                        all_found_skills.append(skill)
                        print(f"  Found skill: {skill} (pattern: {pattern})")
                    break
        
        if found_skills:
            categorized_skills[category] = found_skills
    
    print(f"\nFinal results:")
    print(f"Categorized skills: {categorized_skills}")
    print(f"All found skills: {all_found_skills}")
    
    return categorized_skills, all_found_skills

# Test with sample resume text
test_resume = """
John Doe
Software Engineer
Skills: Python, JavaScript, React, Machine Learning, R programming
Experience with TensorFlow and data analysis
"""

test_job = """
Looking for developer with Python, React, Machine Learning experience
"""

print("=== TESTING SKILL EXTRACTION ===")
resume_cats, resume_skills = extract_skills_enhanced(test_resume)
job_cats, job_skills = extract_skills_enhanced(test_job)

print(f"\nResume skills: {resume_skills}")
print(f"Job skills: {job_skills}")

# Test matching
matched_skills = []
missing_skills = []

for job_skill in job_skills:
    if job_skill in resume_skills:
        matched_skills.append(job_skill)
    else:
        missing_skills.append(job_skill)

print(f"\nMatched: {matched_skills}")
print(f"Missing: {missing_skills}")
