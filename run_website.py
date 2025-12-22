#!/usr/bin/env python3
"""
Simple Website Launcher - No Unicode Issues
"""

import os
import sys
import subprocess
import time
import threading
import webbrowser
from pathlib import Path

def main():
    print("AI Resume Analyzer - Starting Complete Website")
    print("=" * 50)
    
    # Create directories
    for d in ['uploads', 'cache', 'logs', 'static']:
        Path(d).mkdir(exist_ok=True)
    print("Directories created")
    
    # Create integrated HTML frontend
    static_dir = Path("static")
    html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Resume Analyzer</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-50">
    <nav class="bg-white shadow-lg">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex items-center">
                    <h1 class="text-xl font-bold text-indigo-600">AI Resume Analyzer</h1>
                </div>
                <div class="flex items-center space-x-4">
                    <button onclick="showSection('upload')" class="text-gray-700 hover:text-indigo-600 px-3 py-2">Analyze</button>
                    <button onclick="showSection('matches')" class="text-gray-700 hover:text-indigo-600 px-3 py-2">Matches</button>
                </div>
            </div>
        </div>
    </nav>

    <section id="hero" class="bg-gradient-to-r from-indigo-600 to-purple-600 text-white py-20">
        <div class="max-w-4xl mx-auto text-center px-4">
            <h1 class="text-5xl font-bold mb-6">AI Resume Analyzer</h1>
            <p class="text-xl mb-8">Upload your resume and get instant AI feedback</p>
            <button onclick="showSection('upload')" class="bg-white text-indigo-600 px-8 py-4 rounded-lg font-semibold">
                Start Analysis
            </button>
        </div>
    </section>

    <section id="upload" class="py-12 hidden">
        <div class="max-w-4xl mx-auto px-4">
            <div class="bg-white rounded-xl shadow-lg p-8">
                <h2 class="text-3xl font-bold text-center mb-8">Upload Resume</h2>
                
                <div class="mb-8">
                    <div class="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                        <input type="file" id="resumeFile" accept=".pdf,.docx,.doc,.txt" class="hidden">
                        <div id="uploadArea" class="cursor-pointer" onclick="document.getElementById('resumeFile').click()">
                            <div class="text-6xl mb-4">📄</div>
                            <p class="text-xl text-gray-600">Click to upload resume</p>
                            <p class="text-gray-500">PDF, DOCX, DOC, TXT supported</p>
                        </div>
                    </div>
                </div>

                <div class="mb-8">
                    <label class="block text-lg font-semibold mb-3">Job Description</label>
                    <textarea id="jobDescription" rows="8" class="w-full border rounded-lg p-4" placeholder="Paste job description here..."></textarea>
                </div>

                <button onclick="analyzeResume()" class="w-full bg-indigo-600 text-white py-4 rounded-lg font-semibold">
                    Analyze Resume
                </button>
            </div>
        </div>
    </section>

    <section id="results" class="py-12 hidden">
        <div class="max-w-6xl mx-auto px-4">
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div class="bg-white rounded-xl shadow-lg p-6 text-center">
                    <div id="fitScore" class="text-4xl font-bold text-indigo-600 mb-2">--</div>
                    <div class="text-gray-600">Fit Score</div>
                </div>
                <div class="bg-white rounded-xl shadow-lg p-6 text-center">
                    <div id="selectionProb" class="text-4xl font-bold text-green-600 mb-2">--</div>
                    <div class="text-gray-600">Selection Probability</div>
                </div>
                <div class="bg-white rounded-xl shadow-lg p-6 text-center">
                    <div id="skillMatch" class="text-4xl font-bold text-purple-600 mb-2">--</div>
                    <div class="text-gray-600">Skill Match</div>
                </div>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
                <div class="bg-white rounded-xl shadow-lg p-6">
                    <h3 class="text-xl font-semibold text-green-600 mb-4">Matched Skills</h3>
                    <div id="matchedSkills" class="flex flex-wrap gap-2"></div>
                </div>
                <div class="bg-white rounded-xl shadow-lg p-6">
                    <h3 class="text-xl font-semibold text-red-600 mb-4">Missing Skills</h3>
                    <div id="missingSkills" class="flex flex-wrap gap-2"></div>
                </div>
            </div>

            <div class="bg-white rounded-xl shadow-lg p-6">
                <h3 class="text-xl font-semibold text-blue-600 mb-4">AI Feedback</h3>
                <div id="feedback" class="space-y-3"></div>
            </div>
        </div>
    </section>

    <section id="matches" class="py-12 hidden">
        <div class="max-w-6xl mx-auto px-4">
            <h2 class="text-3xl font-bold text-center mb-8">Job Matches</h2>
            <div id="jobMatches" class="space-y-6"></div>
        </div>
    </section>

    <div id="loading" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center hidden">
        <div class="bg-white rounded-lg p-8 text-center">
            <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
            <p>Analyzing resume...</p>
        </div>
    </div>

    <script>
        let currentFileId = null;

        function showSection(section) {
            const sections = ['hero', 'upload', 'results', 'matches'];
            sections.forEach(s => {
                document.getElementById(s).classList.add('hidden');
            });
            document.getElementById(section).classList.remove('hidden');
        }

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
                        <p class="text-gray-500">Ready for analysis</p>
                    `;
                } else {
                    alert('Upload failed: ' + result.message);
                }
            } catch (error) {
                alert('Upload error: ' + error.message);
            }
        });

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

                const response = await fetch('/analyze_resume', {
                    method: 'POST',
                    body: formData
                });

                const result = await response.json();
                document.getElementById('loading').classList.add('hidden');

                if (result.success) {
                    displayResults(result.analysis);
                    await loadJobMatches();
                    showSection('results');
                } else {
                    alert('Analysis failed: ' + result.message);
                }
            } catch (error) {
                document.getElementById('loading').classList.add('hidden');
                alert('Analysis error: ' + error.message);
            }
        }

        function displayResults(analysis) {
            document.getElementById('fitScore').textContent = analysis.fit_score + '%';
            document.getElementById('selectionProb').textContent = analysis.selection_probability + '%';
            document.getElementById('skillMatch').textContent = analysis.skill_match_score + '%';

            const matchedSkillsDiv = document.getElementById('matchedSkills');
            matchedSkillsDiv.innerHTML = '';
            analysis.matched_skills.forEach(skill => {
                const span = document.createElement('span');
                span.className = 'px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm';
                span.textContent = skill;
                matchedSkillsDiv.appendChild(span);
            });

            const missingSkillsDiv = document.getElementById('missingSkills');
            missingSkillsDiv.innerHTML = '';
            analysis.missing_skills.forEach(skill => {
                const span = document.createElement('span');
                span.className = 'px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm';
                span.textContent = skill;
                missingSkillsDiv.appendChild(span);
            });

            const feedbackDiv = document.getElementById('feedback');
            feedbackDiv.innerHTML = '';
            analysis.feedback.forEach(item => {
                const div = document.createElement('div');
                div.className = 'p-4 bg-blue-50 rounded-lg';
                div.textContent = item;
                feedbackDiv.appendChild(div);
            });
        }

        async function loadJobMatches() {
            try {
                const response = await fetch(`/match_jobs?file_id=${currentFileId}`);
                const result = await response.json();

                if (result.success) {
                    const jobMatchesDiv = document.getElementById('jobMatches');
                    jobMatchesDiv.innerHTML = '';

                    result.matches.forEach(match => {
                        const div = document.createElement('div');
                        div.className = 'bg-white rounded-xl shadow-lg p-6';
                        div.innerHTML = `
                            <div class="flex justify-between items-start mb-4">
                                <div>
                                    <h3 class="text-xl font-semibold">${match.role_title}</h3>
                                    <p class="text-gray-600">${match.company}</p>
                                    <p class="text-sm text-gray-500">${match.salary_range || 'Salary not specified'}</p>
                                </div>
                                <div class="text-2xl font-bold text-indigo-600">${match.fit_score}%</div>
                            </div>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div>
                                    <h4 class="font-semibold text-green-600 mb-2">Matched Skills</h4>
                                    <p class="text-sm">${match.skills_overlap.join(', ')}</p>
                                </div>
                                <div>
                                    <h4 class="font-semibold text-red-600 mb-2">Missing Skills</h4>
                                    <p class="text-sm">${match.missing_skills.join(', ')}</p>
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

        showSection('hero');
    </script>
