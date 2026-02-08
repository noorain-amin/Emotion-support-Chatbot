"""
Request and response schemas for the Emo-ch AI API.
"""
from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Represents a single message in the conversation history."""
    role: Literal["user", "ai", "model"]  # "ai" for frontend compatibility, "model" for Gemini
    content: str


class ChatRequest(BaseModel):
    """Request model for the /chat endpoint."""
    message: str = Field(..., min_length=1, max_length=4000, description="User's message")
    session_id: Optional[str] = Field(
        default=None,
        description="Session ID to maintain conversation history (optional)"
    )


class ChatResponse(BaseModel):
    """Response model for the /chat endpoint."""
    reply: str = Field(..., description="AI-generated empathetic response")
    session_id: str = Field(..., description="Session ID for maintaining conversation history")


class HealthResponse(BaseModel):
    """Response model for the /health endpoint."""
    status: str = Field(default="ok", description="Service health status")
