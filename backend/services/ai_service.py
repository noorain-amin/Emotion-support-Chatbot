"""
AI service layer for generating empathetic responses using Google Gemini API.
"""
import os
from typing import List, Optional

import google.generativeai as genai
from fastapi import HTTPException

from models.schemas import ChatMessage


class AIService:
    """Service for interacting with Google Gemini API to generate empathetic responses."""
    
    def __init__(self):
        """Initialize the AI service with API key from environment."""
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY environment variable is required. "
                "Set it in your .env file."
            )
        
        genai.configure(api_key=api_key)
        
        # Model configuration for empathetic responses
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        
        # System instruction for emotional support
        system_instruction = (
            "You are Emo-ch AI, an empathetic emotional support chatbot. "
            "Your role is to provide warm, validating, and non-judgmental support. "
            "Keep responses concise (2-4 sentences), natural, and emotionally attuned. "
            "Ask gentle follow-up questions to understand the user better. "
            "Offer simple, practical coping strategies when appropriate (breathing exercises, grounding techniques, journaling). "
            "Do NOT provide medical, legal, or professional advice. "
            "If the user expresses intent to self-harm or immediate danger, "
            "encourage them to contact local emergency services or a trusted person immediately. "
            "Always respond with empathy and understanding."
        )
        
        # Initialize model with system instruction
        self.model = genai.GenerativeModel(
            self.model_name,
            system_instruction=system_instruction
        )
    
    def generate_response(
        self,
        user_message: str,
        history: Optional[List[ChatMessage]] = None
    ) -> str:
        """
        Generate an empathetic AI response using Gemini API.
        
        Args:
            user_message: The current user message
            history: Optional conversation history
            
        Returns:
            Generated empathetic response string
            
        Raises:
            HTTPException: If API call fails or returns invalid response
        """
        try:
            # Build conversation context
            if history and len(history) > 0:
                # Build conversation history as messages for chat
                chat_history = []
                for msg in history[-20:]:  # Limit to last 20 messages
                    role = "user" if msg.role == "user" else "model"
                    chat_history.append({
                        "role": role,
                        "parts": [msg.content]
                    })
                
                # Start chat session with history
                chat = self.model.start_chat(history=chat_history)
                response = chat.send_message(
                    user_message,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7,
                        max_output_tokens=300,
                        top_p=0.9,
                    )
                )
            else:
                # No history - direct generation
                response = self.model.generate_content(
                    user_message,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.7,
                        max_output_tokens=300,
                        top_p=0.9,
                    )
                )
            
            # Extract text from response
            reply = response.text.strip() if response.text else ""
            
            if not reply:
                # Fallback response if API returns empty
                return self._get_fallback_response(user_message)
            
            return reply
            
        except Exception as e:
            # Log error details for debugging
            error_msg = str(e)
            
            # Provide user-friendly error messages
            if "API_KEY" in error_msg or "authentication" in error_msg.lower():
                raise HTTPException(
                    status_code=500,
                    detail="AI service authentication failed. Please check API key configuration."
                )
            elif "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
                raise HTTPException(
                    status_code=503,
                    detail="AI service is temporarily unavailable due to rate limits. Please try again later."
                )
            else:
                # Return fallback response instead of crashing
                return self._get_fallback_response(user_message)
    
    def _get_fallback_response(self, user_message: str) -> str:
        """
        Generate a fallback empathetic response when API fails.
        
        Args:
            user_message: The user's message (for context)
            
        Returns:
            A simple empathetic fallback message
        """
        return (
            "I'm here for you, and I want to understand what you're going through. "
            "Could you tell me a bit more about how you're feeling right now?"
        )


# Singleton instance (initialized on first import)
_ai_service: Optional[AIService] = None


def get_ai_service() -> AIService:
    """
    Get or create the singleton AI service instance.
    
    Returns:
        AIService instance
        
    Raises:
        ValueError: If GEMINI_API_KEY is not configured
    """
    global _ai_service
    if _ai_service is None:
        _ai_service = AIService()
    return _ai_service
