import React from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import {
  DocumentTextIcon,
  ChartBarIcon,
  CpuChipIcon,
  LightBulbIcon,
  RocketLaunchIcon,
  CheckCircleIcon,
  ArrowRightIcon
} from '@heroicons/react/24/outline';

const Home = () => {
  const features = [
    {
      icon: DocumentTextIcon,
      title: 'Smart Resume Analysis',
      description: 'Advanced AI-powered text extraction and analysis from PDF and DOCX files with intelligent content parsing.',
      color: 'text-blue-600'
    },
    {
      icon: CpuChipIcon,
      title: 'ML-Powered Matching',
      description: 'Machine learning algorithms predict your selection probability and match you with the best opportunities.',
      color: 'text-purple-600'
    },
    {
      icon: ChartBarIcon,
      title: 'Skill Gap Analysis',
      description: 'Comprehensive skill assessment with personalized recommendations for career advancement.',
      color: 'text-green-600'
    },
    {
      icon: LightBulbIcon,
      title: 'Intelligent Feedback',
      description: 'Get actionable insights on resume improvement, ATS optimization, and professional presentation.',
      color: 'text-yellow-600'
    },
    {
      icon: RocketLaunchIcon,
      title: 'Career Acceleration',
      description: 'Upskilling recommendations with course suggestions and learning paths tailored to your goals.',
      color: 'text-red-600'
    }
  ];

  const benefits = [
    'Increase interview callbacks by up to 40%',
    'Save 10+ hours of manual resume optimization',
    'Get personalized career development roadmap',
    'Access to 1000+ relevant course recommendations',
    'Real-time ATS compatibility scoring',
    'Multi-job matching and prioritization'
  ];

  const stats = [
    { label: 'Resumes Analyzed', value: '50,000+' },
    { label: 'Success Rate', value: '94%' },
    { label: 'Time Saved', value: '10hrs+' },
    { label: 'Job Matches', value: '1M+' }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden bg-gradient-to-br from-blue-50 via-white to-purple-50 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
            >
              <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-6">
                Transform Your Career with{' '}
                <span className="gradient-text">AI-Powered</span>{' '}
                Resume Analysis
              </h1>
              <p className="text-xl text-gray-600 mb-8 max-w-3xl mx-auto">
                Get instant, intelligent feedback on your resume, discover skill gaps, 
                and receive personalized recommendations to land your dream job.
              </p>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.2 }}
              className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-12"
            >
              <Link
                to="/analysis"
                className="bg-blue-600 text-white px-8 py-4 rounded-lg font-semibold text-lg hover:bg-blue-700 transition-colors duration-200 flex items-center space-x-2 shadow-lg hover:shadow-xl"
              >
                <DocumentTextIcon className="w-5 h-5" />
                <span>Analyze Resume Now</span>
                <ArrowRightIcon className="w-4 h-4" />
              </Link>
              <Link
                to="/multi-job"
                className="border-2 border-blue-600 text-blue-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-blue-50 transition-colors duration-200 flex items-center space-x-2"
              >
                <ChartBarIcon className="w-5 h-5" />
                <span>Multi-Job Analysis</span>
              </Link>
            </motion.div>

            {/* Stats */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="grid grid-cols-2 md:grid-cols-4 gap-8 max-w-4xl mx-auto"
            >
              {stats.map((stat, index) => (
                <div key={index} className="text-center">
                  <div className="text-3xl font-bold text-blue-600">{stat.value}</div>
                  <div className="text-gray-600 mt-1">{stat.label}</div>
                </div>
              ))}
            </motion.div>
          </div>
        </div>

        {/* Background decoration */}
        <div className="absolute top-0 right-0 -mt-4 opacity-10">
          <svg width="404" height="384" fill="none" viewBox="0 0 404 384">
            <defs>
              <pattern id="b1e6e422" x="0" y="0" width="20" height="20" patternUnits="userSpaceOnUse">
                <rect x="0" y="0" width="4" height="4" fill="currentColor" />
              </pattern>
            </defs>
            <rect width="404" height="384" fill="url(#b1e6e422)" />
          </svg>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 bg-white">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
              Powerful Features for Career Success
            </h2>
            <p className="text-xl text-gray-600 max-w-3xl mx-auto">
              Our AI-powered platform combines cutting-edge technology with career expertise 
              to give you the competitive edge you need.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                viewport={{ once: true }}
                className="bg-white p-8 rounded-xl shadow-lg hover:shadow-xl transition-shadow duration-300 border border-gray-100 card-hover"
              >
                <div className={`w-12 h-12 rounded-lg bg-gray-50 flex items-center justify-center mb-6 ${feature.color}`}>
                  <feature.icon className="w-6 h-6" />
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
        </div>
      </section>

      {/* Benefits Section */}
      <section className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              whileInView={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
              viewport={{ once: true }}
            >
              <h2 className="text-3xl md:text-4xl font-bold text-gray-900 mb-6">
                Why Choose Our AI Resume Analyzer?
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
                    <CheckCircleIcon className="w-6 h-6 text-green-500 flex-shrink-0" />
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
              <div className="bg-white p-8 rounded-2xl shadow-xl">
                <div className="text-center mb-6">
                  <div className="w-16 h-16 bg-gradient-to-r from-blue-600 to-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                    <CpuChipIcon className="w-8 h-8 text-white" />
                  </div>
                  <h3 className="text-2xl font-bold text-gray-900">
                    AI-Powered Analysis
                  </h3>
                </div>
                
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Resume Quality</span>
                    <span className="text-green-600 font-semibold">94%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-green-500 h-2 rounded-full" style={{ width: '94%' }}></div>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">ATS Compatibility</span>
                    <span className="text-blue-600 font-semibold">89%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-blue-500 h-2 rounded-full" style={{ width: '89%' }}></div>
                  </div>
                  
                  <div className="flex justify-between items-center">
                    <span className="text-gray-600">Skill Match</span>
                    <span className="text-purple-600 font-semibold">87%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div className="bg-purple-500 h-2 rounded-full" style={{ width: '87%' }}></div>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-purple-600">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            viewport={{ once: true }}
          >
            <h2 className="text-3xl md:text-4xl font-bold text-white mb-6">
              Ready to Transform Your Career?
            </h2>
            <p className="text-xl text-blue-100 mb-8">
              Join thousands of professionals who have already accelerated their careers 
              with our AI-powered resume analysis.
            </p>
            <Link
              to="/analysis"
              className="bg-white text-blue-600 px-8 py-4 rounded-lg font-semibold text-lg hover:bg-gray-100 transition-colors duration-200 inline-flex items-center space-x-2 shadow-lg"
            >
              <RocketLaunchIcon className="w-5 h-5" />
              <span>Start Your Analysis</span>
            </Link>
          </motion.div>
        </div>
      </section>
    </div>
  );
};

export default Home;
