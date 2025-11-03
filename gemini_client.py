"""
Simple Gemini client wrapper.

This module provides two functions used by the Flask app:
- detect_mood(text): returns a short mood label (e.g., 'happy', 'sad', 'anxious', 'neutral')
- generate_response(text, mood): returns an empathetic reply + motivational quote or exercise

Configuration via environment variables:
- GEMINI_API_KEY (optional): API key for Gemini-compatible endpoint
- GEMINI_API_URL (optional): Full URL of the Gemini endpoint that accepts POST JSON payloads

If no API key is provided, the module falls back to safe local stubs.
"""
import os
import requests
import random
"""
Simple Gemini client wrapper.

Provides two functions used by the Flask app:
- detect_mood(text): returns a short mood label (e.g., 'happy', 'sad', 'anxious', 'neutral')
- generate_response(text, mood): returns an empathetic reply + motivational quote or exercise

Configuration via environment variables:
- GEMINI_API_KEY (optional): API key for Gemini-compatible endpoint
- GEMINI_API_URL (optional): Full URL of the Gemini endpoint that accepts POST JSON payloads

If no API key is provided, the module falls back to safe local stubs.
"""
import os
import requests
import random

GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
GEMINI_API_URL = os.environ.get('GEMINI_API_URL', 'https://api.example.com/v1/generate')

# Safe fallback answers
MOOD_LABELS = ['happy', 'sad', 'anxious', 'stressed', 'tired', 'neutral', 'motivated']
QUOTES = [
    "You are stronger than you think.",
    "Small steps forward are still progress.",
    "Take a breath — you're doing your best.",
    "Focus on what you can control today.",
]
EXERCISES = [
    "Try box breathing: inhale 4s, hold 4s, exhale 4s, hold 4s — repeat 4 times.",
    "Write down 3 things you're grateful for right now.",
    "Stand up, stretch for 60 seconds, and take a short walk.",
]


def _call_remote_gemini(prompt: str, system_prompt: str = None) -> str:
    """Call a Gemini-compatible HTTP endpoint.

    The exact payload depends on the user's Gemini setup. We send a conservative JSON structure:
    {"model": "gemini", "prompt": prompt}

    If GEMINI_API_KEY is not set, this raises RuntimeError.
    """
    if not GEMINI_API_KEY:
        raise RuntimeError('GEMINI_API_KEY not configured')

    headers = {
        'Authorization': f'Bearer {GEMINI_API_KEY}',
        'Content-Type': 'application/json',
    }
    payload = {
        'model': 'gemini',
        'prompt': prompt,
    }
    if system_prompt:
        payload['system'] = system_prompt

    resp = requests.post(GEMINI_API_URL, headers=headers, json=payload, timeout=15)
    resp.raise_for_status()
    j = resp.json()

    # Try to read a text response from common fields
    if isinstance(j, dict):
        # Very generic handling: try several common keys
        for key in ('text', 'response', 'output', 'content'):
            if key in j and isinstance(j[key], str):
                return j[key]
        # Some APIs return choices -> [{message: {content: '...'}}]
        choices = j.get('choices')
        if choices and isinstance(choices, list):
            first = choices[0]
            if isinstance(first, dict):
                # different shapes
                if 'text' in first and isinstance(first['text'], str):
                    return first['text']
                msg = first.get('message')
                if msg and isinstance(msg, dict):
                    content = msg.get('content')
                    if isinstance(content, str):
                        return content
    # Fallback to raw text
    return str(j)


