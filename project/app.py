from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_cors import CORS
import os
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__, static_folder='dist', static_url_path='')
CORS(app)

# In-memory storage for demo (in production, use a database)
concerns_data = []
feedback_data = []

# Sample data for demonstration
sample_concerns = [
    {
        "id": "1",
        "message": "The streetlight near Kakinada Port area has been out for a week, causing safety concerns for night workers",
        "category": "Infrastructure",
        "sentiment": "negative",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": "concern",
        "priority": "high"
    },
    {
        "id": "2",
        "message": "Need more police patrols in the evening hours around Main Road market area for better security",
        "category": "Public Safety",
        "sentiment": "neutral",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": "concern",
        "priority": "medium"
    }
]

sample_feedback = [
    {
        "id": "1",
        "message": "Great job on the new community center at Jagannaickpur! The facilities are excellent and well-maintained",
        "category": "General",
        "sentiment": "positive",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": "feedback",
        "priority": "low"
    }
]

# Initialize with sample data
concerns_data.extend(sample_concerns)
feedback_data.extend(sample_feedback)

def analyze_sentiment(text):
    """Simple sentiment analysis"""
    positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'happy', 'satisfied', 'love', 'perfect']
    negative_words = ['bad', 'terrible', 'awful', 'horrible', 'hate', 'angry', 'frustrated', 'disappointed', 'poor', 'broken']
    
    text_lower = text.lower()
    positive_count = sum(1 for word in positive_words if word in text_lower)
    negative_count = sum(1 for word in negative_words if word in text_lower)
    
    if positive_count > negative_count:
        return 'positive'
    elif negative_count > positive_count:
        return 'negative'
    else:
        return 'neutral'

def categorize_message(text):
    """Simple categorization based on keywords"""
    categories = {
        'Infrastructure': ['road', 'bridge', 'water', 'sewer', 'traffic', 'construction', 'streetlight', 'pothole'],
        'Public Safety': ['police', 'fire', 'emergency', 'crime', 'safety', 'security'],
        'Environment': ['pollution', 'waste', 'recycling', 'park', 'green', 'environment', 'clean'],
        'Transportation': ['bus', 'transit', 'parking', 'transportation', 'commute'],
        'General': []
    }
    
    text_lower = text.lower()
    for category, keywords in categories.items():
        if any(keyword in text_lower for keyword in keywords):
            return category
    return 'General'

def determine_priority(sentiment, category):
    """Determine priority based on sentiment and category"""
    if sentiment == 'negative':
        if category in ['Public Safety', 'Infrastructure']:
            return 'high'
        return 'medium'
    elif sentiment == 'neutral':
        return 'medium'
    return 'low'

# Routes
@app.route('/')
def index():
    """Serve the React app"""
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    """Serve static files"""
    if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# API Routes
@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    })

@app.route('/api/concerns', methods=['GET', 'POST'])
def handle_concerns():
    """Handle concern submissions and retrieval"""
    if request.method == 'POST':
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Message is required"}), 400
        
        # Analyze the concern
        sentiment = analyze_sentiment(data['message'])
        category = categorize_message(data['message'])
        priority = determine_priority(sentiment, category)
        
        concern = {
            "id": str(len(concerns_data) + 1),
            "message": data['message'],
            "category": category,
            "sentiment": sentiment,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "concern",
            "priority": priority
        }
        
        concerns_data.append(concern)
        logger.info(f"New concern submitted: {concern['id']}")
        
        return jsonify(concern), 201
    
    # GET request
    return jsonify(concerns_data)

@app.route('/api/feedback', methods=['GET', 'POST'])
def handle_feedback():
    """Handle feedback submissions and retrieval"""
    if request.method == 'POST':
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Message is required"}), 400
        
        # Analyze the feedback
        sentiment = analyze_sentiment(data['message'])
        category = categorize_message(data['message'])
        priority = determine_priority(sentiment, category)
        
        feedback = {
            "id": str(len(feedback_data) + 1),
            "message": data['message'],
            "category": category,
            "sentiment": sentiment,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": "feedback",
            "priority": priority
        }
        
        feedback_data.append(feedback)
        logger.info(f"New feedback submitted: {feedback['id']}")
        
        return jsonify(feedback), 201
    
    # GET request
    return jsonify(feedback_data)

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle chat messages"""
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({"error": "Message is required"}), 400
    
    user_message = data['message'].lower().strip()
    
    # Simple response logic
    if any(greeting in user_message for greeting in ['hi', 'hello', 'hey']):
        response = "Hello! Welcome to Citizen AI. I'm here to help you with any questions about city services, community programs, or local government information in Kakinada. How can I assist you today?"
    elif 'office hours' in user_message or 'municipal corporation' in user_message:
        response = "Kakinada Municipal Corporation office is open Monday through Friday from 10:00 AM to 5:00 PM, with a lunch break from 1:00 PM to 2:00 PM. Saturday hours are 10:00 AM to 2:00 PM. We are closed on Sundays and public holidays."
    elif 'street light' in user_message or 'streetlight' in user_message:
        response = "You can report a broken or out street light by calling the Kakinada Municipal Corporation at 0884-2372345, or visit the Electrical Department at the Municipal Office. Most street light repairs are completed within 5-7 business days."
    elif 'water bill' in user_message or 'utility bill' in user_message:
        response = "You can pay your Kakinada water bill online through AP Water Portal, at Municipal Corporation office, or at authorized collection centers. Bills are issued monthly and due within 15 days of issue."
    elif 'thank' in user_message:
        response = "You're very welcome! I'm glad I could help. If you have any other questions about Kakinada city services, please don't hesitate to ask. Have a great day!"
    else:
        response = f"I understand you're asking about '{data['message']}'. For specific information about city services, please contact Kakinada Municipal Corporation at 0884-2372345 or visit the office during business hours."
    
    return jsonify({
        "response": response,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/analytics')
def analytics():
    """Get analytics data"""
    all_data = concerns_data + feedback_data
    
    # Calculate statistics
    total_submissions = len(all_data)
    concerns_count = len(concerns_data)
    feedback_count = len(feedback_data)
    
    # Sentiment distribution
    sentiment_counts = {
        'positive': len([item for item in all_data if item['sentiment'] == 'positive']),
        'negative': len([item for item in all_data if item['sentiment'] == 'negative']),
        'neutral': len([item for item in all_data if item['sentiment'] == 'neutral'])
    }
    
    # Category distribution
    categories = {}
    for item in all_data:
        category = item['category']
        categories[category] = categories.get(category, 0) + 1
    
    # Priority distribution
    priorities = {
        'high': len([item for item in all_data if item['priority'] == 'high']),
        'medium': len([item for item in all_data if item['priority'] == 'medium']),
        'low': len([item for item in all_data if item['priority'] == 'low'])
    }
    
    return jsonify({
        "total_submissions": total_submissions,
        "concerns_count": concerns_count,
        "feedback_count": feedback_count,
        "sentiment_distribution": sentiment_counts,
        "category_distribution": categories,
        "priority_distribution": priorities,
        "generated_at": datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors by serving the React app"""
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)