from fastapi import FastAPI, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import uvicorn
import asyncio
import logging
from datetime import datetime, timedelta
import json
import os
from contextlib import asynccontextmanager

# Import our custom modules
from models.database import init_db, get_db_session
from models.schemas import *
from services.ai_service import AIService
from services.sentiment_analyzer import SentimentAnalyzer
from services.text_classifier import TextClassifier
from services.notification_service import NotificationService
from utils.auth import verify_token, create_access_token
from utils.rate_limiter import RateLimiter
from utils.cache import CacheManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('citizen_ai.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Initialize services
ai_service = AIService()
sentiment_analyzer = SentimentAnalyzer()
text_classifier = TextClassifier()
notification_service = NotificationService()
rate_limiter = RateLimiter()
cache_manager = CacheManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting Citizen AI Backend...")
    await init_db()
    await ai_service.initialize()
    await cache_manager.connect()
    yield
    # Shutdown
    logger.info("Shutting down Citizen AI Backend...")
    await cache_manager.disconnect()

app = FastAPI(
    title="Citizen AI API",
    description="AI-powered citizen engagement platform",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "services": {
            "ai_service": await ai_service.health_check(),
            "database": "connected",
            "cache": await cache_manager.health_check()
        }
    }

# Authentication endpoints
@app.post("/api/v1/auth/login", response_model=TokenResponse)
async def login(credentials: LoginRequest, db=Depends(get_db_session)):
    try:
        # Authenticate user (simplified for demo)
        user = await authenticate_user(db, credentials.email, credentials.password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        access_token = create_access_token(data={"sub": user.email})
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            expires_in=3600
        )
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        raise HTTPException(status_code=500, detail="Authentication failed")

@app.post("/api/v1/auth/register", response_model=UserResponse)
async def register(user_data: UserCreateRequest, db=Depends(get_db_session)):
    try:
        # Check if user already exists
        existing_user = await get_user_by_email(db, user_data.email)
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Create new user
        user = await create_user(db, user_data)
        return UserResponse.from_orm(user)
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        raise HTTPException(status_code=500, detail="Registration failed")

# AI Chat endpoints
@app.post("/api/v1/chat/message", response_model=ChatResponse)
async def chat_message(
    request: ChatRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db_session)
):
    try:
        # Verify authentication
        user = await verify_token(credentials.credentials, db)
        
        # Rate limiting
        await rate_limiter.check_rate_limit(user.id, "chat", limit=60, window=3600)
        
        # Check cache first
        cache_key = f"chat:{hash(request.message)}"
        cached_response = await cache_manager.get(cache_key)
        if cached_response:
            return ChatResponse.parse_raw(cached_response)
        
        # Process message with AI
        ai_response = await ai_service.generate_response(
            message=request.message,
            user_id=user.id,
            context=request.context
        )
        
        # Analyze sentiment
        sentiment_result = await sentiment_analyzer.analyze(request.message)
        
        # Classify message
        classification = await text_classifier.classify(request.message)
        
        # Save conversation to database
        conversation = await save_conversation(
            db=db,
            user_id=user.id,
            message=request.message,
            response=ai_response.text,
            sentiment=sentiment_result,
            classification=classification
        )
        
        response = ChatResponse(
            id=conversation.id,
            message=ai_response.text,
            timestamp=datetime.utcnow(),
            sentiment=sentiment_result,
            classification=classification,
            confidence=ai_response.confidence
        )
        
        # Cache response
        await cache_manager.set(cache_key, response.json(), expire=3600)
        
        return response
        
    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail="Chat processing failed")

# Concern reporting endpoints
@app.post("/api/v1/concerns/", response_model=ConcernResponse)
async def create_concern(
    concern_data: ConcernCreateRequest,
    background_tasks: BackgroundTasks,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db_session)
):
    try:
        user = await verify_token(credentials.credentials, db)
        
        # Rate limiting for concern submission
        await rate_limiter.check_rate_limit(user.id, "concerns", limit=10, window=3600)
        
        # Analyze sentiment and classify
        sentiment_result = await sentiment_analyzer.analyze(concern_data.message)
        classification = await text_classifier.classify(concern_data.message)
        
        # Determine priority based on AI analysis
        priority = await ai_service.assess_priority(
            message=concern_data.message,
            sentiment=sentiment_result,
            classification=classification
        )
        
        # Create concern in database
        concern = await create_concern_record(
            db=db,
            user_id=user.id,
            concern_data=concern_data,
            sentiment=sentiment_result,
            classification=classification,
            priority=priority
        )
        
        # Background tasks
        background_tasks.add_task(
            notification_service.notify_authorities,
            concern.id,
            priority
        )
        background_tasks.add_task(
            ai_service.update_trend_analysis,
            classification.category,
            sentiment_result.sentiment
        )
        
        return ConcernResponse.from_orm(concern)
        
    except Exception as e:
        logger.error(f"Concern creation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create concern")

