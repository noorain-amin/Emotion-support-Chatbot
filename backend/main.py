"""
FastAPI application for Emo-ch AI emotional support chatbot backend.
"""
import os
from typing import List

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models.schemas import ChatMessage, ChatRequest, ChatResponse, HealthResponse
from services.ai_service import get_ai_service
from services.session_store import get_session_store

# Load environment variables
load_dotenv()


def _split_origins(value: str) -> List[str]:
    """Split comma-separated origins string into a list."""
    return [o.strip() for o in value.split(",") if o.strip()]


# Initialize FastAPI app
app = FastAPI(
    title="Emo-ch AI Backend",
    version="1.0.0",
    description="Emotional support chatbot API powered by Google Gemini"
)

# Configure CORS
allowed_origins = _split_origins(os.getenv("ALLOWED_ORIGINS", "http://localhost:8080"))
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
def health_check():
    """
    Health check endpoint to verify the API is running.
    
    Returns:
        HealthResponse with status "ok"
    """
    return HealthResponse(status="ok")


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """
    Main chat endpoint that generates empathetic AI responses.
    
    Maintains conversation history server-side using session_id.
    Each request appends the user message, gets AI response, and saves both to session.
    
    Args:
        request: ChatRequest containing user message and optional session_id
        
    Returns:
        ChatResponse with AI-generated empathetic reply and session_id
        
    Raises:
        HTTPException: If AI service fails or request is invalid
    """
    try:
        session_store = get_session_store()
        ai_service = get_ai_service()
        
        # Get or create session
        if request.session_id and session_store.session_exists(request.session_id):
            session_id = request.session_id
            # Retrieve existing conversation history from session store
            history = session_store.get_history(session_id) or []
        else:
            # Create new session if none provided or session doesn't exist
            session_id = session_store.create_session()
            history = []
        
        # Append user message to history BEFORE calling AI
        user_message_obj = ChatMessage(role="user", content=request.message)
        history.append(user_message_obj)
        
        # Generate AI response using full conversation history
        reply = ai_service.generate_response(
            user_message=request.message,
            history=history
        )
        
        # Append AI response to history AFTER generation
        ai_message_obj = ChatMessage(role="ai", content=reply)
        history.append(ai_message_obj)
        
        # Save updated history back to session store
        session_store.update_history(session_id, history)
        
        return ChatResponse(reply=reply, session_id=session_id)
        
    except ValueError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Service configuration error: {str(e)}"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred: {str(e)}"
        )


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "name": "Emo-ch AI Backend",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "chat": "/chat (POST)"
        }
    }
