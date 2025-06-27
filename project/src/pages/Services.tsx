import React, { useState } from 'react';
import { BarChart3, MessageSquare, Send, TrendingUp, AlertCircle, CheckCircle, MessageCircleHeart } from 'lucide-react';
import { useData } from '../context/DataContext';

const Services: React.FC = () => {
  const [concernText, setConcernText] = useState('');
  const [feedbackText, setFeedbackText] = useState('');
  const [isSubmittingConcern, setIsSubmittingConcern] = useState(false);
  const [isSubmittingFeedback, setIsSubmittingFeedback] = useState(false);
  const { concerns, addConcern, getConcernsByType } = useData();

  const analyzeSentiment = (text: string): 'positive' | 'negative' | 'neutral' => {
    const positiveWords = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'happy', 'satisfied', 'love', 'perfect', 'outstanding', 'fantastic', 'awesome', 'brilliant', 'superb'];
    const negativeWords = ['bad', 'terrible', 'awful', 'horrible', 'hate', 'angry', 'frustrated', 'disappointed', 'poor', 'worst', 'broken', 'damaged', 'problem', 'issue', 'concern'];
    
    const lowercaseText = text.toLowerCase();
    const positiveCount = positiveWords.filter(word => lowercaseText.includes(word)).length;
    const negativeCount = negativeWords.filter(word => lowercaseText.includes(word)).length;
    
    if (positiveCount > negativeCount) return 'positive';
    if (negativeCount > positiveCount) return 'negative';
    return 'neutral';
  };

  const categorizeMessage = (text: string): string => {
    const categories = {
      'Infrastructure': ['road', 'bridge', 'water', 'sewer', 'traffic', 'construction', 'maintenance', 'streetlight', 'pothole'],
      'Public Safety': ['police', 'fire', 'emergency', 'crime', 'safety', 'security', 'patrol'],
      'Environment': ['pollution', 'waste', 'recycling', 'park', 'green', 'environment', 'clean', 'trash', 'garbage'],
      'Transportation': ['bus', 'transit', 'parking', 'transportation', 'commute', 'route'],
      'General': []
    };
    
    const lowercaseText = text.toLowerCase();
    
    for (const [category, keywords] of Object.entries(categories)) {
      if (keywords.some(keyword => lowercaseText.includes(keyword))) {
        return category;
      }
    }
    
    return 'General';
  };

  const handleSubmitConcern = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!concernText.trim()) return;

    setIsSubmittingConcern(true);
    
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    addConcern({
      message: concernText,
      sentiment: analyzeSentiment(concernText),
      category: categorizeMessage(concernText),
      type: 'concern'
    });

    setConcernText('');
    setIsSubmittingConcern(false);
  };

  const handleSubmitFeedback = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!feedbackText.trim()) return;

    setIsSubmittingFeedback(true);
    
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    addConcern({
      message: feedbackText,
      sentiment: analyzeSentiment(feedbackText),
      category: categorizeMessage(feedbackText),
      type: 'feedback'
    });

    setFeedbackText('');
    setIsSubmittingFeedback(false);
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return 'text-green-600 bg-green-100';
      case 'negative': return 'text-red-600 bg-red-100';
      default: return 'text-yellow-600 bg-yellow-100';
    }
  };

  const getSentimentIcon = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return <CheckCircle className="h-4 w-4" />;
      case 'negative': return <AlertCircle className="h-4 w-4" />;
      default: return <TrendingUp className="h-4 w-4" />;
    }
  };

  const recentConcerns = getConcernsByType('concern').slice(0, 3);
  const recentFeedback = getConcernsByType('feedback').slice(0, 3);

  return (
    <div className="py-16 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        {/* Header */}
        <div className="text-center mb-16">
          <h1 className="text-4xl font-bold text-gray-900 mb-6">Our Services</h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Comprehensive AI-powered tools designed to enhance citizen engagement and improve community services
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
          {/* Concern Reporting Section */}
          <div className="bg-white rounded-xl shadow-lg p-8">
            <div className="flex items-center mb-6">
              <div className="p-3 bg-red-100 rounded-lg mr-4">
                <AlertCircle className="h-6 w-6 text-red-600" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900">Report a Concern</h2>
            </div>

            <p className="text-gray-600 mb-6">
              Report issues, problems, or concerns that need attention from local authorities. Our AI will analyze and prioritize your submission.
            </p>

            <form onSubmit={handleSubmitConcern} className="space-y-4">
              <div>
                <label htmlFor="concern" className="block text-sm font-medium text-gray-700 mb-2">
                  Describe Your Concern
                </label>
                <textarea
                  id="concern"
                  value={concernText}
                  onChange={(e) => setConcernText(e.target.value)}
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-red-500 focus:border-red-500 resize-none"
                  placeholder="Please describe the issue or concern in detail..."
                  required
                />
              </div>
              
              <button
                type="submit"
                disabled={isSubmittingConcern || !concernText.trim()}
                className="w-full flex items-center justify-center px-4 py-2 bg-red-600 text-white rounded-lg hover:bg-red-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {isSubmittingConcern ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Processing...
                  </>
                ) : (
                  <>
                    <Send className="h-4 w-4 mr-2" />
                    Submit Concern
                  </>
                )}
              </button>
            </form>

            {recentConcerns.length > 0 && (
              <div className="mt-6">
                <h3 className="font-semibold text-gray-900 mb-3">Recent Concerns:</h3>
                <div className="space-y-3">
                  {recentConcerns.map((concern) => (
                    <div key={concern.id} className="p-3 border border-gray-200 rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium flex items-center gap-1 ${getSentimentColor(concern.sentiment)}`}>
                          {getSentimentIcon(concern.sentiment)}
                          {concern.sentiment.charAt(0).toUpperCase() + concern.sentiment.slice(1)}
                        </span>
                        <span className="text-xs text-gray-500">{concern.category}</span>
                      </div>
                      <p className="text-sm text-gray-600">{concern.message}</p>
                      <p className="text-xs text-gray-400 mt-1">{concern.timestamp}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* Feedback Section */}
          <div className="bg-white rounded-xl shadow-lg p-8">
            <div className="flex items-center mb-6">
              <div className="p-3 bg-green-100 rounded-lg mr-4">
                <MessageCircleHeart className="h-6 w-6 text-green-600" />
              </div>
              <h2 className="text-2xl font-bold text-gray-900">Share Feedback</h2>
            </div>

            <p className="text-gray-600 mb-6">
              Share positive feedback, suggestions, or general comments about city services and community programs.
            </p>

            <form onSubmit={handleSubmitFeedback} className="space-y-4">
              <div>
                <label htmlFor="feedback" className="block text-sm font-medium text-gray-700 mb-2">
                  Your Feedback
                </label>
                <textarea
                  id="feedback"
                  value={feedbackText}
                  onChange={(e) => setFeedbackText(e.target.value)}
                  rows={4}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 resize-none"
                  placeholder="Share your thoughts, suggestions, or positive feedback..."
                  required
                />
              </div>
              
              <button
                type="submit"
                disabled={isSubmittingFeedback || !feedbackText.trim()}
                className="w-full flex items-center justify-center px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {isSubmittingFeedback ? (
                  <>
                    <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                    Processing...
                  </>
                ) : (
                  <>
                    <Send className="h-4 w-4 mr-2" />
                    Submit Feedback
                  </>
                )}
              </button>
            </form>

            {recentFeedback.length > 0 && (
              <div className="mt-6">
                <h3 className="font-semibold text-gray-900 mb-3">Recent Feedback:</h3>
                <div className="space-y-3">
                  {recentFeedback.map((feedback) => (
                    <div key={feedback.id} className="p-3 border border-gray-200 rounded-lg">
                      <div className="flex items-center justify-between mb-2">
                        <span className={`px-2 py-1 rounded-full text-xs font-medium flex items-center gap-1 ${getSentimentColor(feedback.sentiment)}`}>
                          {getSentimentIcon(feedback.sentiment)}
                          {feedback.sentiment.charAt(0).toUpperCase() + feedback.sentiment.slice(1)}
                        </span>
                        <span className="text-xs text-gray-500">{feedback.category}</span>
                      </div>
                      <p className="text-sm text-gray-600">{feedback.message}</p>
                      <p className="text-xs text-gray-400 mt-1">{feedback.timestamp}</p>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Sentiment Analysis Section */}
        <div className="bg-white rounded-xl shadow-lg p-8 mb-8">
          <div className="flex items-center mb-6">
            <div className="p-3 bg-blue-100 rounded-lg mr-4">
              <BarChart3 className="h-6 w-6 text-blue-600" />
            </div>
            <h2 className="text-2xl font-bold text-gray-900">Sentiment Analysis</h2>
          </div>
          
          <p className="text-gray-600 mb-6">
            Our advanced AI analyzes all submissions to understand community sentiment and identify trends in real-time.
          </p>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="p-4 bg-gray-50 rounded-lg">
              <h3 className="font-semibold text-gray-900 mb-2">Key Features:</h3>
              <ul className="space-y-2 text-gray-600">
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                  Real-time sentiment detection
                </li>
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                  Automatic categorization
                </li>
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                  Priority assessment
                </li>
                <li className="flex items-center">
                  <CheckCircle className="h-4 w-4 text-green-500 mr-2" />
                  Trend analysis and reporting
                </li>
              </ul>
            </div>

            <div className="p-4 bg-blue-50 rounded-lg">
              <h3 className="font-semibold text-gray-900 mb-2">Current Statistics:</h3>
              <div className="space-y-2">
                <div className="flex justify-between">
                  <span className="text-gray-600">Total Submissions:</span>
                  <span className="font-semibold">{concerns.length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Concerns:</span>
                  <span className="font-semibold text-red-600">{getConcernsByType('concern').length}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Feedback:</span>
                  <span className="font-semibold text-green-600">{getConcernsByType('feedback').length}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Additional Services */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="bg-white rounded-xl shadow-lg p-6 text-center">
            <div className="p-3 bg-purple-100 rounded-lg w-fit mx-auto mb-4">
              <TrendingUp className="h-8 w-8 text-purple-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Predictive Analytics</h3>
            <p className="text-gray-600">
              Forecast trends and potential issues before they become major problems using advanced machine learning algorithms.
            </p>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6 text-center">
            <div className="p-3 bg-orange-100 rounded-lg w-fit mx-auto mb-4">
              <AlertCircle className="h-8 w-8 text-orange-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Priority Assessment</h3>
            <p className="text-gray-600">
              Automatically prioritize concerns based on severity, impact, and urgency to ensure critical issues are addressed first.
            </p>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6 text-center">
            <div className="p-3 bg-indigo-100 rounded-lg w-fit mx-auto mb-4">
              <CheckCircle className="h-8 w-8 text-indigo-600" />
            </div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Follow-up System</h3>
            <p className="text-gray-600">
              Automated follow-up system to keep citizens informed about the status and resolution of their submitted concerns.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Services;