</body>
</html>'''
    
    with open(static_dir / "index.html", "w", encoding='utf-8') as f:
        f.write(html_content)
    print("Frontend created")
    
    # Update backend to serve static files
    with open("simple_backend.py", "r") as f:
        content = f.read()
    
    if "StaticFiles" not in content:
        content = content.replace(
            "from fastapi import FastAPI, File, UploadFile, Form, HTTPException",
            "from fastapi import FastAPI, File, UploadFile, Form, HTTPException\nfrom fastapi.staticfiles import StaticFiles"
        )
        
        mount_code = '''
# Mount static files
if Path("static").exists():
    app.mount("/", StaticFiles(directory="static", html=True), name="static")
'''
        
        content = content.replace(
            'if __name__ == "__main__":',
            mount_code + '\nif __name__ == "__main__":'
        )
        
        with open("simple_backend.py", "w") as f:
            f.write(content)
    
    print("Backend updated")
    print("\nStarting server on http://localhost:9000")
    print("Opening browser in 5 seconds...")
    
    def open_browser():
        time.sleep(5)
        webbrowser.open('http://localhost:9000')
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    try:
        subprocess.run([sys.executable, 'simple_backend.py'])
    except KeyboardInterrupt:
        print("\nServer stopped")

if __name__ == "__main__":
    main()