def detect_mood(text: str) -> str:
    """Detects the user's mood from text.

    If GEMINI_API_KEY is set, calls remote API. Otherwise uses a small keyword heuristic.
    Returns a simple lowercase label.
    """
    text = (text or '').strip()
    if not text:
        return 'neutral'

    if GEMINI_API_KEY:
        prompt = (
            "You are a mood classifier. Given the user's message, reply with a single short lowercase mood label like: "
            "happy, sad, anxious, stressed, tired, neutral, motivated.\n\nMessage:\n" + text
        )
        try:
            out = _call_remote_gemini(prompt)
            # Basic cleanup
            out = out.strip().lower()
            # Return the first matching known label if present
            for label in MOOD_LABELS:
                if label in out:
                    return label
            # Otherwise return first word
            return out.split()[0]
        except Exception:
            # fall through to local heuristic
            pass

    # Local heuristic fallback
    low = text.lower()
    if any(w in low for w in ('sad', 'unhappy', 'depressed', 'down', 'lonely')):
        return 'sad'
    if any(w in low for w in ('anxious', 'anxiety', 'nervous', 'worried')):
        return 'anxious'
    if any(w in low for w in ('stressed', 'overwhelmed', 'panic')):
        return 'stressed'
    if any(w in low for w in ('tired', 'exhausted', 'sleepy')):
        return 'tired'
    if any(w in low for w in ('great', 'good', 'happy', 'awesome', 'fantastic')):
        return 'happy'
    if any(w in low for w in ('motivated', 'productive', 'energized')):
        return 'motivated'
    return 'neutral'


def generate_response(user_text: str, mood: str) -> str:
    """Generate an empathetic reply + short motivational quote or exercise.

    If GEMINI_API_KEY is set, uses the remote model to produce a concise friendly reply. Otherwise returns a local templated response.
    """
    user_text = (user_text or '').strip()
    mood = (mood or 'neutral').lower()

    # Quick local short-circuit responses
    if mood == 'happy':
        return "😊 It's great to hear you're feeling good! Keep building on this energy — maybe take a moment to celebrate a small win today. You are stronger than you think."
    if mood == 'sad':
        return "😔 I'm sorry you're feeling down — that can be really hard. It's okay to take things slowly; try writing one thing you appreciate about yourself right now. Stand up, stretch for 60 seconds, and take a short walk."
    if mood == 'angry':
        return "😤 I can sense some frustration. Try deep breathing or journaling for 2 minutes — it might help calm your thoughts."

    if GEMINI_API_KEY:
        system_prompt = (
            "You are MindMate Mini, an empathetic mental wellness assistant. Given the user's message and a detected mood, "
            "compose a short (2-4 sentences) empathetic reply and include one short practical action or breathing exercise or motivational quote. "
            "Keep a warm, supportive tone and be concise. Do NOT provide medical advice. Format as plain text."
        )
        prompt = f"User message:\n{user_text}\n\nDetected mood: {mood}\n\nResponse:"
        try:
            out = _call_remote_gemini(prompt, system_prompt=system_prompt)
            return out.strip()
        except Exception:
            # Fall back to local template below
            pass

    # Local stubbed response
    quote = random.choice(QUOTES)
    exercise = random.choice(EXERCISES)

    templates = {
        'happy': f"It's great to hear you're feeling good. Keep building on this energy — maybe take a moment to celebrate a small win today. {quote}",
        'sad': f"I'm sorry you're feeling down — that can be really hard. It's okay to take things slowly; try writing one thing you appreciate about yourself right now. {exercise}",
        'anxious': f"I hear your worry — that feeling can be overwhelming. Try a short grounding exercise: name 3 things you can see, 2 things you can touch, and 1 thing you can hear. {exercise}",
        'stressed': f"Stress can pile up; you're not alone. Take a 1-minute break and do box breathing (4-4-4-4). {exercise}",
        'tired': f"Feeling tired makes everything harder. If possible, give yourself a short rest or a gentle stretch. Even a 5-minute break can help. {quote}",
        'motivated': f"Nice — you're feeling motivated. Channel that into one focused 20-minute task and then reward yourself. {quote}",
        'neutral': f"Thanks for sharing. If you'd like, tell me more or try a 60-second breathing break to reset. {exercise}",
    }

    return templates.get(mood, templates['neutral'])
