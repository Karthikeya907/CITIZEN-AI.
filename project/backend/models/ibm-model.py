from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum

# Enums
class SentimentType(str, Enum):
    positive = "positive"
    negative = "negative"
    neutral = "neutral"

class PriorityLevel(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"

class ConcernType(str, Enum):
    concern = "concern"
    feedback = "feedback"

class UserRole(str, Enum):
    citizen = "citizen"
    admin = "admin"
    moderator = "moderator"

# Base schemas
class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
        use_enum_values = True

# User schemas
class UserBase(BaseSchema):
    email: EmailStr
    full_name: str
    phone: Optional[str] = None
    address: Optional[str] = None

class UserCreateRequest(UserBase):
    password: str

class UserResponse(UserBase):
    id: str
    role: UserRole
    is_active: bool
    created_at: datetime
    last_login: Optional[datetime] = None

class UserUpdateRequest(BaseSchema):
    full_name: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None

# Authentication schemas
class LoginRequest(BaseSchema):
    email: EmailStr
    password: str

class TokenResponse(BaseSchema):
    access_token: str
    token_type: str
    expires_in: int
    user: Optional[UserResponse] = None

# AI Response schemas
class AIResponse(BaseSchema):
    text: str
    confidence: float = Field(ge=0.0, le=1.0)
    response_time: float
    model_used: str
    metadata: Optional[Dict[str, Any]] = None

# Chat schemas
class ChatRequest(BaseSchema):
    message: str
    context: Optional[Dict[str, Any]] = None
    conversation_id: Optional[str] = None

class ChatResponse(BaseSchema):
    id: str
    message: str
    timestamp: datetime
    sentiment: Optional[Dict[str, Any]] = None
    classification: Optional[Dict[str, Any]] = None
    confidence: float = Field(ge=0.0, le=1.0)
    conversation_id: Optional[str] = None

# Sentiment Analysis schemas
class SentimentAnalysisRequest(BaseSchema):
    text: str
    context: Optional[Dict[str, Any]] = None

class SentimentAnalysisResponse(BaseSchema):
    sentiment: SentimentType
    confidence: float = Field(ge=0.0, le=1.0)
    polarity: Optional[float] = Field(ge=-1.0, le=1.0, default=None)
    subjectivity: Optional[float] = Field(ge=0.0, le=1.0, default=None)
    emotions: Optional[Dict[str, float]] = None
    dominant_emotion: Optional[str] = None
    civic_analysis: Optional[Dict[str, Any]] = None
    processed_at: datetime = Field(default_factory=datetime.utcnow)

# Text Classification schemas
class TextClassificationRequest(BaseSchema):
    text: str
    context: Optional[Dict[str, Any]] = None

class TextClassificationResponse(BaseSchema):
    category: str
    subcategory: Optional[str] = None
    confidence: float = Field(ge=0.0, le=1.0)
    priority: PriorityLevel
    urgency_score: float = Field(ge=1.0, le=10.0)
    matched_keywords: Optional[List[str]] = None
    all_categories: Optional[Dict[str, float]] = None
    processed_at: datetime = Field(default_factory=datetime.utcnow)

# Concern schemas
class ConcernBase(BaseSchema):
    message: str
    category: Optional[str] = None
    location: Optional[str] = None
    attachments: Optional[List[str]] = None

class ConcernCreateRequest(ConcernBase):
    type: ConcernType = ConcernType.concern

class ConcernResponse(ConcernBase):
    id: str
    user_id: str
    type: ConcernType
    sentiment: SentimentType
    priority: PriorityLevel
    urgency_score: float
    status: str = "open"
    assigned_to: Optional[str] = None
    resolution: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    resolved_at: Optional[datetime] = None

class ConcernUpdateRequest(BaseSchema):
    status: Optional[str] = None
    assigned_to: Optional[str] = None
    resolution: Optional[str] = None

# Feedback schemas
class FeedbackBase(BaseSchema):
    message: str
    category: Optional[str] = None
    rating: Optional[int] = Field(ge=1, le=5, default=None)

class FeedbackCreateRequest(FeedbackBase):
    type: ConcernType = ConcernType.feedback

class FeedbackResponse(FeedbackBase):
    id: str
    user_id: str
    type: ConcernType
    sentiment: SentimentType
    priority: PriorityLevel
    created_at: datetime
    acknowledged: bool = False
    acknowledged_by: Optional[str] = None
    acknowledged_at: Optional[datetime] = None

# Analytics schemas
class DashboardAnalytics(BaseSchema):
    total_submissions: int
    active_concerns: int
    positive_feedback: int
    average_sentiment: float
    top_categories: List[Dict[str, Union[str, int]]]
    recent_trends: Dict[str, str]
    generated_at: datetime

class SentimentTrendsResponse(BaseSchema):
    trends: List[Dict[str, Any]]
    period_days: int
    category: Optional[str] = None
    generated_at: datetime

class CategoryAnalytics(BaseSchema):
    category: str
    total_submissions: int
    sentiment_distribution: Dict[str, int]
    priority_distribution: Dict[str, int]
    average_urgency_score: float
    resolution_rate: Optional[float] = None
    average_resolution_time: Optional[float] = None

# Admin schemas
class AdminStatsResponse(BaseSchema):
    total_users: int
    total_concerns: int
    total_feedback: int
    avg_response_time: float
    satisfaction_score: float
    top_categories: List[Dict[str, Any]]
    recent_activity: List[Dict[str, Any]]
    generated_at: datetime = Field(default_factory=datetime.utcnow)

class UserActivityStats(BaseSchema):
    user_id: str
    total_submissions: int
    concerns_count: int
    feedback_count: int
    average_sentiment: float
    most_active_category: str
    last_activity: datetime

# Batch processing schemas
class BatchProcessRequest(BaseSchema):
    messages: List[str]
    process_type: str = "sentiment_and_classification"
    options: Optional[Dict[str, Any]] = None

class BatchProcessResponse(BaseSchema):
    job_id: str
    status: str
    total_messages: int
    processed_messages: int = 0
    estimated_completion: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)

