import React from 'react';
import { Brain, Target, Users, Lightbulb, Shield, Globe } from 'lucide-react';

const About: React.FC = () => {
  return (
    <div className="py-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <div className="flex justify-center mb-6">
            <div className="p-4 bg-blue-100 rounded-full">
              <Brain className="h-12 w-12 text-blue-600" />
            </div>
          </div>
          <h1 className="text-4xl font-bold text-gray-900 mb-6">About Citizen AI</h1>
          <p className="text-xl text-gray-600">
            Revolutionizing how communities connect, communicate, and collaborate through intelligent technology
          </p>
        </div>

        {/* Mission Section */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-12">
          <div className="flex items-center mb-6">
            <Target className="h-8 w-8 text-blue-600 mr-3" />
            <h2 className="text-2xl font-bold text-gray-900">Our Mission</h2>
          </div>
          <p className="text-lg text-gray-700 leading-relaxed">
            At Citizen AI, we believe that technology should bridge the gap between citizens and their governments. 
            Our mission is to empower communities with intelligent tools that make civic engagement more accessible, 
            efficient, and impactful. We're committed to creating a more responsive and transparent democracy through 
            the power of artificial intelligence.
          </p>
        </div>

        {/* Services Overview */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-12">
          <div className="flex items-center mb-6">
            <Lightbulb className="h-8 w-8 text-green-600 mr-3" />
            <h2 className="text-2xl font-bold text-gray-900">What We Do</h2>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="p-4 border border-gray-200 rounded-lg">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Sentiment Analysis</h3>
              <p className="text-gray-600">
                Advanced AI algorithms analyze public sentiment from various sources to provide real-time insights 
                into community mood and concerns.
              </p>
            </div>
            <div className="p-4 border border-gray-200 rounded-lg">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Concern Reporting</h3>
              <p className="text-gray-600">
                Streamlined digital platform for citizens to report issues, concerns, and suggestions directly 
                to relevant authorities with automatic categorization.
              </p>
            </div>
            <div className="p-4 border border-gray-200 rounded-lg">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">AI-Powered Analytics</h3>
              <p className="text-gray-600">
                Comprehensive dashboards and reports that help government agencies understand trends, 
                prioritize issues, and make data-driven decisions.
              </p>
            </div>
            <div className="p-4 border border-gray-200 rounded-lg">
              <h3 className="text-lg font-semibold text-gray-900 mb-2">Smart Communication</h3>
              <p className="text-gray-600">
                AI assistant that provides 24/7 support to citizens, answering questions and directing 
                them to appropriate resources and services.
              </p>
            </div>
          </div>
        </div>

        {/* Values */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-12">
          <div className="flex items-center mb-6">
            <Shield className="h-8 w-8 text-purple-600 mr-3" />
            <h2 className="text-2xl font-bold text-gray-900">Our Values</h2>
          </div>
          <div className="space-y-6">
            <div className="flex items-start">
              <div className="p-2 bg-blue-100 rounded-lg mr-4 mt-1">
                <Users className="h-5 w-5 text-blue-600" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">Transparency</h3>
                <p className="text-gray-600">
                  We believe in open, honest communication and making our processes clear and understandable to all stakeholders.
                </p>
              </div>
            </div>
            <div className="flex items-start">
              <div className="p-2 bg-green-100 rounded-lg mr-4 mt-1">
                <Shield className="h-5 w-5 text-green-600" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">Privacy & Security</h3>
                <p className="text-gray-600">
                  Protecting citizen data and maintaining the highest standards of cybersecurity is our top priority.
                </p>
              </div>
            </div>
            <div className="flex items-start">
              <div className="p-2 bg-purple-100 rounded-lg mr-4 mt-1">
                <Globe className="h-5 w-5 text-purple-600" />
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-1">Accessibility</h3>
                <p className="text-gray-600">
                  Our platform is designed to be inclusive and accessible to all citizens, regardless of technical expertise or abilities.
                </p>
              </div>
            </div>
          </div>
        </div>

        {/* Impact */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-8 text-white">
          <h2 className="text-2xl font-bold mb-4">Making a Difference</h2>
          <p className="text-lg mb-6">
            Since our launch, Citizen AI has helped over 50 government agencies and community organizations 
            improve their citizen engagement, resulting in faster response times, better resource allocation, 
            and increased public satisfaction.
          </p>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-center">
            <div>
              <div className="text-3xl font-bold mb-2">10,000+</div>
              <div className="text-blue-100">Concerns Processed</div>
            </div>
            <div>
              <div className="text-3xl font-bold mb-2">95%</div>
              <div className="text-blue-100">Satisfaction Rate</div>
            </div>
            <div>
              <div className="text-3xl font-bold mb-2">50+</div>
              <div className="text-blue-100">Partner Organizations</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default About;