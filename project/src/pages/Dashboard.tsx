import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, LineChart, Line, PieChart, Pie, Cell, ResponsiveContainer } from 'recharts';
import { TrendingUp, Users, MessageSquare, AlertCircle, Calendar, Filter, MessageCircleHeart } from 'lucide-react';
import { useData } from '../context/DataContext';

const Dashboard: React.FC = () => {
  const { concerns, getConcernsByType } = useData();

  // Generate dynamic data based on actual submissions
  const generateWeeklyData = () => {
    const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    const now = new Date();
    
    return days.map((day, index) => {
      const dayDate = new Date(now);
      dayDate.setDate(now.getDate() - (6 - index));
      
      const dayConcerns = concerns.filter(concern => {
        const concernDate = new Date(concern.timestamp);
        return concernDate.toDateString() === dayDate.toDateString();
      });
      
      const avgSentiment = dayConcerns.length > 0 
        ? dayConcerns.reduce((acc, concern) => {
            const score = concern.sentiment === 'positive' ? 5 : concern.sentiment === 'negative' ? 1 : 3;
            return acc + score;
          }, 0) / dayConcerns.length
        : 3;

      return {
        day,
        concerns: dayConcerns.length,
        sentiment: Number(avgSentiment.toFixed(1))
      };
    });
  };

  const weeklyData = generateWeeklyData();

  const sentimentData = [
    { 
      name: 'Positive', 
      value: concerns.filter(c => c.sentiment === 'positive').length, 
      color: '#10B981' 
    },
    { 
      name: 'Neutral', 
      value: concerns.filter(c => c.sentiment === 'neutral').length, 
      color: '#F59E0B' 
    },
    { 
      name: 'Negative', 
      value: concerns.filter(c => c.sentiment === 'negative').length, 
      color: '#EF4444' 
    },
  ];

  const categoryData = [
    { category: 'Infrastructure', count: concerns.filter(c => c.category === 'Infrastructure').length },
    { category: 'Public Safety', count: concerns.filter(c => c.category === 'Public Safety').length },
    { category: 'Environment', count: concerns.filter(c => c.category === 'Environment').length },
    { category: 'Transportation', count: concerns.filter(c => c.category === 'Transportation').length },
    { category: 'General', count: concerns.filter(c => c.category === 'General').length },
  ].filter(item => item.count > 0);

  const recentConcerns = getConcernsByType('concern').slice(0, 5);
  const recentFeedback = getConcernsByType('feedback').slice(0, 5);

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'bg-red-100 text-red-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-green-100 text-green-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return 'bg-green-100 text-green-800';
      case 'negative': return 'bg-red-100 text-red-800';
      case 'neutral': return 'bg-yellow-100 text-yellow-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const totalConcerns = concerns.length;
  const concernsCount = getConcernsByType('concern').length;
  const feedbackCount = getConcernsByType('feedback').length;
  const avgSentiment = concerns.length > 0 
    ? concerns.reduce((acc, concern) => {
        const score = concern.sentiment === 'positive' ? 5 : concern.sentiment === 'negative' ? 1 : 3;
        return acc + score;
      }, 0) / concerns.length
    : 3;

  return (
    <div className="py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Dashboard</h1>
            <p className="text-gray-600">Real-time analysis and insights from citizen submissions</p>
          </div>
          <div className="flex items-center space-x-2 mt-4 sm:mt-0">
            <Calendar className="h-5 w-5 text-gray-400" />
            <span className="text-sm text-gray-600">Live Data</span>
          </div>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Total Submissions</p>
                <p className="text-2xl font-bold text-gray-900">{totalConcerns}</p>
                <p className="text-sm text-blue-600">All time</p>
              </div>
              <div className="p-3 bg-blue-100 rounded-lg">
                <MessageSquare className="h-6 w-6 text-blue-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Active Concerns</p>
                <p className="text-2xl font-bold text-gray-900">{concernsCount}</p>
                <p className="text-sm text-red-600">Needs attention</p>
              </div>
              <div className="p-3 bg-red-100 rounded-lg">
                <AlertCircle className="h-6 w-6 text-red-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Positive Feedback</p>
                <p className="text-2xl font-bold text-gray-900">{feedbackCount}</p>
                <p className="text-sm text-green-600">Community input</p>
              </div>
              <div className="p-3 bg-green-100 rounded-lg">
                <MessageCircleHeart className="h-6 w-6 text-green-600" />
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-gray-600">Avg. Sentiment</p>
                <p className="text-2xl font-bold text-gray-900">{avgSentiment.toFixed(1)}/5</p>
                <p className="text-sm text-purple-600">Community mood</p>
              </div>
              <div className="p-3 bg-purple-100 rounded-lg">
                <TrendingUp className="h-6 w-6 text-purple-600" />
              </div>
            </div>
          </div>
        </div>

        {/* Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Weekly Submissions Chart */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Weekly Submissions</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={weeklyData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="concerns" fill="#3B82F6" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Sentiment Distribution Chart */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Sentiment Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <PieChart>
                <Pie
                  data={sentimentData}
                  cx="50%"
                  cy="50%"
                  outerRadius={100}
                  fill="#8884d8"
                  dataKey="value"
                  label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                >
                  {sentimentData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-8">
          {/* Category Breakdown */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Submissions by Category</h3>
            {categoryData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={categoryData} layout="horizontal">
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" />
                  <YAxis dataKey="category" type="category" width={100} />
                  <Tooltip />
                  <Bar dataKey="count" fill="#10B981" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="flex items-center justify-center h-64 text-gray-500">
                <p>No data available yet. Submit some concerns or feedback to see analytics.</p>
              </div>
            )}
          </div>

          {/* Recent Activity Summary */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Activity Summary</h3>
            <div className="space-y-4">
              <div className="p-4 bg-red-50 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-semibold text-red-800">High Priority Concerns</h4>
                  <span className="text-red-600 font-bold">
                    {concerns.filter(c => c.priority === 'high').length}
                  </span>
                </div>
                <p className="text-sm text-red-600">Require immediate attention</p>
              </div>
              
              <div className="p-4 bg-yellow-50 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-semibold text-yellow-800">Medium Priority</h4>
                  <span className="text-yellow-600 font-bold">
                    {concerns.filter(c => c.priority === 'medium').length}
                  </span>
                </div>
                <p className="text-sm text-yellow-600">Should be addressed soon</p>
              </div>
              
              <div className="p-4 bg-green-50 rounded-lg">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-semibold text-green-800">Positive Feedback</h4>
                  <span className="text-green-600 font-bold">
                    {concerns.filter(c => c.sentiment === 'positive').length}
                  </span>
                </div>
                <p className="text-sm text-green-600">Community appreciation</p>
              </div>
            </div>
          </div>
        </div>

        {/* Separate Lists for Concerns and Feedback */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Recent Concerns */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900 flex items-center">
                <AlertCircle className="h-5 w-5 text-red-500 mr-2" />
                Recent Concerns
              </h3>
              <span className="text-sm text-gray-500">{concernsCount} total</span>
            </div>
            <div className="space-y-4 max-h-80 overflow-y-auto">
              {recentConcerns.length > 0 ? (
                recentConcerns.map((concern) => (
                  <div key={concern.id} className="p-4 border border-red-200 rounded-lg hover:bg-red-50 transition-colors">
                    <div className="flex items-start justify-between mb-2">
                      <p className="text-sm text-gray-900 font-medium">{concern.message}</p>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(concern.priority)}`}>
                        {concern.priority}
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-xs text-gray-500">
                      <div className="flex items-center space-x-2">
                        <span className={`px-2 py-1 rounded-full ${getSentimentColor(concern.sentiment)}`}>
                          {concern.sentiment}
                        </span>
                        <span>{concern.category}</span>
                      </div>
                      <span>{concern.timestamp}</span>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <AlertCircle className="h-12 w-12 mx-auto mb-2 text-gray-300" />
                  <p>No concerns reported yet</p>
                </div>
              )}
            </div>
          </div>

          {/* Recent Feedback */}
          <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900 flex items-center">
                <MessageCircleHeart className="h-5 w-5 text-green-500 mr-2" />
                Recent Feedback
              </h3>
              <span className="text-sm text-gray-500">{feedbackCount} total</span>
            </div>
            <div className="space-y-4 max-h-80 overflow-y-auto">
              {recentFeedback.length > 0 ? (
                recentFeedback.map((feedback) => (
                  <div key={feedback.id} className="p-4 border border-green-200 rounded-lg hover:bg-green-50 transition-colors">
                    <div className="flex items-start justify-between mb-2">
                      <p className="text-sm text-gray-900 font-medium">{feedback.message}</p>
                      <span className={`px-2 py-1 rounded-full text-xs font-medium ${getPriorityColor(feedback.priority)}`}>
                        {feedback.priority}
                      </span>
                    </div>
                    <div className="flex items-center justify-between text-xs text-gray-500">
                      <div className="flex items-center space-x-2">
                        <span className={`px-2 py-1 rounded-full ${getSentimentColor(feedback.sentiment)}`}>
                          {feedback.sentiment}
                        </span>
                        <span>{feedback.category}</span>
                      </div>
                      <span>{feedback.timestamp}</span>
                    </div>
                  </div>
                ))
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <MessageCircleHeart className="h-12 w-12 mx-auto mb-2 text-gray-300" />
                  <p>No feedback submitted yet</p>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;