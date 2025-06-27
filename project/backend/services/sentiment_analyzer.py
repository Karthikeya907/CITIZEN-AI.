import asyncio
import logging
from typing import Dict, List, Optional, Tuple
import numpy as np
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from textblob import TextBlob
import re
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class SentimentAnalyzer:
    def __init__(self):
        self.model_name = "cardiffnlp/twitter-roberta-base-sentiment-latest"
        self.pipeline = None
        self.tokenizer = None
        self.model = None
        self.emotion_model = None
        self.language_detector = None
        self.cache = {}
        
        # Sentiment thresholds
        self.thresholds = {
            'positive': 0.6,
            'negative': 0.6,
            'neutral': 0.4
        }
        
        # Emotion categories
        self.emotion_categories = [
            'joy', 'sadness', 'anger', 'fear', 'surprise', 'disgust',
            'trust', 'anticipation', 'frustration', 'satisfaction'
        ]
        
        # Context-aware keywords for government/civic domain
        self.civic_keywords = {
            'infrastructure': ['road', 'bridge', 'water', 'electricity', 'drainage', 'streetlight'],
            'safety': ['police', 'crime', 'security', 'emergency', 'fire', 'accident'],
            'environment': ['pollution', 'waste', 'garbage', 'clean', 'green', 'park'],
            'transport': ['bus', 'traffic', 'parking', 'vehicle', 'route', 'station'],
            'health': ['hospital', 'clinic', 'doctor', 'medicine', 'health', 'treatment'],
            'education': ['school', 'college', 'teacher', 'student', 'education', 'library']
        }
        
    async def initialize(self):
        """Initialize sentiment analysis models"""
        try:
            logger.info("Initializing Sentiment Analyzer...")
            
            # Load main sentiment analysis pipeline
            self.pipeline = pipeline(
                "sentiment-analysis",
                model=self.model_name,
                tokenizer=self.model_name,
                device=0 if torch.cuda.is_available() else -1,
                return_all_scores=True
            )
            
            # Load tokenizer and model separately for advanced processing
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            
            # Load emotion detection model
            self.emotion_model = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                device=0 if torch.cuda.is_available() else -1,
                return_all_scores=True
            )
            
            logger.info("Sentiment Analyzer initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Sentiment Analyzer: {str(e)}")
            # Initialize fallback methods
            await self._initialize_fallback()
    
    async def _initialize_fallback(self):
        """Initialize fallback sentiment analysis methods"""
        logger.info("Initializing fallback sentiment analysis...")
        # TextBlob will be used as fallback
        
    async def analyze(self, text: str, context: Optional[Dict] = None) -> Dict:
        """
        Comprehensive sentiment analysis with multiple approaches
        """
        try:
            # Check cache first
            cache_key = hash(text)
            if cache_key in self.cache:
                return self.cache[cache_key]
            
            # Preprocess text
            cleaned_text = await self._preprocess_text(text)
            
            # Multi-model sentiment analysis
            results = await self._multi_model_analysis(cleaned_text)
            
            # Context-aware adjustment
            if context:
                results = await self._context_aware_adjustment(results, context)
            
            # Civic domain specific analysis
            civic_analysis = await self._civic_domain_analysis(cleaned_text)
            results.update(civic_analysis)
            
            # Emotion detection
            emotions = await self._detect_emotions(cleaned_text)
            results['emotions'] = emotions
            
            # Confidence scoring
            results['confidence'] = await self._calculate_confidence(results)
            
            # Cache results
            self.cache[cache_key] = results
            
            return results
            
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {str(e)}")
            return await self._fallback_analysis(text)
    
    async def _preprocess_text(self, text: str) -> str:
        """Preprocess text for better sentiment analysis"""
        try:
            # Remove URLs
            text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
            
            # Remove email addresses
            text = re.sub(r'\S+@\S+', '', text)
            
            # Remove phone numbers
            text = re.sub(r'\b\d{10}\b|\b\d{3}-\d{3}-\d{4}\b', '', text)
            
            # Normalize whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Handle negations properly
            text = re.sub(r"n't", " not", text)
            text = re.sub(r"won't", "will not", text)
            text = re.sub(r"can't", "cannot", text)
            
            return text
            
        except Exception as e:
            logger.error(f"Error preprocessing text: {str(e)}")
            return text
    
    async def _multi_model_analysis(self, text: str) -> Dict:
        """Perform sentiment analysis using multiple models"""
        results = {}
        
        try:
            # Primary model (RoBERTa-based)
            if self.pipeline:
                primary_result = await asyncio.to_thread(self.pipeline, text)
                results['primary'] = self._process_pipeline_result(primary_result[0])
            
            # TextBlob analysis (rule-based)
            blob = TextBlob(text)
            textblob_sentiment = blob.sentiment
            results['textblob'] = {
                'polarity': textblob_sentiment.polarity,
                'subjectivity': textblob_sentiment.subjectivity,
                'sentiment': self._polarity_to_sentiment(textblob_sentiment.polarity)
            }
            
            # Lexicon-based analysis
            lexicon_result = await self._lexicon_based_analysis(text)
            results['lexicon'] = lexicon_result
            
            # Ensemble result
            results['ensemble'] = await self._ensemble_sentiment(results)
            
            return results
            
        except Exception as e:
            logger.error(f"Error in multi-model analysis: {str(e)}")
            return {'ensemble': {'sentiment': 'neutral', 'confidence': 0.1}}
    
    def _process_pipeline_result(self, result: List[Dict]) -> Dict:
        """Process pipeline result to standard format"""
        try:
            # Find the highest scoring sentiment
            best_result = max(result, key=lambda x: x['score'])
            
            return {
                'sentiment': best_result['label'].lower(),
                'confidence': best_result['score'],
                'all_scores': {item['label'].lower(): item['score'] for item in result}
            }
            
        except Exception as e:
            logger.error(f"Error processing pipeline result: {str(e)}")
            return {'sentiment': 'neutral', 'confidence': 0.1}
    
    def _polarity_to_sentiment(self, polarity: float) -> str:
        """Convert polarity score to sentiment label"""
        if polarity > 0.1:
            return 'positive'
        elif polarity < -0.1:
            return 'negative'
        else:
            return 'neutral'
    
    async def _lexicon_based_analysis(self, text: str) -> Dict:
        """Perform lexicon-based sentiment analysis"""
        try:
            # Simple lexicon-based approach
            positive_words = [
                'good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic',
                'awesome', 'brilliant', 'outstanding', 'perfect', 'satisfied',
                'happy', 'pleased', 'delighted', 'impressed', 'grateful'
            ]
            
            negative_words = [
                'bad', 'terrible', 'awful', 'horrible', 'disgusting', 'hate',
                'angry', 'frustrated', 'disappointed', 'annoyed', 'upset',
                'broken', 'damaged', 'problem', 'issue', 'complaint', 'poor'
            ]
            
            words = text.lower().split()
            positive_count = sum(1 for word in words if word in positive_words)
            negative_count = sum(1 for word in words if word in negative_words)
            
            total_sentiment_words = positive_count + negative_count
            
            if total_sentiment_words == 0:
                return {'sentiment': 'neutral', 'confidence': 0.5, 'positive_count': 0, 'negative_count': 0}
            
            positive_ratio = positive_count / total_sentiment_words
            negative_ratio = negative_count / total_sentiment_words
            
            if positive_ratio > negative_ratio:
                sentiment = 'positive'
                confidence = positive_ratio
            elif negative_ratio > positive_ratio:
                sentiment = 'negative'
                confidence = negative_ratio
            else:
                sentiment = 'neutral'
                confidence = 0.5
            
            return {
                'sentiment': sentiment,
                'confidence': confidence,
                'positive_count': positive_count,
                'negative_count': negative_count
            }
            
        except Exception as e:
            logger.error(f"Error in lexicon-based analysis: {str(e)}")
            return {'sentiment': 'neutral', 'confidence': 0.1}
    
    async def _ensemble_sentiment(self, results: Dict) -> Dict:
        """Combine multiple sentiment analysis results"""
        try:
            sentiments = []
            confidences = []
            
            # Collect sentiments and confidences from different models
            for model_name, result in results.items():
                if isinstance(result, dict) and 'sentiment' in result:
                    sentiments.append(result['sentiment'])
                    confidences.append(result.get('confidence', 0.5))
            
            if not sentiments:
                return {'sentiment': 'neutral', 'confidence': 0.1}
            
            # Weighted voting based on confidence
            sentiment_scores = {'positive': 0, 'negative': 0, 'neutral': 0}
            
            for sentiment, confidence in zip(sentiments, confidences):
                sentiment_scores[sentiment] += confidence
            
            # Find the sentiment with highest weighted score
            best_sentiment = max(sentiment_scores, key=sentiment_scores.get)
            total_score = sum(sentiment_scores.values())
            ensemble_confidence = sentiment_scores[best_sentiment] / total_score if total_score > 0 else 0.1
            
            return {
                'sentiment': best_sentiment,
                'confidence': ensemble_confidence,
                'scores': sentiment_scores,
                'model_agreement': len(set(sentiments)) == 1
            }
            
        except Exception as e:
            logger.error(f"Error in ensemble sentiment: {str(e)}")
            return {'sentiment': 'neutral', 'confidence': 0.1}
    
    async def _context_aware_adjustment(self, results: Dict, context: Dict) -> Dict:
        """Adjust sentiment based on context"""
        try:
            # Adjust based on user history, time of day, etc.
            adjustment_factor = 1.0
            
            # If user has history of negative experiences, slightly adjust
            if context.get('user_history_sentiment') == 'negative':
                adjustment_factor *= 0.9
            elif context.get('user_history_sentiment') == 'positive':
                adjustment_factor *= 1.1
            
            # Time-based adjustments (people might be more negative during certain hours)
            current_hour = datetime.now().hour
            if 22 <= current_hour or current_hour <= 6:  # Late night/early morning
                if results['ensemble']['sentiment'] == 'negative':
                    adjustment_factor *= 1.1
            
            # Apply adjustment
            if 'ensemble' in results:
                results['ensemble']['confidence'] *= adjustment_factor
                results['context_adjusted'] = True
            
            return results
            
        except Exception as e:
            logger.error(f"Error in context-aware adjustment: {str(e)}")
            return results
    
    async def _civic_domain_analysis(self, text: str) -> Dict:
        """Analyze sentiment in civic/government domain context"""
        try:
            civic_analysis = {
                'domain_relevance': {},
                'urgency_indicators': [],
                'satisfaction_indicators': []
            }
            
            text_lower = text.lower()
            
            # Check domain relevance
            for domain, keywords in self.civic_keywords.items():
                relevance_score = sum(1 for keyword in keywords if keyword in text_lower)
                if relevance_score > 0:
                    civic_analysis['domain_relevance'][domain] = relevance_score
            
            # Check for urgency indicators
            urgency_keywords = [
                'urgent', 'emergency', 'immediate', 'asap', 'critical',
                'dangerous', 'broken', 'not working', 'failed', 'stopped'
            ]
            
            for keyword in urgency_keywords:
                if keyword in text_lower:
                    civic_analysis['urgency_indicators'].append(keyword)
            
            # Check for satisfaction indicators
            satisfaction_keywords = [
                'thank you', 'appreciate', 'grateful', 'excellent service',
                'well done', 'impressed', 'satisfied', 'good job'
            ]
            
            for keyword in satisfaction_keywords:
                if keyword in text_lower:
                    civic_analysis['satisfaction_indicators'].append(keyword)
            
            # Calculate civic sentiment modifier
            urgency_count = len(civic_analysis['urgency_indicators'])
            satisfaction_count = len(civic_analysis['satisfaction_indicators'])
            
            civic_analysis['civic_sentiment_modifier'] = satisfaction_count - urgency_count
            
            return civic_analysis
            
        except Exception as e:
            logger.error(f"Error in civic domain analysis: {str(e)}")
            return {}
    
    async def _detect_emotions(self, text: str) -> Dict:
        """Detect emotions in the text"""
        try:
            if self.emotion_model:
                emotion_result = await asyncio.to_thread(self.emotion_model, text)
                
                # Process emotion results
                emotions = {}
                for emotion_data in emotion_result[0]:
                    emotions[emotion_data['label']] = emotion_data['score']
                
                # Find dominant emotion
                dominant_emotion = max(emotions, key=emotions.get)
                
                return {
                    'dominant_emotion': dominant_emotion,
                    'emotion_scores': emotions,
                    'emotion_confidence': emotions[dominant_emotion]
                }
            else:
                # Fallback emotion detection
                return await self._fallback_emotion_detection(text)
                
        except Exception as e:
            logger.error(f"Error in emotion detection: {str(e)}")
            return await self._fallback_emotion_detection(text)
    
    async def _fallback_emotion_detection(self, text: str) -> Dict:
        """Fallback emotion detection using keyword matching"""
        try:
            emotion_keywords = {
                'joy': ['happy', 'glad', 'pleased', 'delighted', 'cheerful'],
                'anger': ['angry', 'mad', 'furious', 'annoyed', 'irritated'],
                'sadness': ['sad', 'disappointed', 'upset', 'depressed'],
                'fear': ['scared', 'afraid', 'worried', 'anxious', 'concerned'],
                'surprise': ['surprised', 'shocked', 'amazed', 'astonished'],
                'disgust': ['disgusted', 'revolted', 'appalled', 'horrified']
            }
            
            text_lower = text.lower()
            emotion_scores = {}
            
            for emotion, keywords in emotion_keywords.items():
                score = sum(1 for keyword in keywords if keyword in text_lower)
                if score > 0:
                    emotion_scores[emotion] = score / len(keywords)
            
            if emotion_scores:
                dominant_emotion = max(emotion_scores, key=emotion_scores.get)
                return {
                    'dominant_emotion': dominant_emotion,
                    'emotion_scores': emotion_scores,
                    'emotion_confidence': emotion_scores[dominant_emotion]
                }
            else:
                return {
                    'dominant_emotion': 'neutral',
                    'emotion_scores': {'neutral': 1.0},
                    'emotion_confidence': 1.0
                }
                
        except Exception as e:
            logger.error(f"Error in fallback emotion detection: {str(e)}")
            return {'dominant_emotion': 'neutral', 'emotion_scores': {}, 'emotion_confidence': 0.1}
    
    async def _calculate_confidence(self, results: Dict) -> float:
        """Calculate overall confidence score"""
        try:
            confidences = []
            
            # Collect confidence scores from different analyses
            if 'ensemble' in results:
                confidences.append(results['ensemble'].get('confidence', 0.5))
            
            if 'emotions' in results:
                confidences.append(results['emotions'].get('emotion_confidence', 0.5))
            
            # Model agreement bonus
            if results.get('ensemble', {}).get('model_agreement', False):
                agreement_bonus = 0.1
            else:
                agreement_bonus = 0.0
            
            # Calculate weighted average
            if confidences:
                base_confidence = sum(confidences) / len(confidences)
                return min(1.0, base_confidence + agreement_bonus)
            else:
                return 0.1
                
        except Exception as e:
            logger.error(f"Error calculating confidence: {str(e)}")
            return 0.1
    
    async def _fallback_analysis(self, text: str) -> Dict:
        """Fallback sentiment analysis when main models fail"""
        try:
            # Use TextBlob as fallback
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            sentiment = self._polarity_to_sentiment(polarity)
            confidence = abs(polarity) if abs(polarity) > 0.1 else 0.1
            
            return {
                'sentiment': sentiment,
                'confidence': confidence,
                'polarity': polarity,
                'subjectivity': blob.sentiment.subjectivity,
                'fallback_used': True
            }
            
        except Exception as e:
            logger.error(f"Error in fallback analysis: {str(e)}")
            return {
                'sentiment': 'neutral',
                'confidence': 0.1,
                'error': str(e),
                'fallback_used': True
            }
    
    async def batch_analyze(self, texts: List[str]) -> List[Dict]:
        """Analyze sentiment for multiple texts"""
        try:
            results = []
            
            # Process in batches to avoid memory issues
            batch_size = 32
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                batch_results = await asyncio.gather(
                    *[self.analyze(text) for text in batch],
                    return_exceptions=True
                )
                
                for result in batch_results:
                    if isinstance(result, Exception):
                        results.append(await self._fallback_analysis(""))
                    else:
                        results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Error in batch analysis: {str(e)}")
            return [await self._fallback_analysis("") for _ in texts]
    
    def get_sentiment_summary(self, analyses: List[Dict]) -> Dict:
        """Generate summary statistics from multiple sentiment analyses"""
        try:
            if not analyses:
                return {}
            
            sentiments = [analysis.get('sentiment', 'neutral') for analysis in analyses]
            confidences = [analysis.get('confidence', 0.1) for analysis in analyses]
            
            sentiment_counts = {
                'positive': sentiments.count('positive'),
                'negative': sentiments.count('negative'),
                'neutral': sentiments.count('neutral')
            }
            
            total = len(sentiments)
            sentiment_percentages = {
                sentiment: (count / total) * 100 
                for sentiment, count in sentiment_counts.items()
            }
            
            avg_confidence = sum(confidences) / len(confidences)
            
            # Overall sentiment based on weighted average
            positive_weight = sentiment_counts['positive'] * 1
            negative_weight = sentiment_counts['negative'] * -1
            neutral_weight = sentiment_counts['neutral'] * 0
            
            overall_score = (positive_weight + negative_weight + neutral_weight) / total
            
            if overall_score > 0.1:
                overall_sentiment = 'positive'
            elif overall_score < -0.1:
                overall_sentiment = 'negative'
            else:
                overall_sentiment = 'neutral'
            
            return {
                'total_analyzed': total,
                'sentiment_counts': sentiment_counts,
                'sentiment_percentages': sentiment_percentages,
                'overall_sentiment': overall_sentiment,
                'overall_score': overall_score,
                'average_confidence': avg_confidence,
                'generated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating sentiment summary: {str(e)}")
            return {}
    
    def clear_cache(self):
        """Clear the analysis cache"""
        self.cache.clear()
        logger.info("Sentiment analysis cache cleared")