class BatchJobStatus(BaseSchema):
    job_id: str
    status: str
    total_messages: int
    processed_messages: int
    progress_percentage: float
    results: Optional[List[Dict[str, Any]]] = None
    error: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

# Notification schemas
class NotificationBase(BaseSchema):
    title: str
    message: str
    type: str = "info"  # info, warning, error, success
    priority: PriorityLevel = PriorityLevel.medium

class NotificationCreateRequest(NotificationBase):
    user_ids: Optional[List[str]] = None
    send_email: bool = False
    send_sms: bool = False

class NotificationResponse(NotificationBase):
    id: str
    user_id: str
    read: bool = False
    created_at: datetime
    read_at: Optional[datetime] = None

# Search and Filter schemas
class SearchRequest(BaseSchema):
    query: str
    filters: Optional[Dict[str, Any]] = None
    sort_by: Optional[str] = "created_at"
    sort_order: Optional[str] = "desc"
    page: int = Field(ge=1, default=1)
    page_size: int = Field(ge=1, le=100, default=20)

class SearchResponse(BaseSchema):
    results: List[Dict[str, Any]]
    total_count: int
    page: int
    page_size: int
    total_pages: int

# Export schemas
class ExportRequest(BaseSchema):
    format: str = "csv"  # csv, json, xlsx
    filters: Optional[Dict[str, Any]] = None
    date_range: Optional[Dict[str, datetime]] = None
    include_fields: Optional[List[str]] = None

class ExportResponse(BaseSchema):
    export_id: str
    status: str
    file_url: Optional[str] = None
    created_at: datetime
    expires_at: datetime

# System schemas
class HealthCheckResponse(BaseSchema):
    status: str
    timestamp: datetime
    version: str
    services: Dict[str, str]
    uptime: Optional[float] = None

class SystemMetrics(BaseSchema):
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    active_connections: int
    requests_per_minute: int
    error_rate: float
    average_response_time: float
    timestamp: datetime

# WebSocket schemas
class WebSocketMessage(BaseSchema):
    type: str
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class WebSocketResponse(BaseSchema):
    type: str
    data: Dict[str, Any]
    status: str = "success"
    error: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Configuration schemas
class AIModelConfig(BaseSchema):
    model_name: str
    temperature: float = Field(ge=0.0, le=2.0, default=0.7)
    max_tokens: int = Field(ge=1, le=4096, default=512)
    top_p: float = Field(ge=0.0, le=1.0, default=0.9)
    frequency_penalty: float = Field(ge=-2.0, le=2.0, default=0.0)
    presence_penalty: float = Field(ge=-2.0, le=2.0, default=0.0)

class SystemConfig(BaseSchema):
    ai_model_config: AIModelConfig
    rate_limits: Dict[str, int]
    cache_ttl: int = 3600
    max_file_size: int = 10485760  # 10MB
    allowed_file_types: List[str] = ["jpg", "jpeg", "png", "pdf", "doc", "docx"]
    notification_settings: Dict[str, bool]

# Error schemas
class ErrorResponse(BaseSchema):
    error: str
    message: str
    details: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None

class ValidationErrorResponse(BaseSchema):
    error: str = "validation_error"
    message: str
    field_errors: List[Dict[str, str]]
    timestamp: datetime = Field(default_factory=datetime.utcnow)

# Pagination schemas
class PaginationParams(BaseSchema):
    page: int = Field(ge=1, default=1)
    page_size: int = Field(ge=1, le=100, default=20)

class PaginatedResponse(BaseSchema):
    items: List[Any]
    total_count: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_previous: bool

# File upload schemas
class FileUploadResponse(BaseSchema):
    file_id: str
    filename: str
    file_size: int
    file_type: str
    upload_url: str
    uploaded_at: datetime

class FileMetadata(BaseSchema):
    file_id: str
    filename: str
    file_size: int
    file_type: str
    uploaded_by: str
    uploaded_at: datetime
    is_public: bool = False
    tags: Optional[List[str]] = None

# Integration schemas
class WebhookPayload(BaseSchema):
    event_type: str
    data: Dict[str, Any]
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    signature: Optional[str] = None

class APIKeyResponse(BaseSchema):
    api_key: str
    name: str
    permissions: List[str]
    created_at: datetime
    expires_at: Optional[datetime] = None
    last_used: Optional[datetime] = None

# Audit schemas
class AuditLogEntry(BaseSchema):
    id: str
    user_id: Optional[str] = None
    action: str
    resource_type: str
    resource_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    user_agent: Optional[str] = None
    timestamp: datetime

class AuditLogResponse(BaseSchema):
    entries: List[AuditLogEntry]
    total_count: int
    page: int
    page_size: int