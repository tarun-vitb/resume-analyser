import React, { useState } from 'react'
import { motion } from 'framer-motion'
import { useQuery, useMutation } from '@tanstack/react-query'
import axios from 'axios'
import { toast } from 'react-hot-toast'
import { 
  BriefcaseIcon,
  BuildingOfficeIcon,
  CurrencyDollarIcon,
  ChartBarIcon,
  MagnifyingGlassIcon,
  FunnelIcon,
  StarIcon,
  CheckCircleIcon,
  XCircleIcon,
  ArrowPathIcon,
  CloudArrowUpIcon,
  DocumentTextIcon,
  PhoneIcon,
  EnvelopeIcon,
  GlobeAltIcon
} from '@heroicons/react/24/outline'

import API_CONFIG from '../config'
const API_BASE_URL = API_CONFIG.BASE_URL

const Matches = () => {
  const [searchTerm, setSearchTerm] = useState('')
  const [filterBy, setFilterBy] = useState('all')
  const [resumeUploaded, setResumeUploaded] = useState(false)
  const [candidateName, setCandidateName] = useState('')
  const [extractedSkills, setExtractedSkills] = useState([])
  const [showUploader, setShowUploader] = useState(false)

  // Resume upload mutation
  const uploadMutation = useMutation({
    mutationFn: async (file) => {
      const formData = new FormData()
      formData.append('file', file, file.name)
      
      const response = await axios.post(`${API_BASE_URL}${API_CONFIG.ENDPOINTS.UPLOAD}`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
        timeout: 30000
      })
      return response.data
    },
    onSuccess: (data) => {
      setResumeUploaded(true)
      setExtractedSkills(data.skills || [])
      setCandidateName(data.name || 'Unknown')
      setShowUploader(false)
      toast.success(`Resume uploaded! Found ${data.skills?.length || 0} skills`)
      refetch() // Refresh job matches with new resume data
    },
    onError: (error) => {
      console.error('Upload error:', error)
      toast.error(`Upload failed: ${error.response?.data?.detail || error.message}`)
    }
  })

  // Fetch company job matches
  const { data: matchesData, isLoading, error, refetch } = useQuery({
    queryKey: ['companyMatches'],
    queryFn: async () => {
      console.log('Fetching company matches from:', `${API_BASE_URL}${API_CONFIG.ENDPOINTS.COMPANY_MATCHES}`)
      const response = await axios.get(`${API_BASE_URL}${API_CONFIG.ENDPOINTS.COMPANY_MATCHES}`)
      console.log('Company matches response:', response.data)
      return response.data
    },
    retry: 1,
    onError: (error) => {
      console.error('Error fetching company matches:', error)
    }
  })

  const matches = matchesData?.matches || []
  
  console.log('Matches data:', matchesData)
  console.log('Matches array:', matches)
  console.log('Is loading:', isLoading)
  console.log('Error:', error)

  // Filter matches and show best opportunities first
  const filteredMatches = matches
    .filter(match => {
      const matchesSearch = match.role_title.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           match.company.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           match.industry.toLowerCase().includes(searchTerm.toLowerCase())
      
      const matchesFilter = filterBy === 'all' || 
                           (filterBy === 'remote' && match.remote_friendly) ||
                           (filterBy === 'high_match' && match.fit_score >= 70) ||
                           (filterBy === 'tech_giants' && ['Google', 'Microsoft', 'Amazon', 'Meta', 'Netflix'].includes(match.company))
      
      return matchesSearch && matchesFilter
    })
    // Always sort by selection probability first (best interview chances), then by fit score
    .sort((a, b) => {
      if (b.selection_probability !== a.selection_probability) {
        return b.selection_probability - a.selection_probability
      }
      return b.fit_score - a.fit_score
    })

  const getScoreColor = (score) => {
    if (score >= 80) return 'text-green-600 bg-green-100'
    if (score >= 60) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  const getScoreBarColor = (score) => {
    if (score >= 80) return 'bg-green-500'
    if (score >= 60) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  if (error && error.response?.status === 400) {
    return (
      <div className="min-h-screen py-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
          >
            <BriefcaseIcon className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h1 className="text-3xl font-bold text-gray-900 mb-4">Job Matching</h1>
            <p className="text-gray-600 mb-8">
              Please upload and analyze your resume first to see personalized job matches.
            </p>
            <a
              href="/analyze"
              className="inline-flex items-center space-x-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-3 rounded-xl font-medium hover:from-indigo-700 hover:to-purple-700 transition-all duration-200"
            >
              <span>Analyze Resume</span>
            </a>
          </motion.div>
        </div>
      </div>
    )
  }

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
            Best <span className="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">Interview Opportunities</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Discover jobs where you have the highest chances of interview success based on your skills and profile.
          </p>
        </motion.div>

        {/* Resume Upload Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.1 }}
          className="bg-white rounded-2xl shadow-lg p-6 mb-8 border border-gray-100"
        >
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-3">
              <DocumentTextIcon className="w-6 h-6 text-indigo-600" />
              <div>
                <h3 className="text-lg font-semibold text-gray-900">Resume Analysis</h3>
                <p className="text-sm text-gray-600">Upload your resume to get personalized job matches</p>
              </div>
            </div>
            
            {!showUploader && !resumeUploaded && (
              <button
                onClick={() => setShowUploader(true)}
                className="flex items-center space-x-2 bg-indigo-600 text-white px-4 py-2 rounded-lg hover:bg-indigo-700 transition-colors"
              >
                <CloudArrowUpIcon className="w-4 h-4" />
                <span>Upload Resume</span>
              </button>
            )}
          </div>

          {/* Upload Area */}
          {showUploader && (
            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center">
              <input
                type="file"
                accept=".pdf,.docx,.doc"
                onChange={(e) => {
                  const file = e.target.files[0]
                  if (file) {
                    uploadMutation.mutate(file)
                  }
                }}
                className="hidden"
                id="resume-upload"
              />
              <label htmlFor="resume-upload" className="cursor-pointer">
                <CloudArrowUpIcon className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <p className="text-lg font-medium text-gray-900 mb-2">
                  {uploadMutation.isLoading ? 'Analyzing Resume...' : 'Click to upload your resume'}
                </p>
                <p className="text-sm text-gray-600">
                  Supports PDF, DOCX files (Max 10MB)
                </p>
              </label>
              
              {uploadMutation.isLoading && (
                <div className="mt-4">
                  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-indigo-600 mx-auto"></div>
                </div>
              )}
            </div>
          )}

          {/* Resume Info */}
          {resumeUploaded && (
            <div className="bg-green-50 border border-green-200 rounded-lg p-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <CheckCircleIcon className="w-6 h-6 text-green-600" />
                  <div>
                    <p className="font-medium text-green-900">Resume Analyzed Successfully</p>
                    <p className="text-sm text-green-700">
                      Candidate: {candidateName} • Skills Found: {extractedSkills.length}
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => {
                    setShowUploader(true)
                    setResumeUploaded(false)
                  }}
                  className="text-sm text-green-700 hover:text-green-900 font-medium"
                >
                  Upload New Resume
                </button>
              </div>
              
              {/* Skills Display */}
              {extractedSkills.length > 0 && (
                <div className="mt-3">
                  <p className="text-sm font-medium text-green-800 mb-2">Extracted Skills:</p>
                  <div className="flex flex-wrap gap-2">
                    {extractedSkills.slice(0, 10).map((skill, index) => (
                      <span
                        key={index}
                        className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs font-medium"
                      >
                        {skill}
                      </span>
                    ))}
                    {extractedSkills.length > 10 && (
                      <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">
                        +{extractedSkills.length - 10} more
                      </span>
                    )}
                  </div>
                </div>
              )}
            </div>
          )}
        </motion.div>

        {/* Controls */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
          className="bg-white rounded-2xl shadow-lg p-6 mb-8 border border-gray-100"
        >
          <div className="flex flex-col md:flex-row gap-4 items-center justify-between">
            {/* Search */}
            <div className="relative flex-1 max-w-md">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search jobs or companies..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              />
            </div>

            {/* Filter */}
            <div className="flex items-center space-x-2">
              <FunnelIcon className="w-5 h-5 text-gray-400" />
              <select
                value={filterBy}
                onChange={(e) => setFilterBy(e.target.value)}
                className="border border-gray-300 rounded-lg px-3 py-2 focus:ring-2 focus:ring-indigo-500 focus:border-transparent"
              >
                <option value="all">All Jobs</option>
                <option value="high_match">High Match (70%+)</option>
                <option value="remote">Remote Friendly</option>
                <option value="tech_giants">Tech Giants</option>
              </select>
            </div>

            {/* Info */}
            <div className="flex items-center space-x-2 text-sm text-gray-600">
              <ChartBarIcon className="w-5 h-5 text-indigo-500" />
              <span className="font-medium">Sorted by Interview Success Probability</span>
            </div>

            {/* Stats */}
            <div className="text-sm text-gray-600">
              {filteredMatches.length} of {matches.length} jobs
            </div>
            
            {/* Refresh Button */}
            <button
              onClick={() => refetch()}
              disabled={isLoading}
              className="flex items-center space-x-1 px-3 py-2 text-sm text-gray-600 hover:text-gray-800 border border-gray-300 rounded-lg hover:bg-gray-50 transition-colors disabled:opacity-50"
            >
              <ArrowPathIcon className={`w-4 h-4 ${isLoading ? 'animate-spin' : ''}`} />
              <span>Refresh</span>
            </button>
            
            {/* Debug Info */}
            {process.env.NODE_ENV === 'development' && (
              <div className="text-xs text-gray-500">
                Loading: {isLoading ? 'Yes' : 'No'} | 
                Error: {error ? 'Yes' : 'No'} | 
                Data: {matchesData ? 'Yes' : 'No'}
              </div>
            )}
          </div>
        </motion.div>

        {/* Loading State */}
        {isLoading && (
          <div className="text-center py-12">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
            <p className="text-gray-600">Finding your perfect job matches...</p>
          </div>
        )}

        {/* Error State */}
        {error && (
          <div className="text-center py-12">
            <XCircleIcon className="w-12 h-12 text-red-500 mx-auto mb-4" />
            <p className="text-red-600 mb-2">Failed to load job matches. Please try again.</p>
            <p className="text-sm text-gray-500">Error: {error.message}</p>
            {error.response?.status === 400 && (
              <p className="text-sm text-blue-600 mt-2">
                Please upload and analyze a resume first in the Analyze section.
              </p>
            )}
          </div>
        )}

        {/* Job Matches Grid */}
        {filteredMatches.length > 0 && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {filteredMatches.map((match, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className={`bg-white rounded-2xl shadow-lg p-6 border hover:shadow-xl transition-all duration-300 ${
                  index < 3 ? 'border-indigo-200 ring-2 ring-indigo-100' : 'border-gray-100'
                }`}
              >
                {/* Top Badge for Top 3 */}
                {index < 3 && (
                  <div className="flex justify-between items-center mb-4">
                    <div className="flex items-center space-x-2">
                      <StarIcon className="w-5 h-5 text-yellow-500 fill-current" />
                      <span className="text-sm font-medium text-indigo-600">
                        #{index + 1} Best Interview Chance
                      </span>
                    </div>
                    <div className="text-xs bg-green-100 text-green-800 px-2 py-1 rounded-full font-medium">
                      High Success Rate
                    </div>
                  </div>
                )}

                {/* Job Header */}
                <div className="mb-4">
                  <h3 className="text-xl font-semibold text-gray-900 mb-1">
                    {match.role_title}
                  </h3>
                  <div className="flex items-center space-x-2 text-gray-600 mb-1">
                    <BuildingOfficeIcon className="w-4 h-4" />
                    <span className="font-medium">{match.company}</span>
                    <span className="text-sm">({match.company_size})</span>
                  </div>
                  <div className="flex items-center space-x-4 text-sm text-gray-600">
                    <span>📍 {match.location}</span>
                    <span>🏢 {match.industry}</span>
                    {match.remote_friendly && <span>🏠 Remote</span>}
                  </div>
                  <div className="flex items-center space-x-2 text-gray-600 mt-2">
                    <CurrencyDollarIcon className="w-4 h-4" />
                    <span className="font-medium">{match.salary_range}</span>
                    <span className="text-sm">• {match.experience_level}</span>
                  </div>
                </div>

                {/* Interview Success Metrics */}
                <div className="mb-4">
                  {/* Primary metric - Selection Probability */}
                  <div className="mb-3">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-sm font-medium text-gray-700">Interview Success Probability</span>
                      <span className={`text-lg font-bold px-3 py-1 rounded-full ${getScoreColor(match.selection_probability)}`}>
                        {match.selection_probability}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-3">
                      <div
                        className={`h-3 rounded-full ${getScoreBarColor(match.selection_probability)} transition-all duration-500`}
                        style={{ width: `${match.selection_probability}%` }}
                      ></div>
                    </div>
                  </div>
                  
                  {/* Secondary metric - Fit Score */}
                  <div>
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-xs text-gray-600">Skills Match Score</span>
                      <span className={`text-xs font-medium px-2 py-1 rounded-full ${getScoreColor(match.fit_score)}`}>
                        {match.fit_score}%
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-1.5">
                      <div
                        className={`h-1.5 rounded-full ${getScoreBarColor(match.fit_score)}`}
                        style={{ width: `${match.fit_score}%` }}
                      ></div>
                    </div>
                  </div>
                </div>

                {/* Skills */}
                <div className="mb-4">
                  {/* Matched Skills */}
                  {match.skills_overlap?.length > 0 && (
                    <div className="mb-3">
                      <h4 className="text-sm font-medium text-green-600 mb-2 flex items-center">
                        <CheckCircleIcon className="w-4 h-4 mr-1" />
                        Matched Skills ({match.skills_overlap.length})
                      </h4>
                      <div className="flex flex-wrap gap-1">
                        {match.skills_overlap.slice(0, 4).map((skill, skillIndex) => (
                          <span
                            key={skillIndex}
                            className="px-2 py-1 bg-green-100 text-green-800 rounded text-xs font-medium"
                          >
                            {skill}
                          </span>
                        ))}
                        {match.skills_overlap.length > 4 && (
                          <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">
                            +{match.skills_overlap.length - 4} more
                          </span>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Missing Skills */}
                  {match.missing_skills?.length > 0 && (
                    <div>
                      <h4 className="text-sm font-medium text-red-600 mb-2 flex items-center">
                        <XCircleIcon className="w-4 h-4 mr-1" />
                        Missing Skills ({match.missing_skills.length})
                      </h4>
                      <div className="flex flex-wrap gap-1">
                        {match.missing_skills.slice(0, 3).map((skill, skillIndex) => (
                          <span
                            key={skillIndex}
                            className="px-2 py-1 bg-red-100 text-red-800 rounded text-xs font-medium"
                          >
                            {skill}
                          </span>
                        ))}
                        {match.missing_skills.length > 3 && (
                          <span className="px-2 py-1 bg-gray-100 text-gray-600 rounded text-xs">
                            +{match.missing_skills.length - 3} more
                          </span>
                        )}
                      </div>
                    </div>
                  )}
                </div>

                {/* Job Description */}
                <div className="mb-4 p-3 bg-gray-50 rounded-lg">
                  <p className="text-sm text-gray-700 leading-relaxed">
                    {match.description}
                  </p>
                </div>

                {/* Skills Match Summary */}
                <div className="mb-4 grid grid-cols-2 gap-3 text-xs">
                  <div className="text-center p-2 bg-green-50 rounded">
                    <div className="font-medium text-green-800">Required Skills</div>
                    <div className="text-green-600">{match.required_skills_match}</div>
                  </div>
                  <div className="text-center p-2 bg-purple-50 rounded">
                    <div className="font-medium text-purple-800">Preferred Skills</div>
                    <div className="text-purple-600">{match.preferred_skills_match}</div>
                  </div>
                </div>

                {/* Company Contact Information */}
                {match.contact_info && (
                  <div className="border-t pt-4">
                    <h5 className="text-sm font-medium text-gray-900 mb-3">How to Apply</h5>
                    <div className="grid grid-cols-1 gap-2 text-sm">
                      {match.contact_info.careers_page && (
                        <a
                          href={match.contact_info.careers_page}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center space-x-2 text-indigo-600 hover:text-indigo-800 transition-colors"
                        >
                          <GlobeAltIcon className="w-4 h-4" />
                          <span>Careers Page</span>
                        </a>
                      )}
                      {match.contact_info.email && (
                        <a
                          href={`mailto:${match.contact_info.email}`}
                          className="flex items-center space-x-2 text-gray-600 hover:text-gray-800 transition-colors"
                        >
                          <EnvelopeIcon className="w-4 h-4" />
                          <span>{match.contact_info.email}</span>
                        </a>
                      )}
                      {match.contact_info.phone && (
                        <a
                          href={`tel:${match.contact_info.phone}`}
                          className="flex items-center space-x-2 text-gray-600 hover:text-gray-800 transition-colors"
                        >
                          <PhoneIcon className="w-4 h-4" />
                          <span>{match.contact_info.phone}</span>
                        </a>
                      )}
                      {match.contact_info.linkedin && (
                        <a
                          href={match.contact_info.linkedin}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="flex items-center space-x-2 text-blue-600 hover:text-blue-800 transition-colors"
                        >
                          <BuildingOfficeIcon className="w-4 h-4" />
                          <span>LinkedIn Company Page</span>
                        </a>
                      )}
                    </div>
                  </div>
                )}
              </motion.div>
            ))}
          </div>
        )}

        {/* No Results */}
        {filteredMatches.length === 0 && matches.length > 0 && (
          <div className="text-center py-12">
            <MagnifyingGlassIcon className="w-12 h-12 text-gray-300 mx-auto mb-4" />
            <h3 className="text-xl font-medium text-gray-900 mb-2">No matches found</h3>
            <p className="text-gray-600">
              Try adjusting your search terms or filters.
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

export default Matches
