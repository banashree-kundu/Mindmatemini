# MindMate Mini

A minimal Flask-based chatbot for mood detection, empathetic replies, and short motivational quotes/exercises. Designed as a small local app that can optionally use a Gemini-compatible API if you provide credentials.

## Project structure

- `app.py` - Flask application (routes: `/` and `/api/chat`)
- `gemini_client.py` - Wrapper that calls a Gemini-compatible HTTP endpoint or falls back to local heuristics
- `templates/index.html` - Simple chat UI
- `static/style.css` - UI styles
- `requirements.txt` - Python dependencies

## Setup (Windows PowerShell)

1. Create and activate a virtual environment (PowerShell):

```powershell
python -m venv .venv; .\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. (Optional) Configure Gemini API

If you have access to a Gemini-compatible HTTP endpoint, set these environment variables in your shell (replace values):

```powershell
$env:GEMINI_API_KEY = 'your_api_key_here'
$env:GEMINI_API_URL = 'https://your-gemini-endpoint.example/v1/generate'
```

The code expects a simple POST JSON API that accepts a prompt and returns text. If no `GEMINI_API_KEY` is present, the app uses a safe local fallback.

4. Run the app:

```powershell
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

## How it works

- The front-end sends the user's message to `/api/chat`.
- `gemini_client.detect_mood()` returns a short mood label (remote call if configured, otherwise local heuristic).
- `gemini_client.generate_response()` produces a concise empathetic reply and one actionable suggestion.

## Notes & Next steps

- The Gemini client is intentionally generic; adapt `_call_remote_gemini` to the exact shape of your Gemini API (Google Cloud Generative Models, internal proxy, etc.).
- Consider adding authentication, rate limiting, conversation history, or more advanced prompt engineering for richer replies.
- For production, disable `debug=True` in `app.py` and use a proper WSGI server.

Enjoy MindMate Mini — a small, empathetic assistant for mood check-ins and motivation.
