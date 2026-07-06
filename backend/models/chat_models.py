from pydantic import BaseModel , Field
from typing import Optional
from datetime import datetime

class ChatRequest(BaseModel):
    """User message request"""
    question : str = Field(...,min_length=1,description="user's questions")

class ChatResponse(BaseModel):
    "AI Response"
    message : str
    timestamp : datetime

class HealthRequest(BaseModel):
    """Health check response"""
    status : str
    version : str