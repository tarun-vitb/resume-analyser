import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { useDropzone } from 'react-dropzone'
import { useMutation } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import axios from 'axios'
import { 
  DocumentArrowUpIcon,
  SparklesIcon,
  ChartBarIcon,
  AcademicCapIcon,
  LightBulbIcon,
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon,
  BriefcaseIcon,
  LinkIcon
} from '@heroicons/react/24/outline'
import { PieChart, Pie, Cell, ResponsiveContainer, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'

import API_CONFIG from '../config'
const API_BASE_URL = API_CONFIG.BASE_URL

const Analyze = () => {
  const [uploadedFile, setUploadedFile] = useState(null)
  const [resumeUploaded, setResumeUploaded] = useState(false)
  const [extractedSkills, setExtractedSkills] = useState([])
  const [candidateName, setCandidateName] = useState('')
  const [jobDescription, setJobDescription] = useState('')
  const [analysisResult, setAnalysisResult] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)

  // File upload mutation
  const uploadMutation = useMutation({
    mutationFn: async (file) => {
      console.log('Uploading file:', file.name, 'Size:', file.size, 'Type:', file.type)
      
      // Validate file
      if (!file) {
        throw new Error('No file selected')
      }
      if (file.size === 0) {
        throw new Error('File is empty')
      }
      if (file.size > 10 * 1024 * 1024) { // 10MB limit
        throw new Error('File is too large (max 10MB)')
      }
      
      const formData = new FormData()
      formData.append('file', file)
      
      console.log('Uploading to:', `${API_BASE_URL}${API_CONFIG.ENDPOINTS.UPLOAD}`)
      
      try {
        const response = await axios.post(
          `${API_BASE_URL}${API_CONFIG.ENDPOINTS.UPLOAD}`, 
          formData, 
          {
            headers: { 
              'Content-Type': 'multipart/form-data',
              'Accept': 'application/json'
            },
            timeout: 60000, // 60 seconds timeout
            withCredentials: true
          }
        )
        console.log('Upload response:', response.data)
        return response.data
      } catch (error) {
        console.error('Upload error details:', {
          message: error.message,
          response: error.response?.data,
          status: error.response?.status,
          headers: error.response?.headers
        })
        throw error
      }
    },
    onSuccess: (data) => {
      setResumeUploaded(true)
      setExtractedSkills(data.skills || [])
      setCandidateName(data.name || 'Unknown')
      toast.success(`Resume uploaded! Found ${data.skills?.length || 0} skills for ${data.name}`)
    },
    onError: (error) => {
      console.error('Upload error:', error)
      const errorMessage = error.response?.data?.detail || error.message || 'Upload failed'
      toast.error(`Upload failed: ${errorMessage}`)
    }
  })

  // Analysis mutation
  const analysisMutation = useMutation({
    mutationFn: async (jobDescription) => {
      if (!uploadedFile) {
        throw new Error('Please upload a resume first')
      }
      
      const formData = new FormData()
      formData.append('file', uploadedFile)
      formData.append('job_description', jobDescription)
      
      console.log('Analyzing with job description:', jobDescription.substring(0, 50) + '...')
      
      try {
        const response = await axios.post(
          `${API_BASE_URL}${API_CONFIG.ENDPOINTS.ANALYZE}`,
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data',
              'Accept': 'application/json'
            },
            timeout: 120000, // 2 minutes timeout for analysis
            withCredentials: true
          }
        )
        return response.data
      } catch (error) {
        console.error('Analysis error:', {
          message: error.message,
          response: error.response?.data,
          status: error.response?.status
        })
        throw error
      }
    },
    onSuccess: (data) => {
      console.log('Analysis successful:', data)
      setAnalysisResult(data)
      setIsAnalyzing(false)
      toast.success('Analysis completed successfully!')
    },
    onError: (error) => {
      console.error('Analysis failed:', error)
      setIsAnalyzing(false)
      const errorMessage = error.response?.data?.detail || 
                         error.response?.data?.message || 
                         error.message || 
                         'Analysis failed. Please try again.'
      toast.error(errorMessage)
    }
  })

  // Dropzone configuration
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    accept: {
      'application/pdf': ['.pdf'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'],
      'application/msword': ['.doc']
    },
    maxFiles: 1,
    onDrop: (acceptedFiles) => {
      if (acceptedFiles.length > 0) {
        const file = acceptedFiles[0]
        setUploadedFile(file)
        uploadMutation.mutate(file)
      }
    }
  })

  const handleAnalyze = () => {
    if (!resumeUploaded || !jobDescription.trim()) {
      toast.error('Please upload a resume and enter a job description')
      return
    }
    
    setIsAnalyzing(true)
    analysisMutation.mutate(jobDescription)
  }

  // Chart data
  const pieData = analysisResult ? [
    { name: 'Match', value: analysisResult.fit_score, color: '#10b981' },
    { name: 'Gap', value: 100 - analysisResult.fit_score, color: '#e5e7eb' }
  ] : []

  const skillsData = analysisResult ? [
    { name: 'Present Skills', value: analysisResult.skills?.length || 0, color: '#10b981' },
    { name: 'Missing Skills', value: analysisResult.missing_skills?.length || 0, color: '#ef4444' }
  ] : []

  return (
    <div className="min-h-screen py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            AI Resume <span className="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">Analyzer</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Upload your resume and job description to get instant AI-powered feedback, 
            skill gap analysis, and personalized recommendations.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Left Column - Upload & Input */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="space-y-6"
          >
            {/* File Upload */}
            <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4 flex items-center">
                <DocumentArrowUpIcon className="w-6 h-6 mr-2 text-indigo-600" />
                Upload Resume
              </h2>
              
              <div
                {...getRootProps()}
                className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-300 ${
                  isDragActive 
                    ? 'border-indigo-500 bg-indigo-50' 
                    : uploadedFile 
                      ? 'border-green-500 bg-green-50' 
                      : 'border-gray-300 hover:border-indigo-400 hover:bg-gray-50'
                }`}
              >
                <input {...getInputProps()} />
                
                {uploadMutation.isPending ? (
                  <div className="flex flex-col items-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mb-4"></div>
                    <p className="text-gray-600">Uploading...</p>
                  </div>
                ) : uploadedFile ? (
                  <div className="flex flex-col items-center">
                    <CheckCircleIcon className="w-12 h-12 text-green-500 mb-4" />
                    <p className="text-green-600 font-medium">{uploadedFile.name}</p>
                    {candidateName && (
                      <p className="text-gray-700 font-semibold mt-1">Candidate: {candidateName}</p>
                    )}
                    <p className="text-gray-500 text-sm mt-1">Ready for analysis</p>
                    <p className="text-sm text-blue-600 mt-2">Skills found: {extractedSkills.length}</p>
                    {extractedSkills.length > 0 && (
                      <div className="mt-2 flex flex-wrap gap-1 max-w-md">
                        {extractedSkills.slice(0, 5).map((skill, index) => (
                          <span key={index} className="px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                            {skill}
                          </span>
                        ))}
                        {extractedSkills.length > 5 && (
                          <span className="px-2 py-1 bg-gray-100 text-gray-600 text-xs rounded-full">
                            +{extractedSkills.length - 5} more
                          </span>
                        )}
                      </div>
                    )}
                  </div>
                ) : (
                  <div className="flex flex-col items-center">
                    <DocumentArrowUpIcon className="w-12 h-12 text-gray-400 mb-4" />
                    <p className="text-gray-600 font-medium mb-2">
                      {isDragActive ? 'Drop your resume here' : 'Drag & drop your resume'}
                    </p>
                    <p className="text-gray-500 text-sm">
                      Supports PDF, DOCX, DOC files
                    </p>
                  </div>
                )}
              </div>
            </div>

            {/* Job Description Input */}
            <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
              <h2 className="text-2xl font-semibold text-gray-900 mb-4 flex items-center">
                <SparklesIcon className="w-6 h-6 mr-2 text-indigo-600" />
                Job Description
              </h2>
              
              <textarea
                value={jobDescription}
                onChange={(e) => setJobDescription(e.target.value)}
                placeholder="Paste the job description here..."
                className="w-full h-40 p-4 border border-gray-300 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent resize-none"
              />
              
              <div className="mt-4 flex justify-between items-center">
                <span className="text-sm text-gray-500">
                  {jobDescription.length} characters
                </span>
                
                <button
                  onClick={handleAnalyze}
                  disabled={!resumeUploaded || !jobDescription.trim() || isAnalyzing}
                  className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-xl font-medium hover:from-indigo-700 hover:to-purple-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center space-x-2"
                >
                  {isAnalyzing ? (
                    <>
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white"></div>
                      <span>Analyzing...</span>
                    </>
                  ) : (
                    <>
                      <SparklesIcon className="w-4 h-4" />
                      <span>Analyze Resume</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          </motion.div>

          {/* Right Column - Results */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.4 }}
            className="space-y-6"
          >
            {analysisResult ? (
              <>
                {/* Fit Score */}
                <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
                  <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                    <ChartBarIcon className="w-5 h-5 mr-2 text-indigo-600" />
                    Overall Fit Score
                  </h3>
                  
                  <div className="flex items-center justify-center">
                    <div className="relative w-48 h-48">
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie
                            data={pieData}
                            cx="50%"
                            cy="50%"
                            innerRadius={60}
                            outerRadius={90}
                            startAngle={90}
                            endAngle={450}
                            dataKey="value"
                          >
                            {pieData.map((entry, index) => (
                              <Cell key={`cell-${index}`} fill={entry.color} />
                            ))}
                          </Pie>
                        </PieChart>
                      </ResponsiveContainer>
                      <div className="absolute inset-0 flex items-center justify-center">
                        <div className="text-center">
                          <div className="text-3xl font-bold text-gray-900">
                            {analysisResult.fit_score}%
                          </div>
                          <div className="text-sm text-gray-500">Match</div>
                        </div>
                      </div>
                    </div>
                  </div>
                  
                  <div className="mt-4 grid grid-cols-2 gap-4 text-center">
                    <div>
                      <div className="text-2xl font-bold text-green-600">
                        {analysisResult.shortlist_probability}%
                      </div>
                      <div className="text-sm text-gray-500">Shortlist Probability</div>
                    </div>
                    <div>
                      <div className="text-2xl font-bold text-blue-600">
                        {analysisResult.skills?.length || 0}
                      </div>
                      <div className="text-sm text-gray-500">Total Skills</div>
                    </div>
                  </div>
                </div>

                {/* Skills Analysis */}
                <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
                  <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                    <AcademicCapIcon className="w-5 h-5 mr-2 text-indigo-600" />
                    Skills Analysis
                  </h3>
                  
                  <div className="mb-4">
                    <ResponsiveContainer width="100%" height={200}>
                      <BarChart data={skillsData}>
                        <CartesianGrid strokeDasharray="3 3" />
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip />
                        <Bar dataKey="value" fill="#8884d8" />
                      </BarChart>
                    </ResponsiveContainer>
                  </div>
                  
                  <div className="space-y-4">
                    {/* Present Skills */}
                    <div>
                      <h4 className="font-medium text-green-600 mb-2 flex items-center">
                        <CheckCircleIcon className="w-4 h-4 mr-1" />
                        Present Skills ({analysisResult.skills?.length || 0})
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {analysisResult.skills?.map((skill, index) => (
                          <span
                            key={index}
                            className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium"
                          >
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                    
                    {/* Missing Skills */}
                    <div>
                      <h4 className="font-medium text-red-600 mb-2 flex items-center">
                        <XCircleIcon className="w-4 h-4 mr-1" />
                        Missing Skills ({analysisResult.missing_skills?.length || 0})
                      </h4>
                      <div className="flex flex-wrap gap-2">
                        {analysisResult.missing_skills?.map((skill, index) => (
                          <span
                            key={index}
                            className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm font-medium"
                          >
                            {skill}
                          </span>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Feedback */}
                <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
                  <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                    <LightBulbIcon className="w-5 h-5 mr-2 text-indigo-600" />
                    AI Feedback
                  </h3>
                  
                  <div className="flex items-start space-x-3 p-4 bg-blue-50 rounded-lg">
                    <LightBulbIcon className="w-5 h-5 text-blue-600 mt-0.5 flex-shrink-0" />
                    <p className="text-gray-700">{analysisResult.feedback}</p>
                  </div>
                </div>

                {/* Course Recommendations */}
                {analysisResult.recommended_courses?.length > 0 && (
                  <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
                    <h3 className="text-xl font-semibold text-gray-900 mb-4 flex items-center">
                      <AcademicCapIcon className="w-5 h-5 mr-2 text-indigo-600" />
                      Recommended Courses
                    </h3>
                    
                    <div className="space-y-4">
                      {analysisResult.recommended_courses.map((course, index) => (
                        <div key={index} className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow">
                          <div className="flex justify-between items-start mb-2">
                            <h4 className="font-medium text-gray-900">{course.name}</h4>
                            <a 
                              href={course.link} 
                              target="_blank" 
                              rel="noopener noreferrer"
                              className="text-indigo-600 hover:text-indigo-800 flex items-center"
                            >
                              <LinkIcon className="w-4 h-4 mr-1" />
                              View Course
                            </a>
                          </div>
                          <p className="text-sm text-gray-600">
                            Learn the skills you need to improve your resume match score
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Eligible Jobs */}
                {analysisResult.eligible_jobs?.length > 0 && (
                  <div className="bg-white rounded-2xl shadow-lg p-6 border border-gray-100">
                    <h3 className="text-xl font-semibold text-gray-900 mb-6 flex items-center">
                      <BriefcaseIcon className="w-5 h-5 mr-2 text-indigo-600" />
                      Recommended Job Roles
                    </h3>
                    
                    <div className="grid gap-6 md:grid-cols-2">
                      {analysisResult.eligible_jobs.map((job, index) => (
                        <motion.div
                          key={index}
                          initial={{ opacity: 0, y: 20 }}
                          animate={{ opacity: 1, y: 0 }}
                          transition={{ delay: index * 0.1 }}
                          className="border border-gray-200 rounded-xl p-5 hover:shadow-md transition-shadow"
                        >
                          {/* Job Header */}
                          <div className="flex justify-between items-start mb-3">
                            <h4 className="text-lg font-semibold text-gray-900">{job.title}</h4>
                            <span className={`px-3 py-1 rounded-full text-sm font-medium ${
                              job.fit_score >= 80 ? 'bg-green-100 text-green-800' :
                              job.fit_score >= 60 ? 'bg-yellow-100 text-yellow-800' :
                              'bg-red-100 text-red-800'
                            }`}>
                              {job.fit_score}% Match
                            </span>
                          </div>
                          
                          {/* Job Details */}
                          <div className="space-y-3">
                            <p className="text-sm text-gray-600 leading-relaxed">
                              {job.description}
                            </p>
                            
                            {/* Salary and Experience */}
                            <div className="flex justify-between text-sm">
                              <span className="text-gray-500">
                                💰 {job.salary_range}
                              </span>
                              <span className="text-gray-500">
                                📈 {job.experience_level}
                              </span>
                            </div>
                            
                            {/* Skills Coverage */}
                            <div className="grid grid-cols-2 gap-3 text-xs">
                              <div>
                                <span className="text-gray-500">Required Skills:</span>
                                <span className="ml-1 font-medium text-indigo-600">
                                  {job.skills_coverage?.required || '0/0'}
                                </span>
                              </div>
                              <div>
                                <span className="text-gray-500">Preferred Skills:</span>
                                <span className="ml-1 font-medium text-purple-600">
                                  {job.skills_coverage?.preferred || '0/0'}
                                </span>
                              </div>
                            </div>
                            
                            {/* Matching Skills */}
                            {job.matching_skills && (
                              <div className="space-y-2">
                                {job.matching_skills.required?.length > 0 && (
                                  <div>
                                    <p className="text-xs font-medium text-gray-700 mb-1">Your Matching Required Skills:</p>
                                    <div className="flex flex-wrap gap-1">
                                      {job.matching_skills.required.map((skill, skillIndex) => (
                                        <span
                                          key={skillIndex}
                                          className="px-2 py-1 bg-indigo-100 text-indigo-700 rounded text-xs font-medium"
                                        >
                                          {skill}
                                        </span>
                                      ))}
                                    </div>
                                  </div>
                                )}
                                
                                {job.matching_skills.preferred?.length > 0 && (
                                  <div>
                                    <p className="text-xs font-medium text-gray-700 mb-1">Your Matching Preferred Skills:</p>
                                    <div className="flex flex-wrap gap-1">
                                      {job.matching_skills.preferred.map((skill, skillIndex) => (
                                        <span
                                          key={skillIndex}
                                          className="px-2 py-1 bg-purple-100 text-purple-700 rounded text-xs font-medium"
                                        >
                                          {skill}
                                        </span>
                                      ))}
                                    </div>
                                  </div>
                                )}
                              </div>
                            )}
                          </div>
                        </motion.div>
                      ))}
                    </div>
                  </div>
                )}
              </>
            ) : (
              <div className="bg-white rounded-2xl shadow-lg p-12 border border-gray-100 text-center">
                <SparklesIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
                <h3 className="text-xl font-medium text-gray-900 mb-2">Ready for Analysis</h3>
                <p className="text-gray-600">
                  Upload your resume and enter a job description to get started with AI-powered analysis.
                </p>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  )
}

export default Analyze
