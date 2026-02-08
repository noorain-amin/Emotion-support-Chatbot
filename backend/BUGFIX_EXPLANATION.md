# Bug Fix: Repeated AI Responses

## Problem Identified

The chatbot was returning the same response for every user input because **conversation history was being lost** between requests.

## Root Causes

### 1. Role Mismatch (Critical Bug)
- **Frontend** sends messages with `role: "ai"`
- **Gemini API** requires `role: "model"`
- The AI service was filtering out all messages with `role: "ai"` because it only accepted `"user"` or `"model"`
- **Result**: All AI responses in history were silently dropped, so Gemini had no conversation context

### 2. No Server-Side Session Management
- History was only maintained client-side
- If frontend state was lost or incomplete, conversation broke
- No way to maintain conversations across browser refreshes
- Multiple users would interfere with each other's conversations

### 3. History Not Persisted After AI Response
- Backend received history but didn't save it
- Each request was treated as independent
- AI service received incomplete or missing history

## Solution Implemented

### 1. Fixed Role Conversion
**File**: `backend/services/ai_service.py`
- Added explicit conversion: `"ai" -> "model"` before sending to Gemini
- Now all messages in history are properly included in API calls

### 2. Added Session Store
**File**: `backend/services/session_store.py` (new)
- In-memory dictionary storing conversation history per session
- Each session gets a unique UUID
- History limited to last 50 messages to prevent memory issues
- Thread-safe for multiple concurrent users

### 3. Updated Chat Endpoint
**File**: `backend/main.py`
- Accepts optional `session_id` in request
- Retrieves existing history from session store
- Appends user message BEFORE calling AI
- Appends AI response AFTER generation
- Saves complete history back to session store
- Returns `session_id` in response

### 4. Updated Request/Response Schemas
**File**: `backend/models/schemas.py`
- `ChatRequest` now has `session_id` instead of `history`
- `ChatResponse` now includes `session_id`
- Frontend no longer needs to send history (server maintains it)

### 5. Updated Frontend
**File**: `frontend/src/components/ChatSection.tsx`
- Stores `session_id` in component state
- Sends `session_id` with each request
- Receives and updates `session_id` from response
- Removed client-side history management (now server-side)

## How It Works Now

1. **First Request**:
   - Frontend sends: `{ message: "Hello", session_id: null }`
   - Backend creates new session, stores user message
   - AI generates response using system instruction only
   - Backend saves both messages, returns `session_id`

2. **Subsequent Requests**:
   - Frontend sends: `{ message: "How are you?", session_id: "abc-123" }`
   - Backend retrieves full history from session store
   - History includes: `[user: "Hello", ai: "Hi there..."], [user: "How are you?"]`
   - AI generates response with full context
   - Backend appends AI response and saves complete history

3. **Multiple Users**:
   - Each user gets unique `session_id`
   - Sessions stored separately in dictionary
   - No cross-contamination between conversations

## Why This Fixes the Issue

- **Role conversion** ensures all messages reach Gemini API
- **Server-side storage** ensures history persists across requests
- **Automatic history management** means frontend doesn't need to track it
- **Session isolation** allows multiple concurrent users

## Testing

To verify the fix works:
1. Send first message → Get response with `session_id`
2. Send second message with same `session_id` → Response should reference previous conversation
3. Send third message → Should show understanding of entire conversation context

The AI should now provide varied, contextually-aware responses instead of repeating the same message.
