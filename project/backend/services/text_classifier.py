import asyncio
import logging
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
import pickle
import re
from datetime import datetime
import json

logger = logging.getLogger(__name__)

class TextClassifier:
    def __init__(self):
        self.model_name = "microsoft/DialoGPT-medium"
        self.classification_pipeline = None
        self.tokenizer = None
        self.model = None
        self.custom_classifier = None
        self.tfidf_vectorizer = None
        self.cache = {}
        
        # Predefined categories for citizen concerns
        self.categories = {
            'Infrastructure': {
                'keywords': [
                    'road', 'bridge', 'water', 'electricity', 'power', 'sewer',
                    'drainage', 'streetlight', 'pothole', 'construction',
                    'maintenance', 'repair', 'broken', 'damaged', 'pipeline'
                ],
                'priority_keywords': ['emergency', 'urgent', 'dangerous', 'broken'],
                'description': 'Issues related to city infrastructure and utilities'
            },
            'Public Safety': {
                'keywords': [
                    'police', 'crime', 'safety', 'security', 'theft', 'violence',
                    'emergency', 'fire', 'accident', 'patrol', 'law', 'order',
                    'harassment', 'assault', 'robbery', 'vandalism'
                ],
                'priority_keywords': ['emergency', 'urgent', 'dangerous', 'crime'],
                'description': 'Public safety and security concerns'
            },
            'Environment': {
                'keywords': [
                    'pollution', 'waste', 'garbage', 'trash', 'recycling',
                    'clean', 'dirty', 'smell', 'air', 'water', 'noise',
                    'park', 'green', 'tree', 'environment', 'sanitation'
                ],
                'priority_keywords': ['pollution', 'contamination', 'health hazard'],
                'description': 'Environmental and sanitation issues'
            },
            'Transportation': {
                'keywords': [
                    'bus', 'transport', 'traffic', 'parking', 'vehicle',
                    'route', 'station', 'road', 'signal', 'congestion',
                    'auto', 'taxi', 'rickshaw', 'bicycle', 'pedestrian'
                ],
                'priority_keywords': ['accident', 'blocked', 'emergency'],
                'description': 'Transportation and traffic related issues'
            },
            'Healthcare': {
                'keywords': [
                    'hospital', 'clinic', 'doctor', 'medicine', 'health',
                    'treatment', 'patient', 'medical', 'ambulance',
                    'emergency', 'disease', 'vaccination', 'pharmacy'
                ],
                'priority_keywords': ['emergency', 'urgent', 'critical', 'life threatening'],
                'description': 'Healthcare and medical services'
            },
            'Education': {
                'keywords': [
                    'school', 'college', 'university', 'teacher', 'student',
                    'education', 'library', 'book', 'class', 'exam',
                    'admission', 'fee', 'scholarship', 'learning'
                ],
                'priority_keywords': ['urgent', 'exam', 'admission'],
                'description': 'Education and learning related issues'
            },
            'Digital Services': {
                'keywords': [
                    'website', 'online', 'app', 'digital', 'internet',
                    'computer', 'system', 'portal', 'login', 'password',
                    'technical', 'software', 'wifi', 'connection'
                ],
                'priority_keywords': ['not working', 'down', 'error'],
                'description': 'Digital services and technology issues'
            },
            'General': {
                'keywords': [
                    'complaint', 'suggestion', 'feedback', 'service',
                    'help', 'support', 'information', 'question',
                    'request', 'application', 'form', 'office'
                ],
                'priority_keywords': ['urgent', 'important'],
                'description': 'General inquiries and feedback'
            }
        }
        
        # Subcategories for more detailed classification
        self.subcategories = {
            'Infrastructure': [
                'Road Maintenance', 'Water Supply', 'Electricity', 'Drainage',
                'Street Lighting', 'Construction', 'Utilities'
            ],
            'Public Safety': [
                'Police Services', 'Fire Safety', 'Emergency Response',
                'Crime Prevention', 'Traffic Safety', 'Security'
            ],
            'Environment': [
                'Waste Management', 'Air Pollution', 'Water Pollution',
                'Noise Pollution', 'Sanitation', 'Parks and Recreation'
            ],
            'Transportation': [
                'Public Transport', 'Traffic Management', 'Parking',
                'Road Safety', 'Vehicle Registration', 'Route Planning'
            ],
            'Healthcare': [
                'Hospital Services', 'Emergency Medical', 'Public Health',
                'Vaccination', 'Medical Facilities', 'Health Insurance'
            ],
            'Education': [
                'School Administration', 'Higher Education', 'Libraries',
                'Educational Programs', 'Student Services', 'Scholarships'
            ],
            'Digital Services': [
                'Government Portals', 'Online Applications', 'Technical Support',
                'Digital Payments', 'E-Governance', 'Internet Services'
            ],
            'General': [
                'Customer Service', 'Information Request', 'Complaints',
                'Suggestions', 'Administrative', 'Miscellaneous'
            ]
        }
        
        # Priority levels
        self.priority_levels = {
            'high': ['emergency', 'urgent', 'critical', 'dangerous', 'life threatening'],
            'medium': ['important', 'soon', 'needed', 'problem', 'issue'],
            'low': ['suggestion', 'feedback', 'information', 'general', 'minor']
        }
    
    async def initialize(self):
        """Initialize text classification models"""
        try:
            logger.info("Initializing Text Classifier...")
            
            # Load pre-trained classification pipeline
            self.classification_pipeline = pipeline(
                "text-classification",
                model="facebook/bart-large-mnli",
                device=0 if torch.cuda.is_available() else -1
            )
            
            # Initialize custom classifier
            await self._initialize_custom_classifier()
            
            # Load or train TF-IDF vectorizer
            await self._initialize_tfidf_classifier()
            
            logger.info("Text Classifier initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize Text Classifier: {str(e)}")
            # Continue with keyword-based classification as fallback
    
    async def _initialize_custom_classifier(self):
        """Initialize custom classification model"""
        try:
            # This would typically load a pre-trained model
            # For demo purposes, we'll use a simple approach
            self.custom_classifier = MultinomialNB()
            
            # In a real implementation, you would load training data and train the model
            # For now, we'll rely on keyword-based classification
            
        except Exception as e:
            logger.error(f"Error initializing custom classifier: {str(e)}")
    
    async def _initialize_tfidf_classifier(self):
        """Initialize TF-IDF based classifier"""
        try:
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=5000,
                stop_words='english',
                ngram_range=(1, 2),
                lowercase=True
            )
            
            # In a real implementation, you would fit this on training data
            
        except Exception as e:
            logger.error(f"Error initializing TF-IDF classifier: {str(e)}")
    
    async def classify(self, text: str, context: Optional[Dict] = None) -> Dict:
        """
        Comprehensive text classification
        """
        try:
            # Check cache first
            cache_key = hash(text)
            if cache_key in self.cache:
                return self.cache[cache_key]
            
            # Preprocess text
            cleaned_text = await self._preprocess_text(text)
            
            # Multi-approach classification
            results = await self._multi_approach_classification(cleaned_text)
            
            # Context-aware adjustment
            if context:
                results = await self._context_aware_classification(results, context)
            
            # Priority assessment
            results['priority'] = await self._assess_priority(cleaned_text, results)
            
            # Urgency scoring
            results['urgency_score'] = await self._calculate_urgency_score(cleaned_text, results)
            
            # Subcategory classification
            results['subcategory'] = await self._classify_subcategory(
                cleaned_text, results.get('category', 'General')
            )
            
            # Confidence calculation
            results['confidence'] = await self._calculate_classification_confidence(results)
            
            # Cache results
            self.cache[cache_key] = results
            
            return results
            
        except Exception as e:
            logger.error(f"Error in text classification: {str(e)}")
            return await self._fallback_classification(text)
    
    async def _preprocess_text(self, text: str) -> str:
        """Preprocess text for classification"""
        try:
            # Convert to lowercase
            text = text.lower()
            
            # Remove special characters but keep spaces
            text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
            
            # Remove extra whitespace
            text = re.sub(r'\s+', ' ', text).strip()
            
            # Remove very short words (less than 2 characters)
            words = text.split()
            words = [word for word in words if len(word) >= 2]
            
            return ' '.join(words)
            
        except Exception as e:
            logger.error(f"Error preprocessing text: {str(e)}")
            return text
    
    async def _multi_approach_classification(self, text: str) -> Dict:
        """Use multiple approaches for classification"""
        results = {}
        
        try:
            # Keyword-based classification (primary)
            keyword_result = await self._keyword_based_classification(text)
            results['keyword_based'] = keyword_result
            
            # ML-based classification (if available)
            if self.classification_pipeline:
                ml_result = await self._ml_based_classification(text)
                results['ml_based'] = ml_result
            
            # Rule-based classification
            rule_result = await self._rule_based_classification(text)
            results['rule_based'] = rule_result
            
            # Ensemble classification
            results['ensemble'] = await self._ensemble_classification(results)
            
            return results
            
        except Exception as e:
            logger.error(f"Error in multi-approach classification: {str(e)}")
            return {'ensemble': {'category': 'General', 'confidence': 0.1}}
    
    async def _keyword_based_classification(self, text: str) -> Dict:
        """Classify text based on keyword matching"""
        try:
            category_scores = {}
            
            for category, data in self.categories.items():
                score = 0
                matched_keywords = []
                
                for keyword in data['keywords']:
                    if keyword in text:
                        # Weight longer keywords more heavily
                        weight = len(keyword.split())
                        score += weight
                        matched_keywords.append(keyword)
                
                # Bonus for priority keywords
                for priority_keyword in data['priority_keywords']:
                    if priority_keyword in text:
                        score += 2
                        matched_keywords.append(f"{priority_keyword} (priority)")
                
                if score > 0:
                    category_scores[category] = {
                        'score': score,
                        'matched_keywords': matched_keywords
                    }
            
            if category_scores:
                best_category = max(category_scores, key=lambda x: category_scores[x]['score'])
                confidence = min(1.0, category_scores[best_category]['score'] / 10)
                
                return {
                    'category': best_category,
                    'confidence': confidence,
                    'matched_keywords': category_scores[best_category]['matched_keywords'],
                    'all_scores': category_scores
                }
            else:
                return {
                    'category': 'General',
                    'confidence': 0.1,
                    'matched_keywords': [],
                    'all_scores': {}
                }
                
        except Exception as e:
            logger.error(f"Error in keyword-based classification: {str(e)}")
            return {'category': 'General', 'confidence': 0.1}
    
    async def _ml_based_classification(self, text: str) -> Dict:
        """Classify text using ML models"""
        try:
            if not self.classification_pipeline:
                return {'category': 'General', 'confidence': 0.1}
            
            # Use zero-shot classification with predefined categories
            candidate_labels = list(self.categories.keys())
            
            result = await asyncio.to_thread(
                self.classification_pipeline,
                text,
                candidate_labels
            )
            
            return {
                'category': result['labels'][0],
                'confidence': result['scores'][0],
                'all_scores': dict(zip(result['labels'], result['scores']))
            }
            
        except Exception as e:
            logger.error(f"Error in ML-based classification: {str(e)}")
            return {'category': 'General', 'confidence': 0.1}
    
    async def _rule_based_classification(self, text: str) -> Dict:
        """Classify text using predefined rules"""
        try:
            # Define classification rules
            rules = [
                {
                    'condition': lambda t: any(word in t for word in ['emergency', 'urgent', 'help', 'police', 'fire']),
                    'category': 'Public Safety',
                    'confidence': 0.9
                },
                {
                    'condition': lambda t: any(word in t for word in ['road', 'pothole', 'streetlight', 'water', 'electricity']),
                    'category': 'Infrastructure',
                    'confidence': 0.8
                },
                {
                    'condition': lambda t: any(word in t for word in ['garbage', 'waste', 'pollution', 'clean']),
                    'category': 'Environment',
                    'confidence': 0.8
                },
                {
                    'condition': lambda t: any(word in t for word in ['bus', 'traffic', 'parking', 'transport']),
                    'category': 'Transportation',
                    'confidence': 0.8
                },
                {
                    'condition': lambda t: any(word in t for word in ['hospital', 'doctor', 'health', 'medical']),
                    'category': 'Healthcare',
                    'confidence': 0.8
                },
                {
                    'condition': lambda t: any(word in t for word in ['school', 'education', 'teacher', 'student']),
                    'category': 'Education',
                    'confidence': 0.8
                },
                {
                    'condition': lambda t: any(word in t for word in ['website', 'online', 'app', 'digital']),
                    'category': 'Digital Services',
                    'confidence': 0.8
                }
            ]
            
            # Apply rules
            for rule in rules:
                if rule['condition'](text):
                    return {
                        'category': rule['category'],
                        'confidence': rule['confidence'],
                        'rule_matched': True
                    }
            
            # Default to General if no rules match
            return {
                'category': 'General',
                'confidence': 0.5,
                'rule_matched': False
            }
            
        except Exception as e:
            logger.error(f"Error in rule-based classification: {str(e)}")
            return {'category': 'General', 'confidence': 0.1}
    
    async def _ensemble_classification(self, results: Dict) -> Dict:
        """Combine multiple classification approaches"""
        try:
            categories = []
            confidences = []
            
            # Collect results from different approaches
            for approach, result in results.items():
                if isinstance(result, dict) and 'category' in result:
                    categories.append(result['category'])
                    confidences.append(result.get('confidence', 0.5))
            
            if not categories:
                return {'category': 'General', 'confidence': 0.1}
            
            # Weighted voting
            category_scores = {}
            for category, confidence in zip(categories, confidences):
                if category not in category_scores:
                    category_scores[category] = 0
                category_scores[category] += confidence
            
            # Find best category
            best_category = max(category_scores, key=category_scores.get)
            total_score = sum(category_scores.values())
            ensemble_confidence = category_scores[best_category] / total_score if total_score > 0 else 0.1
            
            return {
                'category': best_category,
                'confidence': ensemble_confidence,
                'category_scores': category_scores,
                'approach_agreement': len(set(categories)) == 1
            }
            
        except Exception as e:
            logger.error(f"Error in ensemble classification: {str(e)}")
            return {'category': 'General', 'confidence': 0.1}
    
    async def _context_aware_classification(self, results: Dict, context: Dict) -> Dict:
        """Adjust classification based on context"""
        try:
            # Adjust based on user history, location, time, etc.
            if context.get('user_location'):
                # Location-based adjustments
                location = context['user_location'].lower()
                if 'hospital' in location and results['ensemble']['category'] != 'Healthcare':
                    # Boost healthcare category if user is near hospital
                    results['context_adjustment'] = 'location_based'
            
            if context.get('time_of_day'):
                # Time-based adjustments
                hour = context['time_of_day']
                if 22 <= hour or hour <= 6:  # Night time
                    if 'safety' in results.get('keyword_based', {}).get('matched_keywords', []):
                        results['ensemble']['confidence'] *= 1.2
            
            return results
            
        except Exception as e:
            logger.error(f"Error in context-aware classification: {str(e)}")
            return results
    
    async def _assess_priority(self, text: str, classification_results: Dict) -> str:
        """Assess priority level of the text"""
        try:
            text_lower = text.lower()
            
            # Check for high priority keywords
            for keyword in self.priority_levels['high']:
                if keyword in text_lower:
                    return 'high'
            
            # Check category-specific priority
            category = classification_results.get('ensemble', {}).get('category', 'General')
            if category in ['Public Safety', 'Healthcare']:
                # These categories are generally higher priority
                for keyword in self.priority_levels['medium']:
                    if keyword in text_lower:
                        return 'high'
                return 'medium'
            
            # Check for medium priority keywords
            for keyword in self.priority_levels['medium']:
                if keyword in text_lower:
                    return 'medium'
            
            # Check for low priority keywords
            for keyword in self.priority_levels['low']:
                if keyword in text_lower:
                    return 'low'
            
            # Default priority based on category
            if category in ['Infrastructure', 'Environment']:
                return 'medium'
            else:
                return 'low'
                
        except Exception as e:
            logger.error(f"Error assessing priority: {str(e)}")
            return 'medium'
    
    async def _calculate_urgency_score(self, text: str, classification_results: Dict) -> float:
        """Calculate urgency score (1-10)"""
        try:
            base_score = 5.0  # Default medium urgency
            
            # Urgency keywords with weights
            urgency_keywords = {
                'emergency': 4.0,
                'urgent': 3.0,
                'immediate': 3.0,
                'critical': 3.5,
                'dangerous': 3.5,
                'broken': 2.0,
                'not working': 2.0,
                'failed': 2.0,
                'help': 1.5,
                'problem': 1.0,
                'issue': 1.0
            }
            
            text_lower = text.lower()
            urgency_boost = 0
            
            for keyword, weight in urgency_keywords.items():
                if keyword in text_lower:
                    urgency_boost += weight
            
            # Category-based adjustment
            category = classification_results.get('ensemble', {}).get('category', 'General')
            category_multipliers = {
                'Public Safety': 1.5,
                'Healthcare': 1.4,
                'Infrastructure': 1.2,
                'Environment': 1.1,
                'Transportation': 1.0,
                'Education': 0.9,
                'Digital Services': 0.8,
                'General': 0.7
            }
            
            multiplier = category_multipliers.get(category, 1.0)
            final_score = min(10.0, (base_score + urgency_boost) * multiplier)
            
            return round(final_score, 1)
            
        except Exception as e:
            logger.error(f"Error calculating urgency score: {str(e)}")
            return 5.0
    
    async def _classify_subcategory(self, text: str, category: str) -> str:
        """Classify into subcategory within the main category"""
        try:
            if category not in self.subcategories:
                return 'General'
            
            subcategories = self.subcategories[category]
            
            # Simple keyword matching for subcategories
            subcategory_keywords = {
                # Infrastructure subcategories
                'Road Maintenance': ['road', 'pothole', 'street', 'pavement'],
                'Water Supply': ['water', 'tap', 'pipeline', 'supply'],
                'Electricity': ['power', 'electricity', 'electric', 'current'],
                'Drainage': ['drain', 'sewer', 'water logging', 'flood'],
                'Street Lighting': ['streetlight', 'light', 'lamp', 'lighting'],
                'Construction': ['construction', 'building', 'work', 'site'],
                'Utilities': ['utility', 'service', 'connection'],
                
                # Public Safety subcategories
                'Police Services': ['police', 'cop', 'law', 'order'],
                'Fire Safety': ['fire', 'smoke', 'burn', 'flame'],
                'Emergency Response': ['emergency', 'ambulance', '108', '100'],
                'Crime Prevention': ['crime', 'theft', 'robbery', 'violence'],
                'Traffic Safety': ['traffic', 'accident', 'signal', 'crossing'],
                'Security': ['security', 'guard', 'protection', 'safety'],
                
                # Add more subcategory keywords as needed...
            }
            
            text_lower = text.lower()
            best_subcategory = subcategories[0]  # Default to first subcategory
            best_score = 0
            
            for subcategory in subcategories:
                if subcategory in subcategory_keywords:
                    score = sum(1 for keyword in subcategory_keywords[subcategory] if keyword in text_lower)
                    if score > best_score:
                        best_score = score
                        best_subcategory = subcategory
            
            return best_subcategory
            
        except Exception as e:
            logger.error(f"Error classifying subcategory: {str(e)}")
            return 'General'
    
    async def _calculate_classification_confidence(self, results: Dict) -> float:
        """Calculate overall classification confidence"""
        try:
            confidences = []
            
            # Collect confidence scores
            if 'ensemble' in results:
                confidences.append(results['ensemble'].get('confidence', 0.5))
            
            # Agreement bonus
            if results.get('ensemble', {}).get('approach_agreement', False):
                agreement_bonus = 0.1
            else:
                agreement_bonus = 0.0
            
            # Keyword match bonus
            if results.get('keyword_based', {}).get('matched_keywords'):
                keyword_bonus = 0.05
            else:
                keyword_bonus = 0.0
            
            if confidences:
                base_confidence = sum(confidences) / len(confidences)
                return min(1.0, base_confidence + agreement_bonus + keyword_bonus)
            else:
                return 0.1
                
        except Exception as e:
            logger.error(f"Error calculating classification confidence: {str(e)}")
            return 0.1
    
    async def _fallback_classification(self, text: str) -> Dict:
        """Fallback classification when main methods fail"""
        try:
            # Simple keyword-based fallback
            text_lower = text.lower()
            
            # Check for obvious categories
            if any(word in text_lower for word in ['emergency', 'police', 'fire', 'help']):
                return {
                    'category': 'Public Safety',
                    'subcategory': 'Emergency Response',
                    'priority': 'high',
                    'urgency_score': 8.0,
                    'confidence': 0.7,
                    'fallback_used': True
                }
            elif any(word in text_lower for word in ['road', 'water', 'electricity', 'streetlight']):
                return {
                    'category': 'Infrastructure',
                    'subcategory': 'General',
                    'priority': 'medium',
                    'urgency_score': 6.0,
                    'confidence': 0.6,
                    'fallback_used': True
                }
            else:
                return {
                    'category': 'General',
                    'subcategory': 'General',
                    'priority': 'low',
                    'urgency_score': 3.0,
                    'confidence': 0.3,
                    'fallback_used': True
                }
                
        except Exception as e:
            logger.error(f"Error in fallback classification: {str(e)}")
            return {
                'category': 'General',
                'subcategory': 'General',
                'priority': 'low',
                'urgency_score': 1.0,
                'confidence': 0.1,
                'error': str(e)
            }
    
    async def batch_classify(self, texts: List[str]) -> List[Dict]:
        """Classify multiple texts"""
        try:
            results = []
            
            # Process in batches
            batch_size = 16
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]
                batch_results = await asyncio.gather(
                    *[self.classify(text) for text in batch],
                    return_exceptions=True
                )
                
                for result in batch_results:
                    if isinstance(result, Exception):
                        results.append(await self._fallback_classification(""))
                    else:
                        results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Error in batch classification: {str(e)}")
            return [await self._fallback_classification("") for _ in texts]
    
    def get_classification_summary(self, classifications: List[Dict]) -> Dict:
        """Generate summary statistics from multiple classifications"""
        try:
            if not classifications:
                return {}
            
            categories = [c.get('category', 'General') for c in classifications]
            priorities = [c.get('priority', 'low') for c in classifications]
            urgency_scores = [c.get('urgency_score', 1.0) for c in classifications]
            
            category_counts = {}
            for category in categories:
                category_counts[category] = category_counts.get(category, 0) + 1
            
            priority_counts = {}
            for priority in priorities:
                priority_counts[priority] = priority_counts.get(priority, 0) + 1
            
            total = len(classifications)
            
            return {
                'total_classified': total,
                'category_distribution': {
                    category: (count / total) * 100 
                    for category, count in category_counts.items()
                },
                'priority_distribution': {
                    priority: (count / total) * 100 
                    for priority, count in priority_counts.items()
                },
                'average_urgency_score': sum(urgency_scores) / len(urgency_scores),
                'top_category': max(category_counts, key=category_counts.get),
                'high_priority_count': priority_counts.get('high', 0),
                'generated_at': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error generating classification summary: {str(e)}")
            return {}
    
    def get_categories(self) -> Dict[str, Any]:
        """Get available categories and their descriptions"""
        return {
            category: {
                'description': data['description'],
                'subcategories': self.subcategories.get(category, [])
            }
            for category, data in self.categories.items()
        }
    
    def clear_cache(self):
        """Clear the classification cache"""
        self.cache.clear()
        logger.info("Text classification cache cleared")