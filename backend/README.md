# Emo-ch AI Backend (FastAPI + Google Gemini)

Production-ready FastAPI backend for the Emo-ch AI emotional support chatbot, powered by Google Gemini API.

## Project Structure

```
backend/
├── main.py                 # FastAPI application and routes
├── models/
│   └── schemas.py         # Request/response models
├── services/
│   └── ai_service.py      # Gemini API service layer
├── requirements.txt       # Python dependencies
├── env.example           # Environment variables template
└── README.md             # This file
```

## Setup (Windows-friendly)

### 1. Create Virtual Environment

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create your `.env` file:

```bash
copy env.example .env
```

Edit `backend/.env` and set your Gemini API key:

```env
GEMINI_API_KEY=your_actual_api_key_here
GEMINI_MODEL=gemini-1.5-flash
ALLOWED_ORIGINS=http://localhost:5173
```

**Getting a Gemini API Key:**
1. Visit https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Create a new API key
4. Copy and paste it into your `.env` file

### 4. Run the Backend

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## API Endpoints

### GET `/health`

Health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

### POST `/chat`

Main chat endpoint for generating empathetic AI responses.

**Request Body:**
```json
{
  "message": "I've been feeling really stressed lately",
  "history": [
    {
      "role": "user",
      "content": "Hello"
    },
    {
      "role": "ai",
      "content": "Hi there! I'm here to listen. How are you feeling today?"
    }
  ]
}
```

**Response:**
```json
{
  "reply": "I understand that stress can be really overwhelming. Would you like to talk about what's been causing you to feel this way?"
}
```

**Note:** The `history` field is optional. If omitted, only the current message will be used.

## Architecture

- **Clean Architecture**: Separated concerns with models, services, and routes
- **Service Layer**: `AIService` handles all Gemini API interactions
- **Error Handling**: Graceful fallbacks and user-friendly error messages
- **Type Safety**: Full Pydantic validation for requests and responses
- **CORS**: Configured for frontend integration

## Troubleshooting

### "GEMINI_API_KEY environment variable is required"

- Make sure you created `backend/.env` file
- Verify the API key is set correctly (no quotes, no spaces)
- Restart the server after changing `.env`

### "AI service authentication failed"

- Check that your Gemini API key is valid
- Ensure you haven't exceeded API quotas
- Verify the key has proper permissions

### CORS Errors

- Update `ALLOWED_ORIGINS` in `.env` to match your frontend URL
- Restart the server after changing `.env`

## Development

The server runs with auto-reload enabled. Any changes to Python files will automatically restart the server.

## Production Deployment

For production:
1. Remove `--reload` flag
2. Use a production ASGI server like `gunicorn` with `uvicorn` workers
3. Set proper `ALLOWED_ORIGINS` for your domain
4. Use environment variables from your hosting platform (not `.env` file)
