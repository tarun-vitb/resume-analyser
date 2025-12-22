#!/usr/bin/env python3
"""
Launch Complete AI Resume Analyzer Website
Frontend + Backend integrated solution
"""

import os
import sys
import subprocess
import time
import threading
import webbrowser
from pathlib import Path

def print_header():
    print("=" * 60)
    print("AI RESUME ANALYZER - COMPLETE WEBSITE LAUNCHER")
    print("=" * 60)
    print("Backend:  http://localhost:9000")
    print("Frontend: Integrated with backend")
    print("=" * 60)

def install_deps():
    """Install only working dependencies"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([
            sys.executable, '-m', 'pip', 'install',
            'fastapi==0.104.1',
            'uvicorn[standard]==0.24.0',
            'python-multipart==0.0.6',
            'pydantic==2.5.0'
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✓ Dependencies installed")
    except:
        print("✓ Using existing dependencies")

def create_integrated_frontend():
    """Create integrated HTML frontend"""
    print("Creating integrated frontend...")
    
    # Create static directory
    static_dir = Path("static")
    static_dir.mkdir(exist_ok=True)
    
    # Create complete HTML frontend
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Resume Analyzer - Complete Website</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .card-hover { transition: all 0.3s ease; }
        .card-hover:hover { transform: translateY(-4px); box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1); }
        .loading { animation: spin 1s linear infinite; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    </style>
</head>
<body class="bg-gray-50 min-h-screen">
    <!-- Navigation -->
    <nav class="bg-white shadow-lg sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex items-center">
                    <div class="flex-shrink-0">
                        <h1 class="text-xl font-bold text-indigo-600">AI Resume Analyzer</h1>
                    </div>
                </div>
                <div class="flex items-center space-x-4">
                    <button onclick="showSection('upload')" class="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md">Analyze</button>
                    <button onclick="showSection('matches')" class="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md">Matches</button>
                    <button onclick="showSection('about')" class="text-gray-700 hover:text-indigo-600 px-3 py-2 rounded-md">About</button>
                </div>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section id="hero" class="gradient-bg text-white py-20">
        <div class="max-w-4xl mx-auto text-center px-4">
            <h1 class="text-5xl font-bold mb-6">AI-Powered Resume Analysis</h1>
            <p class="text-xl mb-8">Upload your resume and get instant AI feedback, skill gap analysis, and job matching</p>
            <button onclick="showSection('upload')" class="bg-white text-indigo-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100 transition-colors">
                Analyze Resume Now
            </button>
        </div>
    </section>

    <!-- Upload Section -->
    <section id="upload" class="py-12 hidden">
        <div class="max-w-4xl mx-auto px-4">
            <div class="bg-white rounded-2xl shadow-lg p-8">
                <h2 class="text-3xl font-bold text-center mb-8">Upload & Analyze Resume</h2>
                
                <!-- File Upload -->
                <div class="mb-8">
                    <div class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-indigo-400 transition-colors">
                        <input type="file" id="resumeFile" accept=".pdf,.docx,.doc,.txt" class="hidden">
                        <div id="uploadArea" class="cursor-pointer" onclick="document.getElementById('resumeFile').click()">
                            <div class="text-6xl mb-4">📄</div>
                            <p class="text-xl text-gray-600 mb-2">Click to upload your resume</p>
                            <p class="text-gray-500">Supports PDF, DOCX, DOC, TXT files</p>
                        </div>
                    </div>
                </div>

                <!-- Job Description -->
                <div class="mb-8">
                    <label class="block text-lg font-semibold text-gray-700 mb-3">Job Description</label>
                    <textarea id="jobDescription" rows="8" class="w-full border border-gray-300 rounded-lg p-4 focus:ring-2 focus:ring-indigo-500 focus:border-transparent" placeholder="Paste the job description here..."></textarea>
                </div>

                <!-- Analyze Button -->
                <button id="analyzeBtn" onclick="analyzeResume()" class="w-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-4 px-8 rounded-lg font-semibold text-lg hover:from-indigo-700 hover:to-purple-700 transition-all duration-200">
                    <span id="analyzeText">Analyze Resume</span>
                    <div id="analyzeSpinner" class="loading border-2 border-white border-t-transparent rounded-full w-5 h-5 ml-2 hidden inline-block"></div>
                </button>
            </div>
        </div>
    </section>

    <!-- Results Section -->
    <section id="results" class="py-12 hidden">
        <div class="max-w-6xl mx-auto px-4">
            <!-- Metrics Cards -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div class="bg-white rounded-xl shadow-lg p-6 text-center card-hover">
                    <div id="fitScore" class="text-4xl font-bold text-indigo-600 mb-2">--</div>
                    <div class="text-gray-600">Fit Score</div>
                </div>
                <div class="bg-white rounded-xl shadow-lg p-6 text-center card-hover">
                    <div id="selectionProb" class="text-4xl font-bold text-green-600 mb-2">--</div>
                    <div class="text-gray-600">Selection Probability</div>
                </div>
                <div class="bg-white rounded-xl shadow-lg p-6 text-center card-hover">
                    <div id="skillMatch" class="text-4xl font-bold text-purple-600 mb-2">--</div>
                    <div class="text-gray-600">Skill Match</div>
                </div>
            </div>

            <!-- Skills Analysis -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                <div class="bg-white rounded-xl shadow-lg p-6">
                    <h3 class="text-xl font-semibold text-green-600 mb-4">✓ Matched Skills</h3>
                    <div id="matchedSkills" class="flex flex-wrap gap-2"></div>
                </div>
                <div class="bg-white rounded-xl shadow-lg p-6">
                    <h3 class="text-xl font-semibold text-red-600 mb-4">✗ Missing Skills</h3>
                    <div id="missingSkills" class="flex flex-wrap gap-2"></div>
                </div>
            </div>

            <!-- AI Feedback -->
            <div class="bg-white rounded-xl shadow-lg p-6 mb-8">
                <h3 class="text-xl font-semibold text-blue-600 mb-4">🤖 AI Feedback</h3>
                <div id="feedback" class="space-y-3"></div>
            </div>

            <!-- Course Recommendations -->
            <div class="bg-white rounded-xl shadow-lg p-6">
                <h3 class="text-xl font-semibold text-purple-600 mb-4">📚 Recommended Courses</h3>
                <div id="courses" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"></div>
            </div>
        </div>
    </section>

    <!-- Job Matches Section -->
    <section id="matches" class="py-12 hidden">
        <div class="max-w-6xl mx-auto px-4">
            <h2 class="text-3xl font-bold text-center mb-8">Job Matches</h2>
            <div id="jobMatches" class="space-y-6"></div>
        </div>
    </section>

    <!-- About Section -->
    <section id="about" class="py-12 hidden">
        <div class="max-w-4xl mx-auto px-4">
            <div class="bg-white rounded-xl shadow-lg p-8">
                <h2 class="text-3xl font-bold text-center mb-8">About AI Resume Analyzer</h2>
                <div class="prose max-w-none">
                    <p class="text-lg text-gray-700 mb-6">
                        Our AI-powered resume analyzer uses advanced machine learning algorithms to provide comprehensive feedback on your resume, helping you land your dream job.
                    </p>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-8">
                        <div>
                            <h3 class="text-xl font-semibold mb-3">Features</h3>
                            <ul class="space-y-2 text-gray-700">
                                <li>✓ AI-powered resume analysis</li>
                                <li>✓ Skill gap detection</li>
                                <li>✓ Job matching algorithms</li>
                                <li>✓ Course recommendations</li>
                                <li>✓ ATS compatibility scoring</li>
                            </ul>
                        </div>
                        <div>
                            <h3 class="text-xl font-semibold mb-3">Technology</h3>
                            <ul class="space-y-2 text-gray-700">
                                <li>• FastAPI Backend</li>
                                <li>• Machine Learning Models</li>
                                <li>• Natural Language Processing</li>
                                <li>• Modern Web Technologies</li>
                                <li>• Responsive Design</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Loading Modal -->
    <div id="loadingModal" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center hidden z-50">
        <div class="bg-white rounded-lg p-8 text-center">
            <div class="loading border-4 border-indigo-200 border-t-indigo-600 rounded-full w-12 h-12 mx-auto mb-4"></div>
            <p class="text-gray-700">Analyzing your resume...</p>
        </div>
    </div>

    <script>
        let currentFileId = null;

        // Show/hide sections
        function showSection(section) {
            const sections = ['hero', 'upload', 'results', 'matches', 'about'];
            sections.forEach(s => {
                document.getElementById(s).classList.add('hidden');
            });
            document.getElementById(section).classList.remove('hidden');
        }

        // File upload handler
        document.getElementById('resumeFile').addEventListener('change', async function(e) {
            const file = e.target.files[0];
            if (!file) return;

            const formData = new FormData();
            formData.append('file', file);

            try {
                const response = await fetch('/upload_resume', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();
                if (result.success) {
                    currentFileId = result.file_id;
                    document.getElementById('uploadArea').innerHTML = `
                        <div class="text-6xl mb-4 text-green-500">✓</div>
                        <p class="text-xl text-green-600 font-semibold">${file.name}</p>
                        <p class="text-gray-500 mt-2">Ready for analysis</p>
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

            // Show loading
            document.getElementById('loadingModal').classList.remove('hidden');
            document.getElementById('analyzeSpinner').classList.remove('hidden');
            document.getElementById('analyzeText').textContent = 'Analyzing...';

            try {
                const formData = new FormData();
                formData.append('file_id', currentFileId);
                formData.append('job_description', jobDescription);

                const response = await fetch('/analyze_resume', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();
                
                // Hide loading
                document.getElementById('loadingModal').classList.add('hidden');
                document.getElementById('analyzeSpinner').classList.add('hidden');
                document.getElementById('analyzeText').textContent = 'Analyze Resume';

                if (result.success) {
                    displayResults(result.analysis);
                    await loadJobMatches();
                    showSection('results');
                } else {
                    alert('Analysis failed: ' + result.message);
                }
            } catch (error) {
                document.getElementById('loadingModal').classList.add('hidden');
                document.getElementById('analyzeSpinner').classList.add('hidden');
                document.getElementById('analyzeText').textContent = 'Analyze Resume';
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
                span.className = 'px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium';
                span.textContent = skill;
                matchedSkillsDiv.appendChild(span);
            });

            // Missing skills
            const missingSkillsDiv = document.getElementById('missingSkills');
            missingSkillsDiv.innerHTML = '';
            analysis.missing_skills.forEach(skill => {
                const span = document.createElement('span');
                span.className = 'px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm font-medium';
                span.textContent = skill;
                missingSkillsDiv.appendChild(span);
            });

            // Feedback
            const feedbackDiv = document.getElementById('feedback');
            feedbackDiv.innerHTML = '';
            analysis.feedback.forEach(item => {
                const div = document.createElement('div');
                div.className = 'p-4 bg-blue-50 rounded-lg border-l-4 border-blue-400';
                div.innerHTML = `<p class="text-blue-800">${item}</p>`;
                feedbackDiv.appendChild(div);
            });

            // Courses
            const coursesDiv = document.getElementById('courses');
            coursesDiv.innerHTML = '';
            analysis.course_recommendations.forEach(course => {
                const div = document.createElement('div');
                div.className = 'bg-gray-50 rounded-lg p-4 hover:shadow-md transition-shadow';
                div.innerHTML = `
                    <h4 class="font-semibold text-gray-900 mb-2">${course.course_title}</h4>
                    <p class="text-sm text-gray-600 mb-2">${course.provider} • ${course.duration}</p>
                    <div class="flex justify-between items-center">
                        <span class="text-sm font-medium text-purple-600">${course.skill}</span>
                        <span class="text-sm font-bold text-green-600">${course.price}</span>
                    </div>
                `;
                coursesDiv.appendChild(div);
            });
        }

        // Load job matches
        async function loadJobMatches() {
            try {
                const response = await fetch(`/match_jobs?file_id=${currentFileId}`);
                const result = await response.json();

                if (result.success) {
                    const jobMatchesDiv = document.getElementById('jobMatches');
                    jobMatchesDiv.innerHTML = '';

                    result.matches.forEach((match, index) => {
                        const div = document.createElement('div');
                        div.className = 'bg-white rounded-xl shadow-lg p-6 card-hover';
                        if (index < 3) div.className += ' border-l-4 border-indigo-500';
                        
                        div.innerHTML = `
                            <div class="flex justify-between items-start mb-4">
                                <div>
                                    <h3 class="text-xl font-semibold text-gray-900">${match.role_title}</h3>
                                    <p class="text-gray-600">${match.company}</p>
                                    <p class="text-sm text-gray-500">${match.salary_range || 'Salary not specified'}</p>
                                </div>
                                <div class="text-right">
                                    <div class="text-2xl font-bold text-indigo-600">${match.fit_score}%</div>
                                    <div class="text-sm text-gray-500">Fit Score</div>
                                </div>
                            </div>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                    <h4 class="text-sm font-semibold text-green-600 mb-2">Matched Skills</h4>
                                    <div class="flex flex-wrap gap-1">
                                        ${match.skills_overlap.map(skill => `<span class="px-2 py-1 bg-green-100 text-green-800 rounded text-xs">${skill}</span>`).join('')}
                                    </div>
                                </div>
                                <div>
                                    <h4 class="text-sm font-semibold text-red-600 mb-2">Missing Skills</h4>
                                    <div class="flex flex-wrap gap-1">
                                        ${match.missing_skills.map(skill => `<span class="px-2 py-1 bg-red-100 text-red-800 rounded text-xs">${skill}</span>`).join('')}
                                    </div>
                                </div>
                            </div>
                            <div class="mt-4 pt-4 border-t border-gray-200">
                                <div class="flex justify-between items-center">
                                    <span class="text-sm text-gray-600">Selection Probability</span>
                                    <span class="text-lg font-semibold text-green-600">${match.selection_probability}%</span>
                                </div>
                            </div>
                        `;
                        jobMatchesDiv.appendChild(div);
                    });
                }
            } catch (error) {
                console.error('Error loading job matches:', error);
            }
        }

        // Initialize
        showSection('hero');
    </script>
</body>
</html>'''
    
    with open(static_dir / "index.html", "w", encoding='utf-8') as f:
        f.write(html_content)
    
    print("✓ Integrated frontend created")

def update_backend():
    """Update backend to serve the integrated frontend"""
    print("Updating backend...")
    
    # Read simple backend
    with open("simple_backend.py", "r") as f:
        content = f.read()
    
    # Add static files serving
    if "StaticFiles" not in content:
        content = content.replace(
            "from fastapi import FastAPI, File, UploadFile, Form, HTTPException",
            "from fastapi import FastAPI, File, UploadFile, Form, HTTPException\nfrom fastapi.staticfiles import StaticFiles"
        )
        
        # Add static mount
        mount_code = '''
# Mount static files for integrated frontend
if Path("static").exists():
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
'''
        
        content = content.replace(
            'if __name__ == "__main__":',
            mount_code + '\nif __name__ == "__main__":'
        )
        
        with open("simple_backend.py", "w") as f:
            f.write(content)
    
    print("✓ Backend updated")

def start_server():
    """Start the integrated server"""
    print("Starting integrated server...")
    print("Server will be available at: http://localhost:9000")
    print("Opening browser in 5 seconds...")
    
    def open_browser():
        time.sleep(5)
        webbrowser.open('http://localhost:9000')
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    try:
        subprocess.run([sys.executable, 'simple_backend.py'])
    except KeyboardInterrupt:
        print("\nServer stopped")

def main():
    """Main function"""
    print_header()
    
    # Create directories
    for d in ['uploads', 'cache', 'logs', 'static']:
        Path(d).mkdir(exist_ok=True)
    
    # Setup
    install_deps()
    create_integrated_frontend()
    update_backend()
    
    print("\n" + "=" * 60)
    print("COMPLETE WEBSITE READY!")
    print("=" * 60)
    print("✓ Frontend: Integrated HTML with modern UI")
    print("✓ Backend: FastAPI with all AI features")
    print("✓ Features: Upload, Analysis, Job Matching, Courses")
    print("✓ Design: Responsive, Professional, Interactive")
    print("=" * 60)
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
