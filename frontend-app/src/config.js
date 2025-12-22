// Frontend configuration for connecting to backend
export const API_CONFIG = {
  BASE_URL: 'http://localhost:9002/api/v1',
  ENDPOINTS: {
    HEALTH: '/health',
    UPLOAD: '/upload-resume',
    ANALYZE: '/analyze-resume',
    MATCHES: '/match-multiple-jobs',
    COMPANY_MATCHES: '/company-matches',
    JOB_RECOMMENDATIONS: '/job-recommendations',
    DEMO: '/demo_data'
  },
  TIMEOUT: 30000, // 30 seconds
  MAX_FILE_SIZE: 10 * 1024 * 1024, // 10MB
  ALLOWED_FILE_TYPES: ['.pdf', '.docx', '.doc', '.txt']
}

export default API_CONFIG
