from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import json
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Citizen AI API",
    description="AI-powered citizen engagement platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class MessageRequest(BaseModel):
    message: str

class ConcernRequest(BaseModel):
    message: str
    category: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    timestamp: str

class SubmissionResponse(BaseModel):
    id: str
    message: str
    category: str
    sentiment: str
    timestamp: str
    type: str
    priority: str

# In-memory storage for demo
concerns_data = []
feedback_data = []

# Sample data
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

def analyze_sentiment(text: str) -> str:
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

def categorize_message(text: str) -> str:
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

def determine_priority(sentiment: str, category: str) -> str:
    """Determine priority based on sentiment and category"""
    if sentiment == 'negative':
        if category in ['Public Safety', 'Infrastructure']:
            return 'high'
        return 'medium'
    elif sentiment == 'neutral':
        return 'medium'
    return 'low'

# Mount static files (React build)
if os.path.exists("dist"):
    app.mount("/static", StaticFiles(directory="dist"), name="static")

# API Routes
@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0"
    }

@app.post("/api/concerns", response_model=SubmissionResponse)
async def create_concern(concern: ConcernRequest):
    """Submit a new concern"""
    # Analyze the concern
    sentiment = analyze_sentiment(concern.message)
    category = categorize_message(concern.message)
    priority = determine_priority(sentiment, category)
    
    new_concern = {
        "id": str(len(concerns_data) + 1),
        "message": concern.message,
        "category": category,
        "sentiment": sentiment,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": "concern",
        "priority": priority
    }
    
    concerns_data.append(new_concern)
    logger.info(f"New concern submitted: {new_concern['id']}")
    
    return new_concern

@app.get("/api/concerns")
async def get_concerns():
    """Get all concerns"""
    return concerns_data

@app.post("/api/feedback", response_model=SubmissionResponse)
async def create_feedback(feedback: ConcernRequest):
    """Submit new feedback"""
    # Analyze the feedback
    sentiment = analyze_sentiment(feedback.message)
    category = categorize_message(feedback.message)
    priority = determine_priority(sentiment, category)
    
    new_feedback = {
        "id": str(len(feedback_data) + 1),
        "message": feedback.message,
        "category": category,
        "sentiment": sentiment,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "type": "feedback",
        "priority": priority
    }
    
    feedback_data.append(new_feedback)
    logger.info(f"New feedback submitted: {new_feedback['id']}")
    
    return new_feedback

@app.get("/api/feedback")
async def get_feedback():
    """Get all feedback"""
    return feedback_data

@app.post("/api/chat", response_model=ChatResponse)
async def chat(message_request: MessageRequest):
    """Handle chat messages"""
    user_message = message_request.message.lower().strip()
    
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
        response = f"I understand you're asking about '{message_request.message}'. For specific information about city services, please contact Kakinada Municipal Corporation at 0884-2372345 or visit the office during business hours."
    
    return ChatResponse(
        response=response,
        timestamp=datetime.now().isoformat()
    )

@app.get("/api/analytics")
async def get_analytics():
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
    
    return {
        "total_submissions": total_submissions,
        "concerns_count": concerns_count,
        "feedback_count": feedback_count,
        "sentiment_distribution": sentiment_counts,
        "category_distribution": categories,
        "priority_distribution": priorities,
        "generated_at": datetime.now().isoformat()
    }

# Serve React app
@app.get("/{full_path:path}")
async def serve_react_app(request: Request, full_path: str):
    """Serve the React app for all non-API routes"""
    if full_path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
    
    # Check if it's a static file
    if os.path.exists(f"dist/{full_path}") and full_path:
        return FileResponse(f"dist/{full_path}")
    
    # Serve index.html for all other routes (React Router)
    if os.path.exists("dist/index.html"):
        return FileResponse("dist/index.html")
    else:
        return {"message": "React app not built. Run 'npm run build' first."}

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)