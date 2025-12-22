import React from 'react'
import { motion } from 'framer-motion'
import { 
  CpuChipIcon,
  ChartBarIcon,
  LightBulbIcon,
  RocketLaunchIcon,
  UserGroupIcon,
  ShieldCheckIcon
} from '@heroicons/react/24/outline'

const About = () => {
  const features = [
    {
      icon: CpuChipIcon,
      title: 'Advanced AI Technology',
      description: 'Powered by state-of-the-art machine learning models and natural language processing to deliver precise resume analysis.'
    },
    {
      icon: ChartBarIcon,
      title: 'Data-Driven Insights',
      description: 'Get quantifiable metrics and actionable feedback based on analysis of thousands of successful resumes and job descriptions.'
    },
    {
      icon: LightBulbIcon,
      title: 'Personalized Recommendations',
      description: 'Receive tailored suggestions for skill development, course recommendations, and career advancement strategies.'
    },
    {
      icon: RocketLaunchIcon,
      title: 'Career Acceleration',
      description: 'Optimize your resume for ATS systems and increase your interview callback rate by up to 40%.'
    },
    {
      icon: UserGroupIcon,
      title: 'Industry Expertise',
      description: 'Built by career experts and data scientists with deep understanding of modern recruitment processes.'
    },
    {
      icon: ShieldCheckIcon,
      title: 'Privacy & Security',
      description: 'Your resume data is processed securely and never stored permanently. Complete privacy guaranteed.'
    }
  ]

  const techStack = [
    { name: 'FastAPI', description: 'High-performance Python web framework' },
    { name: 'React', description: 'Modern frontend library with TypeScript' },
    { name: 'Machine Learning', description: 'Scikit-learn, XGBoost for predictions' },
    { name: 'NLP', description: 'Advanced text processing and analysis' },
    { name: 'Docker', description: 'Containerized deployment' },
    { name: 'Cloud Ready', description: 'Scalable cloud architecture' }
  ]

  return (
    <div className="min-h-screen py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center mb-16"
        >
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            About <span className="bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">ResumeAI</span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto leading-relaxed">
            We're revolutionizing the job search process with AI-powered resume analysis, 
            helping professionals land their dream jobs faster and more effectively.
          </p>
        </motion.div>

        {/* Mission Statement */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="bg-gradient-to-r from-indigo-600 to-purple-600 rounded-3xl p-12 mb-16 text-white text-center"
        >
          <h2 className="text-3xl font-bold mb-6">Our Mission</h2>
          <p className="text-xl leading-relaxed max-w-4xl mx-auto">
            To democratize career success by providing everyone with access to professional-grade 
            resume analysis and career guidance, powered by cutting-edge artificial intelligence.
          </p>
        </motion.div>

        {/* Features Grid */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="mb-16"
        >
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
            Why Choose ResumeAI?
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-white p-8 rounded-2xl shadow-lg border border-gray-100 hover:shadow-xl transition-all duration-300"
              >
                <div className="w-12 h-12 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-xl flex items-center justify-center mb-6">
                  <feature.icon className="w-6 h-6 text-white" />
                </div>
                <h3 className="text-xl font-semibold text-gray-900 mb-3">
                  {feature.title}
                </h3>
                <p className="text-gray-600 leading-relaxed">
                  {feature.description}
                </p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Technology Stack */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="mb-16"
        >
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
            Built with Modern Technology
          </h2>
          
          <div className="bg-white rounded-3xl shadow-lg p-8 border border-gray-100">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {techStack.map((tech, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, scale: 0.9 }}
                  whileInView={{ opacity: 1, scale: 1 }}
                  transition={{ duration: 0.4, delay: index * 0.1 }}
                  viewport={{ once: true }}
                  className="text-center p-6 rounded-xl bg-gradient-to-br from-gray-50 to-blue-50 hover:from-indigo-50 hover:to-purple-50 transition-all duration-300"
                >
                  <h3 className="text-lg font-semibold text-gray-900 mb-2">
                    {tech.name}
                  </h3>
                  <p className="text-gray-600 text-sm">
                    {tech.description}
                  </p>
                </motion.div>
              ))}
            </div>
          </div>
        </motion.div>

        {/* Stats */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="bg-gradient-to-br from-gray-50 to-blue-50 rounded-3xl p-12 mb-16"
        >
          <h2 className="text-3xl font-bold text-gray-900 text-center mb-12">
            Trusted by Professionals Worldwide
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-4xl font-bold text-indigo-600 mb-2">50,000+</div>
              <div className="text-gray-600">Resumes Analyzed</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-purple-600 mb-2">94%</div>
              <div className="text-gray-600">Success Rate</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-blue-600 mb-2">1M+</div>
              <div className="text-gray-600">Job Matches</div>
            </div>
            <div>
              <div className="text-4xl font-bold text-green-600 mb-2">40%</div>
              <div className="text-gray-600">Increase in Callbacks</div>
            </div>
          </div>
        </motion.div>

        {/* CTA */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          viewport={{ once: true }}
          className="text-center"
        >
          <h2 className="text-3xl font-bold text-gray-900 mb-6">
            Ready to Transform Your Career?
          </h2>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Join thousands of professionals who have already accelerated their careers with ResumeAI.
          </p>
          <a
            href="/analyze"
            className="inline-flex items-center space-x-2 bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-8 py-4 rounded-xl font-semibold text-lg hover:from-indigo-700 hover:to-purple-700 transition-all duration-200 shadow-lg hover:shadow-xl"
          >
            <RocketLaunchIcon className="w-5 h-5" />
            <span>Start Your Analysis</span>
          </a>
        </motion.div>
      </div>
    </div>
  )
}

export default About