@app.get("/api/v1/concerns/", response_model=List[ConcernResponse])
async def get_concerns(
    skip: int = 0,
    limit: int = 100,
    category: Optional[str] = None,
    priority: Optional[str] = None,
    sentiment: Optional[str] = None,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db_session)
):
    try:
        user = await verify_token(credentials.credentials, db)
        
        # Build filters
        filters = {}
        if category:
            filters['category'] = category
        if priority:
            filters['priority'] = priority
        if sentiment:
            filters['sentiment'] = sentiment
        
        concerns = await get_concerns_list(
            db=db,
            user_id=user.id,
            skip=skip,
            limit=limit,
            filters=filters
        )
        
        return [ConcernResponse.from_orm(concern) for concern in concerns]
        
    except Exception as e:
        logger.error(f"Get concerns error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve concerns")

# Feedback endpoints
@app.post("/api/v1/feedback/", response_model=FeedbackResponse)
async def create_feedback(
    feedback_data: FeedbackCreateRequest,
    background_tasks: BackgroundTasks,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db_session)
):
    try:
        user = await verify_token(credentials.credentials, db)
        
        # Analyze sentiment
        sentiment_result = await sentiment_analyzer.analyze(feedback_data.message)
        classification = await text_classifier.classify(feedback_data.message)
        
        # Create feedback record
        feedback = await create_feedback_record(
            db=db,
            user_id=user.id,
            feedback_data=feedback_data,
            sentiment=sentiment_result,
            classification=classification
        )
        
        # Background analytics update
        background_tasks.add_task(
            ai_service.update_satisfaction_metrics,
            classification.category,
            sentiment_result.sentiment
        )
        
        return FeedbackResponse.from_orm(feedback)
        
    except Exception as e:
        logger.error(f"Feedback creation error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to create feedback")

# Analytics endpoints
@app.get("/api/v1/analytics/dashboard", response_model=DashboardAnalytics)
async def get_dashboard_analytics(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db_session)
):
    try:
        user = await verify_token(credentials.credentials, db)
        
        # Check cache first
        cache_key = f"dashboard_analytics:{user.id}"
        cached_data = await cache_manager.get(cache_key)
        if cached_data:
            return DashboardAnalytics.parse_raw(cached_data)
        
        # Generate analytics
        analytics = await ai_service.generate_dashboard_analytics(db, user.id)
        
        # Cache for 15 minutes
        await cache_manager.set(cache_key, analytics.json(), expire=900)
        
        return analytics
        
    except Exception as e:
        logger.error(f"Analytics error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate analytics")

@app.get("/api/v1/analytics/sentiment-trends", response_model=SentimentTrendsResponse)
async def get_sentiment_trends(
    days: int = 30,
    category: Optional[str] = None,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db_session)
):
    try:
        user = await verify_token(credentials.credentials, db)
        
        trends = await ai_service.analyze_sentiment_trends(
            db=db,
            days=days,
            category=category
        )
        
        return SentimentTrendsResponse(
            trends=trends,
            period_days=days,
            category=category,
            generated_at=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Sentiment trends error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to analyze sentiment trends")

# Admin endpoints
@app.get("/api/v1/admin/stats", response_model=AdminStatsResponse)
async def get_admin_stats(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db_session)
):
    try:
        user = await verify_token(credentials.credentials, db)
        
        # Check admin permissions
        if not user.is_admin:
            raise HTTPException(status_code=403, detail="Admin access required")
        
        stats = await ai_service.generate_admin_statistics(db)
        
        return AdminStatsResponse(
            total_users=stats['total_users'],
            total_concerns=stats['total_concerns'],
            total_feedback=stats['total_feedback'],
            avg_response_time=stats['avg_response_time'],
            satisfaction_score=stats['satisfaction_score'],
            top_categories=stats['top_categories'],
            recent_activity=stats['recent_activity']
        )
        
    except Exception as e:
        logger.error(f"Admin stats error: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate admin stats")

# Batch processing endpoint
@app.post("/api/v1/batch/process", response_model=BatchProcessResponse)
async def batch_process_messages(
    batch_request: BatchProcessRequest,
    background_tasks: BackgroundTasks,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db=Depends(get_db_session)
):
    try:
        user = await verify_token(credentials.credentials, db)
        
        # Check admin permissions for batch processing
        if not user.is_admin:
            raise HTTPException(status_code=403, detail="Admin access required")
        
        # Start batch processing in background
        job_id = await ai_service.start_batch_processing(
            messages=batch_request.messages,
            user_id=user.id
        )
        
        return BatchProcessResponse(
            job_id=job_id,
            status="started",
            total_messages=len(batch_request.messages),
            estimated_completion=datetime.utcnow() + timedelta(minutes=5)
        )
        
    except Exception as e:
        logger.error(f"Batch processing error: {str(e)}")
        raise HTTPException(status_code=500, detail="Batch processing failed")

# WebSocket endpoint for real-time chat
@app.websocket("/ws/chat/{user_id}")
async def websocket_chat(websocket: WebSocket, user_id: str):
    await websocket.accept()
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Process with AI
            response = await ai_service.generate_streaming_response(
                message=message_data['message'],
                user_id=user_id
            )
            
            # Send response back
            await websocket.send_text(json.dumps({
                "type": "ai_response",
                "message": response.text,
                "timestamp": datetime.utcnow().isoformat()
            }))
            
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await websocket.close()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )