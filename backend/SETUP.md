# Quick Setup Guide

## Step 1: Install Dependencies

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Step 2: Configure API Key

```bash
copy env.example .env
```

Edit `.env` and replace `YOUR_GEMINI_API_KEY` with your actual key from https://makersuite.google.com/app/apikey

## Step 3: Run Backend

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: http://localhost:8000

## Step 4: Test

Open http://localhost:8000/health in your browser. Should return: `{"status":"ok"}`

## Troubleshooting

- **Import errors**: Make sure you're running from the `backend` directory
- **API key errors**: Verify `.env` file exists and has correct key (no quotes)
- **Port already in use**: Change port with `--port 8001`
