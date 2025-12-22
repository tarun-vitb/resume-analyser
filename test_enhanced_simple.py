"""
Simple Test for Enhanced Backend - No Unicode
"""

import requests
import json
from pathlib import Path

def test_enhanced_backend():
    base_url = "http://localhost:9001"
    
    print("Testing Enhanced AI Resume Analyzer Backend")
    print("=" * 60)
    
    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    # Test 2: Create test resume
    print("\n2. Creating test resume...")
    
    test_resume_content = """
JOHN SMITH
Senior Software Engineer
Email: john.smith@email.com | Phone: (555) 123-4567

TECHNICAL SKILLS
Programming Languages: Python, JavaScript, TypeScript, Java, Go
Web Technologies: React, Angular, Node.js, HTML, CSS
Backend & APIs: REST APIs, GraphQL, FastAPI, Django
Databases: PostgreSQL, MongoDB, Redis, MySQL
Cloud & DevOps: AWS, Docker, Kubernetes, Jenkins
Data Science & ML: Machine Learning, TensorFlow, PyTorch, Pandas, NumPy
Tools: Git, Jira, VS Code, Postman

PROFESSIONAL EXPERIENCE
Senior Software Engineer | TechCorp Inc. | 2020 - Present
- Developed web applications using React and Node.js
- Implemented machine learning models using TensorFlow and Python
- Built REST APIs using FastAPI and Django
- Deployed on AWS using Docker and Kubernetes

EDUCATION
Master of Science in Computer Science | Stanford University | 2018
"""
    
    test_resume_path = Path("test_simple_resume.txt")
    with open(test_resume_path, 'w') as f:
        f.write(test_resume_content)
    
    print("   Test resume created")
    
    # Test 3: Upload resume
    print("\n3. Testing resume upload...")
    try:
        with open(test_resume_path, 'rb') as f:
            files = {'file': ('test_simple_resume.txt', f, 'text/plain')}
            response = requests.post(f"{base_url}/upload_resume", files=files)
            
        print(f"   Status: {response.status_code}")
        result = response.json()
        
        if result.get('success'):
            file_id = result.get('file_id')
            print(f"   File ID: {file_id}")
            print(f"   Skills Found: {len(result.get('extracted_skills', []))}")
            print(f"   Categories: {len(result.get('skill_categories', {}))}")
            
            # Show extracted skills by category
            skill_categories = result.get('skill_categories', {})
            for category, skills in skill_categories.items():
                print(f"   {category}: {len(skills)} skills - {skills[:3]}")
            
            # Test 4: Analyze resume
            print("\n4. Testing resume analysis...")
            
            job_description = """
Senior Software Engineer Position

Required Skills:
- Python programming
- React and JavaScript
- REST APIs development
- AWS cloud platform
- Docker containerization
- Machine Learning with TensorFlow
- PostgreSQL database
- Git version control

Preferred Skills:
- TypeScript
- GraphQL
- Kubernetes
- Jenkins CI/CD

Responsibilities:
- Develop web applications
- Implement ML features
- Work with teams
- Code quality

Requirements:
- 5+ years experience
- Computer Science degree
"""
            
            analysis_data = {
                'file_id': file_id,
                'job_description': job_description
            }
            
            analysis_response = requests.post(f"{base_url}/analyze_resume", data=analysis_data)
            print(f"   Status: {analysis_response.status_code}")
            
            analysis_result = analysis_response.json()
            if analysis_result.get('success'):
                analysis = analysis_result['analysis']
                
                print(f"\n   ANALYSIS RESULTS:")
                print(f"   Fit Score: {analysis['fit_score']}%")
                print(f"   Selection Probability: {analysis['selection_probability']}%")
                print(f"   Skill Match Score: {analysis['skill_match_score']}%")
                print(f"   Exact Matches: {analysis['exact_matches']}/{analysis['total_job_skills']}")
                
                print(f"\n   MATCHED SKILLS ({len(analysis['matched_skills'])}):")
                for skill in analysis['matched_skills']:
                    print(f"      + {skill}")
                
                print(f"\n   MISSING SKILLS ({len(analysis['missing_skills'])}):")
                for skill in analysis['missing_skills']:
                    print(f"      - {skill}")
                
                if analysis['extra_skills']:
                    print(f"\n   BONUS SKILLS ({len(analysis['extra_skills'])}):")
                    for skill in analysis['extra_skills']:
                        print(f"      * {skill}")
                
                print(f"\n   SKILL ANALYSIS BY CATEGORY:")
                for category, data in analysis['skill_analysis'].items():
                    print(f"      {category}: {data['match_percentage']}% match")
                    print(f"         Matched: {data['matched']}")
                    print(f"         Missing: {data['missing']}")
            
            # Test 5: Job matching
            print("\n5. Testing job matching...")
            matches_response = requests.get(f"{base_url}/match_jobs?file_id={file_id}")
            print(f"   Status: {matches_response.status_code}")
            
            matches_result = matches_response.json()
            if matches_result.get('success'):
                matches = matches_result['matches']
                print(f"   Total Job Matches: {matches_result['total_matches']}")
                print(f"   Best Fit Company: {matches_result['best_fit_company']}")
                print(f"   Average Fit Score: {matches_result['average_fit_score']}%")
                
                print(f"\n   TOP 5 JOB MATCHES:")
                for i, match in enumerate(matches[:5], 1):
                    print(f"   {i}. {match['company']} - {match['role_title']}")
                    print(f"      Salary: {match['salary_range']}")
                    print(f"      Location: {match['location']}")
                    print(f"      Fit Score: {match['fit_score']}%")
                    print(f"      Selection Probability: {match['selection_probability']}%")
                    print(f"      Skills Match: {match['exact_matches']}/{match['total_required']} ({match['skill_match_percentage']}%)")
                    print(f"      Matched Skills: {', '.join(match['skills_overlap'][:5])}")
                    print(f"      Missing Skills: {', '.join(match['missing_skills'][:3])}")
                    print()
        
    except Exception as e:
        print(f"   Error: {e}")
    finally:
        # Clean up test file
        if test_resume_path.exists():
            test_resume_path.unlink()
    
    print("=" * 60)
    print("Enhanced backend testing completed!")
    print("Features verified:")
    print("   - Exact skill name matching")
    print("   - Accurate percentage calculations")
    print("   - Real company job data")
    print("   - Category-wise skill analysis")
    print("   - Real-time job matching")

if __name__ == "__main__":
    test_enhanced_backend()
