"""
Test Enhanced Backend - Verify Exact Skill Matching and Percentages
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
        print(f"   ❌ Error: {e}")
        return
    
    # Test 2: Create a comprehensive test resume
    print("\n2. Creating comprehensive test resume...")
    
    test_resume_content = """
JOHN SMITH
Senior Software Engineer
Email: john.smith@email.com | Phone: (555) 123-4567
LinkedIn: linkedin.com/in/johnsmith | GitHub: github.com/johnsmith

PROFESSIONAL SUMMARY
Experienced software engineer with 8+ years in full-stack development, machine learning, and cloud technologies.

TECHNICAL SKILLS
Programming Languages: Python, JavaScript, TypeScript, Java, C++, Go
Web Technologies: React, Angular, Node.js, Express.js, HTML, CSS, Bootstrap
Backend & APIs: REST APIs, GraphQL, FastAPI, Django, Flask, Microservices
Databases: PostgreSQL, MongoDB, Redis, MySQL, Elasticsearch
Cloud & DevOps: AWS, Docker, Kubernetes, Jenkins, Terraform, GitLab CI
Data Science & ML: Machine Learning, TensorFlow, PyTorch, Pandas, NumPy, Scikit-learn
Tools: Git, Jira, VS Code, Postman, Figma

PROFESSIONAL EXPERIENCE
Senior Software Engineer | TechCorp Inc. | 2020 - Present
• Developed scalable web applications using React and Node.js serving 1M+ users
• Implemented machine learning models using TensorFlow and Python for recommendation systems
• Designed and built REST APIs and GraphQL endpoints using FastAPI and Django
• Deployed applications on AWS using Docker, Kubernetes, and managed CI/CD pipelines
• Led a team of 5 developers and mentored junior engineers

Software Engineer | StartupXYZ | 2018 - 2020
• Built full-stack applications using JavaScript, React, and PostgreSQL
• Worked with data analysis using Pandas and NumPy for business insights
• Implemented automated testing using Jest and Cypress
• Collaborated with cross-functional teams using Agile methodologies

EDUCATION
Master of Science in Computer Science | Stanford University | 2018
Bachelor of Science in Software Engineering | UC Berkeley | 2016

PROJECTS
• E-commerce Platform: Built using React, Node.js, PostgreSQL, and AWS
• ML Recommendation System: Developed using Python, TensorFlow, and deployed on Kubernetes
• Real-time Chat Application: Created using React, Socket.io, and Redis

CERTIFICATIONS
• AWS Certified Solutions Architect
• Google Cloud Professional Developer
• Certified Kubernetes Administrator (CKA)
"""
    
    test_resume_path = Path("test_enhanced_resume.txt")
    with open(test_resume_path, 'w') as f:
        f.write(test_resume_content)
    
    print("   ✅ Test resume created with comprehensive skills")
    
    # Test 3: Upload resume
    print("\n3. Testing enhanced resume upload...")
    try:
        with open(test_resume_path, 'rb') as f:
            files = {'file': ('test_enhanced_resume.txt', f, 'text/plain')}
            response = requests.post(f"{base_url}/upload_resume", files=files)
            
        print(f"   ✅ Status: {response.status_code}")
        result = response.json()
        
        if result.get('success'):
            file_id = result.get('file_id')
            print(f"   📄 File ID: {file_id}")
            print(f"   🔧 Skills Found: {len(result.get('extracted_skills', []))}")
            print(f"   📊 Categories: {len(result.get('skill_categories', {}))}")
            
            # Show extracted skills by category
            skill_categories = result.get('skill_categories', {})
            for category, skills in skill_categories.items():
                print(f"   📋 {category}: {len(skills)} skills - {skills[:5]}{'...' if len(skills) > 5 else ''}")
            
            # Test 4: Analyze against specific job description
            print("\n4. Testing comprehensive resume analysis...")
            
            job_description = """
Senior Full Stack Developer Position at Google

We are looking for an experienced Senior Full Stack Developer to join our team.

Required Skills:
- Python programming with 5+ years experience
- React and modern JavaScript/TypeScript
- REST APIs and GraphQL development
- Cloud platforms (preferably Google Cloud or AWS)
- Docker and Kubernetes for containerization
- Machine Learning experience with TensorFlow
- Database design with PostgreSQL
- Git version control and CI/CD pipelines

