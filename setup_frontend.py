#!/usr/bin/env python3
"""
Frontend Setup Script - Fix Frontend Issues
Creates a working React frontend from scratch
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def print_banner():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║    🎨 FRONTEND SETUP - FIXING REACT APPLICATION            ║
║                                                              ║
║    Creating a working React frontend for your backend       ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
""")

def check_node():
    """Check if Node.js is available"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Node.js {result.stdout.strip()}")
            return True
        else:
            print("❌ Node.js not found")
            return False
    except FileNotFoundError:
        print("❌ Node.js not found")
        return False

def create_simple_frontend():
    """Create a simple HTML frontend that works with the backend"""
    print("🎨 Creating simple HTML frontend...")
    
    # Create static directory
    static_dir = Path("static")
    static_dir.mkdir(exist_ok=True)
    
    # Create index.html
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Resume Analyzer</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        primary: '#3b82f6',
                        secondary: '#8b5cf6'
                    }
                }
            }
        }
    </script>
</head>
<body class="bg-gradient-to-br from-blue-50 to-indigo-100 min-h-screen">
    <div class="container mx-auto px-4 py-8">
        <!-- Header -->
        <div class="text-center mb-12">
            <h1 class="text-4xl font-bold text-gray-900 mb-4">
                🚀 AI Resume Analyzer
            </h1>
            <p class="text-xl text-gray-600">
                Upload your resume and get AI-powered analysis instantly
            </p>
        </div>

        <!-- Upload Section -->
        <div class="max-w-2xl mx-auto bg-white rounded-2xl shadow-lg p-8 mb-8">
            <h2 class="text-2xl font-semibold mb-6">Upload Resume</h2>
            
            <div class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center mb-6">
                <input type="file" id="resumeFile" accept=".pdf,.docx,.doc,.txt" class="hidden">
                <div id="uploadArea" class="cursor-pointer" onclick="document.getElementById('resumeFile').click()">
                    <div class="text-4xl mb-4">📄</div>
                    <p class="text-gray-600">Click to upload your resume</p>
                    <p class="text-sm text-gray-500 mt-2">Supports PDF, DOCX, DOC, TXT</p>
                </div>
            </div>

            <div class="mb-6">
                <label class="block text-sm font-medium text-gray-700 mb-2">Job Description</label>
                <textarea id="jobDescription" rows="6" class="w-full border border-gray-300 rounded-lg p-3 focus:ring-2 focus:ring-blue-500 focus:border-transparent" placeholder="Paste the job description here..."></textarea>
            </div>

            <button id="analyzeBtn" onclick="analyzeResume()" class="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-3 px-6 rounded-lg font-semibold hover:from-blue-700 hover:to-purple-700 transition-all duration-200">
                Analyze Resume
            </button>
        </div>

        <!-- Results Section -->
        <div id="results" class="max-w-4xl mx-auto hidden">
            <div class="bg-white rounded-2xl shadow-lg p-8 mb-8">
                <h2 class="text-2xl font-semibold mb-6">Analysis Results</h2>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                    <div class="text-center">
                        <div id="fitScore" class="text-4xl font-bold text-blue-600 mb-2">--</div>
                        <div class="text-gray-600">Fit Score</div>
                    </div>
                    <div class="text-center">
                        <div id="selectionProb" class="text-4xl font-bold text-green-600 mb-2">--</div>
                        <div class="text-gray-600">Selection Probability</div>
                    </div>
                    <div class="text-center">
                        <div id="skillMatch" class="text-4xl font-bold text-purple-600 mb-2">--</div>
                        <div class="text-gray-600">Skill Match</div>
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                    <div>
                        <h3 class="text-lg font-semibold text-green-600 mb-3">✅ Matched Skills</h3>
                        <div id="matchedSkills" class="flex flex-wrap gap-2"></div>
                    </div>
                    <div>
                        <h3 class="text-lg font-semibold text-red-600 mb-3">❌ Missing Skills</h3>
                        <div id="missingSkills" class="flex flex-wrap gap-2"></div>
                    </div>
                </div>

                <div class="mt-8">
                    <h3 class="text-lg font-semibold text-blue-600 mb-3">💡 AI Feedback</h3>
                    <div id="feedback" class="space-y-2"></div>
                </div>
            </div>

            <!-- Job Matches -->
            <div class="bg-white rounded-2xl shadow-lg p-8">
                <h2 class="text-2xl font-semibold mb-6">Job Matches</h2>
                <div id="jobMatches" class="space-y-4"></div>
            </div>
        </div>

        <!-- Loading -->
        <div id="loading" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center hidden">
            <div class="bg-white rounded-lg p-8 text-center">
                <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                <p class="text-gray-600">Analyzing your resume...</p>
            </div>
        </div>
    </div>

    <script>
        let currentFileId = null;

        // Handle file upload
        document.getElementById('resumeFile').addEventListener('change', async function(e) {
            const file = e.target.files[0];
            if (!file) return;

            const formData = new FormData();
            formData.append('file', file);

            try {
                const response = await fetch('http://localhost:9000/upload_resume', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();
                if (result.success) {
                    currentFileId = result.file_id;
                    document.getElementById('uploadArea').innerHTML = `
                        <div class="text-4xl mb-4">✅</div>
                        <p class="text-green-600 font-medium">${file.name}</p>
                        <p class="text-sm text-gray-500 mt-2">Ready for analysis</p>
                    `;
                } else {
                    alert('Upload failed: ' + result.message);
                }
            } catch (error) {
                alert('Upload error: ' + error.message);
            }
        });

        // Analyze resume
        async function analyzeResume() {
            if (!currentFileId) {
                alert('Please upload a resume first');
                return;
            }

            const jobDescription = document.getElementById('jobDescription').value;
            if (!jobDescription.trim()) {
                alert('Please enter a job description');
                return;
            }

            document.getElementById('loading').classList.remove('hidden');

            try {
                const formData = new FormData();
                formData.append('file_id', currentFileId);
                formData.append('job_description', jobDescription);

                const response = await fetch('http://localhost:9000/analyze_resume', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();
                document.getElementById('loading').classList.add('hidden');

                if (result.success) {
                    displayResults(result.analysis);
                    await loadJobMatches();
                } else {
                    alert('Analysis failed: ' + result.message);
                }
            } catch (error) {
                document.getElementById('loading').classList.add('hidden');
                alert('Analysis error: ' + error.message);
            }
        }

        // Display results
        function displayResults(analysis) {
            document.getElementById('fitScore').textContent = analysis.fit_score + '%';
            document.getElementById('selectionProb').textContent = analysis.selection_probability + '%';
            document.getElementById('skillMatch').textContent = analysis.skill_match_score + '%';

            // Matched skills
            const matchedSkillsDiv = document.getElementById('matchedSkills');
            matchedSkillsDiv.innerHTML = '';
            analysis.matched_skills.forEach(skill => {
                const span = document.createElement('span');
                span.className = 'px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm';
                span.textContent = skill;
                matchedSkillsDiv.appendChild(span);
            });

            // Missing skills
            const missingSkillsDiv = document.getElementById('missingSkills');
            missingSkillsDiv.innerHTML = '';
            analysis.missing_skills.forEach(skill => {
                const span = document.createElement('span');
                span.className = 'px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm';
                span.textContent = skill;
                missingSkillsDiv.appendChild(span);
            });

            // Feedback
            const feedbackDiv = document.getElementById('feedback');
            feedbackDiv.innerHTML = '';
            analysis.feedback.forEach(item => {
                const div = document.createElement('div');
                div.className = 'p-3 bg-blue-50 rounded-lg';
                div.textContent = '💡 ' + item;
                feedbackDiv.appendChild(div);
            });

            document.getElementById('results').classList.remove('hidden');
        }

        // Load job matches
        async function loadJobMatches() {
            try {
                const response = await fetch(`http://localhost:9000/match_jobs?file_id=${currentFileId}`);
                const result = await response.json();

                if (result.success) {
                    const jobMatchesDiv = document.getElementById('jobMatches');
                    jobMatchesDiv.innerHTML = '';

                    result.matches.forEach(match => {
                        const div = document.createElement('div');
                        div.className = 'border border-gray-200 rounded-lg p-4';
                        div.innerHTML = `
                            <div class="flex justify-between items-start mb-2">
                                <h3 class="font-semibold text-lg">${match.role_title}</h3>
                                <span class="text-sm font-medium px-2 py-1 bg-blue-100 text-blue-800 rounded">${match.fit_score}%</span>
                            </div>
                            <p class="text-gray-600 mb-2">${match.company}</p>
                            <p class="text-sm text-gray-500">${match.salary_range || 'Salary not specified'}</p>
                            <div class="mt-3">
                                <div class="text-sm text-green-600">Matched: ${match.skills_overlap.join(', ')}</div>
                                <div class="text-sm text-red-600 mt-1">Missing: ${match.missing_skills.join(', ')}</div>
                            </div>
                        `;
                        jobMatchesDiv.appendChild(div);
                    });
                }
            } catch (error) {
                console.error('Error loading job matches:', error);
            }
        }
    </script>
</body>
</html>"""
    
    with open(static_dir / "index.html", "w") as f:
        f.write(html_content)
    
    print("✅ Simple HTML frontend created")
    return True

