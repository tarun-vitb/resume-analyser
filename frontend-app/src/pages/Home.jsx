import React from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { 
  SparklesIcon, 
  DocumentTextIcon, 
  ChartBarIcon,
  RocketLaunchIcon,
  CheckCircleIcon,
  ArrowRightIcon,
  CpuChipIcon,
  LightBulbIcon,
  TrophyIcon
} from '@heroicons/react/24/outline'

const Home = () => {
  const features = [
    {
      icon: DocumentTextIcon,
      title: 'Smart Resume Analysis',
      description: 'AI-powered analysis of your resume with instant feedback on content, structure, and ATS compatibility.',
      gradient: 'from-blue-500 to-cyan-500'
    },
    {
      icon: CpuChipIcon,
      title: 'ML-Powered Matching',
      description: 'Advanced machine learning algorithms calculate your fit score and selection probability for any job.',
      gradient: 'from-purple-500 to-pink-500'
    },
    {
      icon: ChartBarIcon,
      title: 'Skill Gap Analysis',
      description: 'Identify missing skills and get personalized recommendations to boost your career prospects.',
      gradient: 'from-green-500 to-emerald-500'
    },
    {
      icon: LightBulbIcon,
      title: 'Course Recommendations',
      description: 'Get curated course suggestions from top platforms to fill your skill gaps and advance your career.',
      gradient: 'from-yellow-500 to-orange-500'
    },
    {
      icon: RocketLaunchIcon,
      title: 'Job Matching',
      description: 'Find the perfect job matches based on your skills, experience, and career aspirations.',
      gradient: 'from-indigo-500 to-purple-500'
    },
    {
      icon: TrophyIcon,
      title: 'Career Insights',
      description: 'Receive data-driven insights and actionable feedback to accelerate your career growth.',
      gradient: 'from-red-500 to-pink-500'
    }
  ]

  const stats = [
    { label: 'Resumes Analyzed', value: '50,000+', icon: DocumentTextIcon },
    { label: 'Success Rate', value: '94%', icon: TrophyIcon },
    { label: 'Job Matches', value: '1M+', icon: RocketLaunchIcon },
    { label: 'Skills Identified', value: '500+', icon: CpuChipIcon }
  ]

  const benefits = [
    'Increase interview callbacks by up to 40%',
    'Save 10+ hours of manual resume optimization',
    'Get personalized career development roadmap',
    'Access 1000+ relevant course recommendations',
    'Real-time ATS compatibility scoring',
    'AI-powered job matching and prioritization'
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        {/* Animated Background */}
        <div className="absolute inset-0 bg-gradient-to-br from-indigo-600 via-purple-600 to-blue-600 opacity-90">
          <div className="absolute inset-0 bg-dots-white/10"></div>
        </div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-24 lg:py-32">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
            >
              <div className="flex justify-center mb-8">
                <div className="relative">
                  <div className="absolute inset-0 bg-white/20 rounded-full blur-xl animate-pulse-glow"></div>
                  <SparklesIcon className="relative w-16 h-16 text-white" />
                </div>
              </div>
              
              <h1 className="text-4xl md:text-6xl lg:text-7xl font-bold text-white mb-6 leading-tight">
                AI Resume Analyzer
                <span className="block text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-400">
                  Level Up Your Career
                </span>
              </h1>
              
              <p className="text-xl md:text-2xl text-blue-100 mb-8 max-w-3xl mx-auto leading-relaxed">
                Upload your resume and get data-driven feedback in seconds. 
                Powered by advanced AI to maximize your job search success.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16"
            >
              <Link
                to="/analyze"
                className="group relative bg-white text-indigo-600 px-8 py-4 rounded-xl font-semibold text-lg hover:bg-blue-50 transition-all duration-300 flex items-center space-x-2 shadow-2xl hover:shadow-3xl transform hover:-translate-y-1"
              >
                <DocumentTextIcon className="w-5 h-5" />
                <span>Analyze Resume Now</span>
                <ArrowRightIcon className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
              </Link>
              
              <Link
                to="/matches"
                className="group border-2 border-white/30 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:bg-white/10 transition-all duration-300 flex items-center space-x-2 backdrop-blur-sm"
              >
                <ChartBarIcon className="w-5 h-5" />
                <span>Find Job Matches</span>
              </Link>
            </motion.div>

            {/* Stats */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto"
            >
              {stats.map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="flex justify-center mb-2">
                    <stat.icon className="w-8 h-8 text-cyan-400" />
                  </div>
                  <div className="text-3xl font-bold text-white">{stat.value}</div>
                  <div className="text-blue-200 text-sm">{stat.label}</div>
                </div>
              ))}
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-24 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl md:text-5xl font-bold text-gray-900 mb-4">
                Powerful AI Features
              </h2>
              <p className="text-xl text-gray-600 max-w-3xl mx-auto">
                Our cutting-edge AI technology analyzes your resume with precision, 
                providing insights that give you the competitive edge.
              </p>
            </motion.div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="group relative bg-white p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 border border-gray-100 hover:border-gray-200 transform hover:-translate-y-2"
              >
                <div className={`absolute inset-0 bg-gradient-to-r ${feature.gradient} opacity-0 group-hover:opacity-5 rounded-2xl transition-opacity duration-300`}></div>
                
                <div className={`relative w-12 h-12 rounded-xl bg-gradient-to-r ${feature.gradient} flex items-center justify-center mb-6 group-hover:scale-110 transition-transform duration-300`}>
                  <feature.icon className="w-6 h-6 text-white" />
                </div>
                
                <h3 className="text-xl font-semibold text-gray-900 mb-3 group-hover:text-gray-800">
                  {feature.title}
                </h3>
                
                <p className="text-gray-600 leading-relaxed group-hover:text-gray-700">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-24 bg-gradient-to-br from-gray-50 to-blue-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
                Why Choose ResumeAI?
              </h2>
              <p className="text-lg text-gray-600 mb-8">
                Join thousands of professionals who have accelerated their careers 
                with our intelligent resume optimization platform.
              </p>
              
              <div className="space-y-4">
                {benefits.map((benefit, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.4, delay: index * 0.1 }}
                    viewport={{ once: true }}
                    className="flex items-center space-x-3"
                  >
                    <div className="flex-shrink-0">
                      <CheckCircleIcon className="w-6 h-6 text-green-500" />
                    </div>
                    <span className="text-gray-700">{benefit}</span>
                  </motion.div>
                ))}
              </div>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
              className="relative"
            >
              <div className="bg-white p-8 rounded-3xl shadow-2xl border border-gray-100">
                <div className="text-center mb-6">
                  <div className="w-16 h-16 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                    <CpuChipIcon className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900">
                    AI-Powered Analysis
                  </h3>
                </div>
                
                <div className="space-y-6">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Resume Quality</span>
                    <span className="text-green-600 font-semibold">94%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <motion.div 
                      className="bg-gradient-to-r from-green-500 to-emerald-500 h-3 rounded-full"
                      initial={{ width: 0 }}
                      whileInView={{ width: '94%' }}
                      transition={{ duration: 1, delay: 0.5 }}
                      viewport={{ once: true }}
                    ></motion.div>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">ATS Compatibility</span>
                    <span className="text-blue-600 font-semibold">89%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <motion.div 
                      className="bg-gradient-to-r from-blue-500 to-cyan-500 h-3 rounded-full"
                      initial={{ width: 0 }}
                      whileInView={{ width: '89%' }}
                      transition={{ duration: 1, delay: 0.7 }}
                      viewport={{ once: true }}
                    ></motion.div>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Job Match Score</span>
                    <span className="text-purple-600 font-semibold">87%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-3">
                    <motion.div 
                      className="bg-gradient-to-r from-purple-500 to-pink-500 h-3 rounded-full"
                      initial={{ width: 0 }}
                      whileInView={{ width: '87%' }}
                      transition={{ duration: 1, delay: 0.9 }}
                      viewport={{ once: true }}
                    ></motion.div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-24 bg-gradient-to-r from-indigo-600 via-purple-600 to-blue-600 relative overflow-hidden">
        <div className="absolute inset-0 bg-black/20"></div>
        <div className="relative max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl md:text-5xl font-bold text-white mb-6">
              Ready to Transform Your Career?
            </h2>
            <p className="text-xl text-blue-100 mb-8 max-w-2xl mx-auto">
              Join thousands of professionals who have already accelerated their careers 
              with our AI-powered resume analysis platform.
            </p>
            <Link
              to="/analyze"
              className="group inline-flex items-center space-x-2 bg-white text-indigo-600 px-8 py-4 rounded-xl font-semibold text-lg hover:bg-blue-50 transition-all duration-300 shadow-2xl hover:shadow-3xl transform hover:-translate-y-1"
            >
              <RocketLaunchIcon className="w-5 h-5" />
              <span>Start Your Analysis</span>
              <ArrowRightIcon className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  )
}

export default Home