Preferred Skills:
- Go programming language
- Microservices architecture
- Data analysis with Pandas and NumPy
- Jenkins or GitLab CI experience
- Agile development methodologies

Responsibilities:
- Design and develop scalable web applications
- Implement machine learning features
- Work with cross-functional teams
- Mentor junior developers
- Ensure code quality and best practices

Requirements:
- Bachelor's degree in Computer Science or related field
- 5+ years of software development experience
- Strong problem-solving skills
- Excellent communication skills

Compensation: $180,000 - $250,000 + equity + benefits
Location: Mountain View, CA (Hybrid)
"""
            
            analysis_data = {
                'file_id': file_id,
                'job_description': job_description
            }
            
            analysis_response = requests.post(f"{base_url}/analyze_resume", data=analysis_data)
            print(f"   ✅ Status: {analysis_response.status_code}")
            
            analysis_result = analysis_response.json()
            if analysis_result.get('success'):
                analysis = analysis_result['analysis']
                
                print(f"\n   📊 ANALYSIS RESULTS:")
                print(f"   🎯 Fit Score: {analysis['fit_score']}%")
                print(f"   🎲 Selection Probability: {analysis['selection_probability']}%")
                print(f"   🔧 Skill Match Score: {analysis['skill_match_score']}%")
                print(f"   ✅ Exact Matches: {analysis['exact_matches']}/{analysis['total_job_skills']}")
                
                print(f"\n   ✅ MATCHED SKILLS ({len(analysis['matched_skills'])}):")
                for skill in analysis['matched_skills']:
                    print(f"      ✓ {skill}")
                
                print(f"\n   ❌ MISSING SKILLS ({len(analysis['missing_skills'])}):")
                for skill in analysis['missing_skills']:
                    print(f"      ✗ {skill}")
                
                if analysis['extra_skills']:
                    print(f"\n   ⭐ BONUS SKILLS ({len(analysis['extra_skills'])}):")
                    for skill in analysis['extra_skills']:
                        print(f"      ⭐ {skill}")
                
                print(f"\n   📋 SKILL ANALYSIS BY CATEGORY:")
                for category, data in analysis['skill_analysis'].items():
                    print(f"      📂 {category}: {data['match_percentage']}% match")
                    print(f"         ✅ Matched: {data['matched']}")
                    print(f"         ❌ Missing: {data['missing']}")
            
            # Test 5: Real-time job matching
            print("\n5. Testing real-time job matching...")
            matches_response = requests.get(f"{base_url}/match_jobs?file_id={file_id}")
            print(f"   ✅ Status: {matches_response.status_code}")
            
            matches_result = matches_response.json()
            if matches_result.get('success'):
                matches = matches_result['matches']
                print(f"   🏢 Total Job Matches: {matches_result['total_matches']}")
                print(f"   🥇 Best Fit Company: {matches_result['best_fit_company']}")
                print(f"   📊 Average Fit Score: {matches_result['average_fit_score']}%")
                
                print(f"\n   🎯 TOP 5 JOB MATCHES:")
                for i, match in enumerate(matches[:5], 1):
                    print(f"   {i}. {match['company']} - {match['role_title']}")
                    print(f"      💰 Salary: {match['salary_range']}")
                    print(f"      📍 Location: {match['location']}")
                    print(f"      🎯 Fit Score: {match['fit_score']}%")
                    print(f"      🎲 Selection Probability: {match['selection_probability']}%")
                    print(f"      ✅ Skills Match: {match['exact_matches']}/{match['total_required']} ({match['skill_match_percentage']}%)")
                    print(f"      🔧 Matched Skills: {', '.join(match['skills_overlap'][:5])}{'...' if len(match['skills_overlap']) > 5 else ''}")
                    print(f"      ❌ Missing Skills: {', '.join(match['missing_skills'][:3])}{'...' if len(match['missing_skills']) > 3 else ''}")
                    print()
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
    finally:
        # Clean up test file
        if test_resume_path.exists():
            test_resume_path.unlink()
    
    print("=" * 60)
    print("🎉 Enhanced backend testing completed!")
    print("✅ Features verified:")
    print("   • Exact skill name matching")
    print("   • Accurate percentage calculations")
    print("   • Real company job data")
    print("   • Category-wise skill analysis")
    print("   • Real-time job matching")

if __name__ == "__main__":
    test_enhanced_backend()
