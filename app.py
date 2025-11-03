import os
import json
from flask import Flask, render_template, request, jsonify
from gemini_client import detect_mood, generate_response

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.get_json() or {}
    message = data.get('message', '').strip()
    if not message:
        return jsonify({'error': 'Message is required.'}), 400

    # Detect mood from the user's message
    mood = detect_mood(message)

    # Generate an empathetic reply and a short actionable suggestion
    assistant_reply = generate_response(message, mood)

    response = {
        'mood': mood,
        'reply': assistant_reply
    }
    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