def update_backend_for_static():
    """Update backend to serve static files"""
    print("🔧 Updating backend to serve static frontend...")
    
    # Read the simple backend file
    backend_file = Path("simple_backend.py")
    if not backend_file.exists():
        print("❌ simple_backend.py not found")
        return False
    
    with open(backend_file, "r") as f:
        content = f.read()
    
    # Add static file serving if not already present
    if "StaticFiles" not in content:
        # Add import
        content = content.replace(
            "from fastapi import FastAPI, File, UploadFile, Form, HTTPException",
            "from fastapi import FastAPI, File, UploadFile, Form, HTTPException\nfrom fastapi.staticfiles import StaticFiles"
        )
        
        # Add static files mounting before the main block
        static_mount = '''
# Mount static files for frontend
if Path("static").exists():
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
'''
        
        content = content.replace(
            'if __name__ == "__main__":',
            static_mount + '\nif __name__ == "__main__":'
        )
        
        with open(backend_file, "w") as f:
            f.write(content)
        
        print("✅ Backend updated to serve static files")
    else:
        print("✅ Backend already configured for static files")
    
    return True

def main():
    """Main setup function"""
    print_banner()
    
    print("🔍 Checking Node.js availability...")
    node_available = check_node()
    
    if not node_available:
        print("\n⚠️  Node.js not found. Creating simple HTML frontend instead.")
        print("   This will work with your backend and provide full functionality.")
        
        if create_simple_frontend():
            update_backend_for_static()
            
            print("\n" + "="*60)
            print("✅ FRONTEND SETUP COMPLETE!")
            print("="*60)
            print()
            print("🌐 ACCESS YOUR APPLICATION:")
            print("   1. Start backend: python simple_backend.py")
            print("   2. Open browser: http://localhost:9000")
            print("   3. Use the AI Resume Analyzer!")
            print()
            print("🎨 FEATURES AVAILABLE:")
            print("   ✅ File upload (PDF/DOCX/TXT)")
            print("   ✅ AI-powered analysis")
            print("   ✅ Interactive results")
            print("   ✅ Job matching")
            print("   ✅ Skill gap detection")
            print("   ✅ Beautiful UI with Tailwind CSS")
            print()
            print("📋 NEXT STEPS:")
            print("   1. Run: python simple_backend.py")
            print("   2. Go to: http://localhost:9000")
            print("   3. Upload resume and analyze!")
            print("="*60)
        else:
            print("❌ Failed to create frontend")
    else:
        print("\n✅ Node.js is available!")
        print("   You can use the React frontend in frontend-app/ directory")
        print("   Run: cd frontend-app && npm install && npm run dev")

if __name__ == "__main__":
    main()
