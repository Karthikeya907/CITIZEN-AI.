import asyncio
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import json
import numpy as np
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    pipeline,
    AutoModelForSequenceClassification
)
import torch
from huggingface_hub import InferenceClient
import redis
from sqlalchemy.orm import Session

from models.schemas import *
from utils.config import settings

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.model_name = "ibm-granite/granite-3.3-2b-instruct"
        self.tokenizer = None
        self.model = None
        self.inference_client = None
        self.sentiment_pipeline = None
        self.classification_pipeline = None
        self.redis_client = None
        self.conversation_memory = {}
        self.model_metrics = {
            'total_requests': 0,
            'successful_requests': 0,
            'average_response_time': 0,
            'error_count': 0
        }
    
    async def initialize(self):
        """Initialize AI models and services"""
        try:
            logger.info("Initializing AI Service...")
            
            # Initialize Hugging Face Inference Client
            self.inference_client = InferenceClient(
                model=self.model_name,
                token=settings.HUGGINGFACE_API_KEY
            )
            
            # Initialize local models for faster processing
            await self._load_local_models()
            
            # Initialize Redis for caching
            self.redis_client = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                decode_responses=True
            )
            
            logger.info("AI Service initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize AI Service: {str(e)}")
            raise
    
    async def _load_local_models(self):
        """Load local models for sentiment analysis and classification"""
        try:
            # Load sentiment analysis model
            self.sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=0 if torch.cuda.is_available() else -1
            )
            
            # Load text classification model
            self.classification_pipeline = pipeline(
                "text-classification",
                model="microsoft/DialoGPT-medium",
                device=0 if torch.cuda.is_available() else -1
            )
            
            # Load tokenizer for IBM Granite model
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                trust_remote_code=True
            )
            
            logger.info("Local models loaded successfully")
            
        except Exception as e:
            logger.warning(f"Failed to load local models: {str(e)}")
            # Continue without local models, use API only
    
    async def generate_response(
        self, 
        message: str, 
        user_id: str, 
        context: Optional[Dict] = None
    ) -> AIResponse:
        """Generate AI response using IBM Granite model"""
        start_time = datetime.utcnow()
        
        try:
            self.model_metrics['total_requests'] += 1
            
            # Build conversation context
            conversation_context = await self._build_context(user_id, message, context)
            
            # Generate response using Hugging Face Inference API
            response = await self._generate_with_granite(conversation_context)
            
            # Post-process response
            processed_response = await self._post_process_response(response, message)
            
            # Update conversation memory
            await self._update_conversation_memory(user_id, message, processed_response)
            
            # Calculate response time
            response_time = (datetime.utcnow() - start_time).total_seconds()
            self._update_metrics(response_time, True)
            
            return AIResponse(
                text=processed_response,
                confidence=0.85,
                response_time=response_time,
                model_used=self.model_name
            )
            
        except Exception as e:
            logger.error(f"Error generating AI response: {str(e)}")
            self._update_metrics(0, False)
            
            # Return fallback response
            return AIResponse(
                text=self._get_fallback_response(message),
                confidence=0.1,
                response_time=0,
                model_used="fallback"
            )
    
    async def _generate_with_granite(self, context: str) -> str:
        """Generate response using IBM Granite model"""
        try:
            # Use Hugging Face Inference API
            response = await asyncio.to_thread(
                self.inference_client.text_generation,
                prompt=context,
                max_new_tokens=512,
                temperature=0.7,
                top_p=0.9,
                do_sample=True,
                repetition_penalty=1.1,
                stop_sequences=["Human:", "Assistant:", "\n\n"]
            )
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"Granite model generation error: {str(e)}")
            raise
    
    async def _build_context(
        self, 
        user_id: str, 
        message: str, 
        context: Optional[Dict] = None
    ) -> str:
        """Build conversation context for AI model"""
        
        # System prompt for Citizen AI
        system_prompt = """You are a helpful AI assistant for Citizen AI, a platform that helps citizens interact with their local government and community services. You should:

1. Be helpful, friendly, and professional
2. Provide information about city services, government processes, and community programs
3. Help citizens understand how to report concerns or access services
4. If you don't know specific local information, suggest they contact Municipal Corporation
5. Keep responses concise but informative
6. Always be respectful and supportive of citizen needs

You can help with topics like:
- Municipal Corporation office hours and contact information
- How to report issues (potholes, streetlights, drainage, etc.)
- Parking regulations and transportation
- Utility services and bill payments
- Permits and licenses
- Waste management and sanitation schedules
- General city services and programs
- Community programs and welfare schemes

"""
        
        # Get conversation history
        history = await self._get_conversation_history(user_id)
        
        # Build context string
        context_parts = [system_prompt]
        
        # Add conversation history
        for entry in history[-5:]:  # Last 5 exchanges
            context_parts.append(f"Human: {entry['message']}")
            context_parts.append(f"Assistant: {entry['response']}")
        
        # Add current message
        context_parts.append(f"Human: {message}")
        context_parts.append("Assistant:")
        
        return "\n".join(context_parts)
    
    async def _get_conversation_history(self, user_id: str) -> List[Dict]:
        """Get conversation history from memory/cache"""
        try:
            # Try to get from Redis cache first
            cache_key = f"conversation:{user_id}"
            cached_history = self.redis_client.get(cache_key)
            
            if cached_history:
                return json.loads(cached_history)
            
            # Return from in-memory storage
            return self.conversation_memory.get(user_id, [])
            
        except Exception as e:
            logger.error(f"Error getting conversation history: {str(e)}")
            return []
    
    async def _update_conversation_memory(
        self, 
        user_id: str, 
        message: str, 
        response: str
    ):
        """Update conversation memory"""
        try:
            # Update in-memory storage
            if user_id not in self.conversation_memory:
                self.conversation_memory[user_id] = []
            
            self.conversation_memory[user_id].append({
                'message': message,
                'response': response,
                'timestamp': datetime.utcnow().isoformat()
            })
            
            # Keep only last 10 exchanges
            if len(self.conversation_memory[user_id]) > 10:
                self.conversation_memory[user_id] = self.conversation_memory[user_id][-10:]
            
            # Update Redis cache
            cache_key = f"conversation:{user_id}"
            self.redis_client.setex(
                cache_key,
                3600,  # 1 hour expiry
                json.dumps(self.conversation_memory[user_id])
            )
            
        except Exception as e:
            logger.error(f"Error updating conversation memory: {str(e)}")
    
    async def _post_process_response(self, response: str, original_message: str) -> str:
        """Post-process AI response for quality and safety"""
        try:
            # Remove any unwanted prefixes/suffixes
            response = response.strip()
            
            # Remove system prompts that might have leaked through
            unwanted_prefixes = ["Human:", "Assistant:", "System:", "AI:"]
            for prefix in unwanted_prefixes:
                if response.startswith(prefix):
                    response = response[len(prefix):].strip()
            
            # Ensure response is not too long
            if len(response) > 1000:
                response = response[:1000] + "..."
            
            # Basic safety check - remove any potentially harmful content
            response = await self._safety_filter(response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error post-processing response: {str(e)}")
            return response
    
    async def _safety_filter(self, text: str) -> str:
        """Basic safety filter for AI responses"""
        # Remove any potentially harmful content
        harmful_patterns = [
            "personal information",
            "private data",
            "confidential",
            "password",
            "credit card"
        ]
        
        text_lower = text.lower()
        for pattern in harmful_patterns:
            if pattern in text_lower:
                return "I apologize, but I cannot provide that type of information. Please contact the appropriate authorities directly."
        
        return text
    
    def _get_fallback_response(self, message: str) -> str:
        """Get fallback response when AI fails"""
        fallback_responses = [
            "I apologize, but I'm experiencing technical difficulties. Please try again or contact Municipal Corporation directly at 0884-2372345.",
            "I'm having trouble processing your request right now. For immediate assistance, please contact the Municipal Corporation office.",
            "Sorry, I'm temporarily unable to provide a detailed response. Please contact local authorities for specific information about city services."
        ]
        
        # Simple keyword-based fallback
        message_lower = message.lower()
        if any(word in message_lower for word in ['emergency', 'urgent', 'help']):
            return "For emergency services, please call: Police (100), Fire (101), Ambulance (108). For non-emergency city services, contact Municipal Corporation at 0884-2372345."
        
        return fallback_responses[hash(message) % len(fallback_responses)]
    
    def _update_metrics(self, response_time: float, success: bool):
        """Update model performance metrics"""
        if success:
            self.model_metrics['successful_requests'] += 1
            
            # Update average response time
            total_successful = self.model_metrics['successful_requests']
            current_avg = self.model_metrics['average_response_time']
            self.model_metrics['average_response_time'] = (
                (current_avg * (total_successful - 1) + response_time) / total_successful
            )
        else:
            self.model_metrics['error_count'] += 1
    
    async def assess_priority(
        self, 
        message: str, 
        sentiment: Dict, 
        classification: Dict
    ) -> str:
        """Assess priority level of a concern using AI"""
        try:
            # Priority assessment prompt
            priority_prompt = f"""Assess the priority level of this citizen concern:

Message: "{message}"
Sentiment: {sentiment.get('sentiment', 'neutral')}
Category: {classification.get('category', 'general')}

Priority levels:
- HIGH: Safety issues, infrastructure failures, emergencies
- MEDIUM: Service disruptions, moderate concerns
- LOW: General feedback, suggestions, minor issues

Priority level:"""

            response = await self._generate_with_granite(priority_prompt)
            
            # Extract priority from response
            response_lower = response.lower()
            if 'high' in response_lower:
                return 'high'
            elif 'medium' in response_lower:
                return 'medium'
            else:
                return 'low'
                
        except Exception as e:
            logger.error(f"Error assessing priority: {str(e)}")
            # Fallback priority assessment
            if sentiment.get('sentiment') == 'negative':
                return 'medium'
            return 'low'
    
    async def generate_dashboard_analytics(self, db: Session, user_id: str) -> DashboardAnalytics:
        """Generate comprehensive dashboard analytics"""
        try:
            # This would typically query the database for real analytics
            # For demo purposes, we'll return mock data
            
            analytics = DashboardAnalytics(
                total_submissions=150,
                active_concerns=45,
                positive_feedback=85,
                average_sentiment=3.2,
                top_categories=[
                    {"category": "Infrastructure", "count": 35},
                    {"category": "Public Safety", "count": 28},
                    {"category": "Environment", "count": 22},
                    {"category": "Transportation", "count": 18}
                ],
                recent_trends={
                    "sentiment_trend": "improving",
                    "concern_volume": "stable",
                    "response_time": "decreasing"
                },
                generated_at=datetime.utcnow()
            )
            
            return analytics
            
        except Exception as e:
            logger.error(f"Error generating dashboard analytics: {str(e)}")
            raise
    
    async def analyze_sentiment_trends(
        self, 
        db: Session, 
        days: int = 30, 
        category: Optional[str] = None
    ) -> List[Dict]:
        """Analyze sentiment trends over time"""
        try:
            # Mock trend data - in real implementation, this would query the database
            trends = []
            base_date = datetime.utcnow() - timedelta(days=days)
            
            for i in range(days):
                date = base_date + timedelta(days=i)
                trends.append({
                    "date": date.isoformat(),
                    "positive": np.random.randint(5, 20),
                    "neutral": np.random.randint(10, 30),
                    "negative": np.random.randint(2, 15),
                    "average_score": np.random.uniform(2.5, 4.5)
                })
            
            return trends
            
        except Exception as e:
            logger.error(f"Error analyzing sentiment trends: {str(e)}")
            return []
    
    async def generate_admin_statistics(self, db: Session) -> Dict[str, Any]:
        """Generate comprehensive admin statistics"""
        try:
            # Mock admin statistics
            stats = {
                "total_users": 1250,
                "total_concerns": 450,
                "total_feedback": 320,
                "avg_response_time": 2.3,
                "satisfaction_score": 4.1,
                "top_categories": [
                    {"name": "Infrastructure", "count": 125, "percentage": 27.8},
                    {"name": "Public Safety", "count": 98, "percentage": 21.8},
                    {"name": "Environment", "count": 76, "percentage": 16.9}
                ],
                "recent_activity": [
                    {"type": "concern", "count": 15, "date": "today"},
                    {"type": "feedback", "count": 8, "date": "today"},
                    {"type": "resolved", "count": 12, "date": "today"}
                ]
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Error generating admin statistics: {str(e)}")
            return {}
    
    async def start_batch_processing(
        self, 
        messages: List[str], 
        user_id: str
    ) -> str:
        """Start batch processing of multiple messages"""
        try:
            job_id = f"batch_{user_id}_{int(datetime.utcnow().timestamp())}"
            
            # Store batch job in Redis
            job_data = {
                "job_id": job_id,
                "user_id": user_id,
                "messages": messages,
                "status": "processing",
                "created_at": datetime.utcnow().isoformat(),
                "total_messages": len(messages),
                "processed_messages": 0
            }
            
            self.redis_client.setex(
                f"batch_job:{job_id}",
                3600,  # 1 hour expiry
                json.dumps(job_data)
            )
            
            # Start background processing
            asyncio.create_task(self._process_batch_messages(job_id, messages, user_id))
            
            return job_id
            
        except Exception as e:
            logger.error(f"Error starting batch processing: {str(e)}")
            raise
    
    async def _process_batch_messages(
        self, 
        job_id: str, 
        messages: List[str], 
        user_id: str
    ):
        """Process batch messages in background"""
        try:
            results = []
            
            for i, message in enumerate(messages):
                try:
                    # Process each message
                    response = await self.generate_response(message, user_id)
                    results.append({
                        "message": message,
                        "response": response.text,
                        "confidence": response.confidence,
                        "processed_at": datetime.utcnow().isoformat()
                    })
                    
                    # Update job progress
                    await self._update_batch_job_progress(job_id, i + 1, len(messages))
                    
                except Exception as e:
                    logger.error(f"Error processing batch message {i}: {str(e)}")
                    results.append({
                        "message": message,
                        "error": str(e),
                        "processed_at": datetime.utcnow().isoformat()
                    })
            
            # Mark job as completed
            await self._complete_batch_job(job_id, results)
            
        except Exception as e:
            logger.error(f"Error in batch processing: {str(e)}")
            await self._fail_batch_job(job_id, str(e))
    
    async def _update_batch_job_progress(
        self, 
        job_id: str, 
        processed: int, 
        total: int
    ):
        """Update batch job progress"""
        try:
            job_key = f"batch_job:{job_id}"
            job_data = json.loads(self.redis_client.get(job_key) or "{}")
            
            job_data.update({
                "processed_messages": processed,
                "progress_percentage": (processed / total) * 100,
                "updated_at": datetime.utcnow().isoformat()
            })
            
            self.redis_client.setex(job_key, 3600, json.dumps(job_data))
            
        except Exception as e:
            logger.error(f"Error updating batch job progress: {str(e)}")
    
    async def _complete_batch_job(self, job_id: str, results: List[Dict]):
        """Mark batch job as completed"""
        try:
            job_key = f"batch_job:{job_id}"
            job_data = json.loads(self.redis_client.get(job_key) or "{}")
            
            job_data.update({
                "status": "completed",
                "results": results,
                "completed_at": datetime.utcnow().isoformat()
            })
            
            self.redis_client.setex(job_key, 3600, json.dumps(job_data))
            
        except Exception as e:
            logger.error(f"Error completing batch job: {str(e)}")
    
    async def _fail_batch_job(self, job_id: str, error: str):
        """Mark batch job as failed"""
        try:
            job_key = f"batch_job:{job_id}"
            job_data = json.loads(self.redis_client.get(job_key) or "{}")
            
            job_data.update({
                "status": "failed",
                "error": error,
                "failed_at": datetime.utcnow().isoformat()
            })
            
            self.redis_client.setex(job_key, 3600, json.dumps(job_data))
            
        except Exception as e:
            logger.error(f"Error failing batch job: {str(e)}")
    
    async def generate_streaming_response(
        self, 
        message: str, 
        user_id: str
    ) -> AIResponse:
        """Generate streaming response for WebSocket connections"""
        try:
            # For streaming, we'll generate the full response and then stream it
            response = await self.generate_response(message, user_id)
            return response
            
        except Exception as e:
            logger.error(f"Error generating streaming response: {str(e)}")
            return AIResponse(
                text=self._get_fallback_response(message),
                confidence=0.1,
                response_time=0,
                model_used="fallback"
            )
    
    async def update_trend_analysis(self, category: str, sentiment: str):
        """Update trend analysis data"""
        try:
            # Update trend data in Redis
            trend_key = f"trends:{category}:{sentiment}"
            current_count = int(self.redis_client.get(trend_key) or 0)
            self.redis_client.setex(trend_key, 86400, current_count + 1)  # 24 hour expiry
            
        except Exception as e:
            logger.error(f"Error updating trend analysis: {str(e)}")
    
    async def update_satisfaction_metrics(self, category: str, sentiment: str):
        """Update satisfaction metrics"""
        try:
            # Update satisfaction metrics in Redis
            metric_key = f"satisfaction:{category}"
            
            # Get current metrics
            current_data = self.redis_client.get(metric_key)
            if current_data:
                metrics = json.loads(current_data)
            else:
                metrics = {"total": 0, "positive": 0, "negative": 0, "neutral": 0}
            
            # Update metrics
            metrics["total"] += 1
            metrics[sentiment] += 1
            
            # Store updated metrics
            self.redis_client.setex(metric_key, 86400, json.dumps(metrics))
            
        except Exception as e:
            logger.error(f"Error updating satisfaction metrics: {str(e)}")
    
    async def health_check(self) -> str:
        """Check AI service health"""
        try:
            # Test basic functionality
            test_response = await self.generate_response("test", "health_check")
            
            if test_response.text:
                return "healthy"
            else:
                return "degraded"
                
        except Exception as e:
            logger.error(f"AI service health check failed: {str(e)}")
            return "unhealthy"
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current model metrics"""
        return self.model_metrics.copy()