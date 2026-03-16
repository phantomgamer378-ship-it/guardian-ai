# Frontend Integration Guide

## Option 1: HTML/JavaScript (Simple)

```html
<!DOCTYPE html>
<html>
<head>
    <title>Guardian AI</title>
    <style>
        body { font-family: Arial; max-width: 800px; margin: 0 auto; padding: 20px; }
        .chat-container { border: 1px solid #ddd; padding: 20px; height: 400px; overflow-y: auto; }
        .input-group { margin-top: 20px; }
        input { width: 80%; padding: 10px; }
        button { padding: 10px 20px; background: #007bff; color: white; border: none; }
        .message { margin: 10px 0; padding: 10px; border-radius: 5px; }
        .user { background: #e3f2fd; text-align: right; }
        .bot { background: #f3e5f5; }
    </style>
</head>
<body>
    <h1>Guardian AI - Cybersecurity Assistant</h1>
    <div id="chat" class="chat-container"></div>
    <div class="input-group">
        <input type="text" id="messageInput" placeholder="Ask about cybersecurity...">
        <button onclick="sendMessage()">Send</button>
    </div>

    <script>
        const API_URL = 'https://your-app-url.onrender.com/api/v1/chat';
        let userId = 'user_' + Math.random().toString(36).substr(2, 9);
        let sessionId = 'session_' + Date.now();

        async function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message) return;

            // Add user message
            addMessage(message, 'user');
            input.value = '';

            try {
                const response = await fetch(API_URL, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        user_id: userId,
                        session_id: sessionId,
                        message: message
                    })
                });

                const data = await response.json();
                addMessage(data.response, 'bot');
            } catch (error) {
                addMessage('Sorry, I encountered an error. Please try again.', 'bot');
            }
        }

        function addMessage(text, sender) {
            const chat = document.getElementById('chat');
            const div = document.createElement('div');
            div.className = `message ${sender}`;
            div.textContent = text;
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
        }

        // Enter key support
        document.getElementById('messageInput').addEventListener('keypress', (e) => {
            if (e.key === 'Enter') sendMessage();
        });
    </script>
</body>
</html>
```

## Option 2: React Integration

```jsx
// ChatComponent.jsx
import React, { useState } from 'react';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1/chat';

export default function ChatComponent() {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [userId] = useState(() => 'user_' + Math.random().toString(36).substr(2, 9));
    const [sessionId] = useState(() => 'session_' + Date.now());

    const sendMessage = async () => {
        if (!input.trim()) return;

        const userMessage = { text: input, sender: 'user' };
        setMessages(prev => [...prev, userMessage]);

        try {
            const response = await fetch(API_URL, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    user_id: userId,
                    session_id: sessionId,
                    message: input
                })
            });

            const data = await response.json();
            const botMessage = { text: data.response, sender: 'bot' };
            setMessages(prev => [...prev, botMessage]);
        } catch (error) {
            const errorMessage = { text: 'Error: Could not reach chatbot', sender: 'bot' };
            setMessages(prev => [...prev, errorMessage]);
        }

        setInput('');
    };

    return (
        <div className="chat-container">
            <div className="messages">
                {messages.map((msg, i) => (
                    <div key={i} className={`message ${msg.sender}`}>
                        {msg.text}
                    </div>
                ))}
            </div>
            <div className="input-area">
                <input
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
                    placeholder="Ask about cybersecurity..."
                />
                <button onClick={sendMessage}>Send</button>
            </div>
        </div>
    );
}
```

## Option 3: Python Flask Frontend

```python
# app.py
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)
API_URL = "https://your-app-url.onrender.com/api/v1/chat"

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    
    try:
        response = requests.post(API_URL, json={
            'user_id': request.json.get('user_id', 'web_user'),
            'session_id': request.json.get('session_id', 'web_session'),
            'message': user_message
        })
        
        return jsonify(response.json())
    except:
        return jsonify({'response': 'Sorry, I encountered an error.'})

if __name__ == '__main__':
    app.run(debug=True)
```

## Environment Variables for Production

```bash
# Render/Railway Environment Variables
GROQ_API_KEY=your_production_groq_key
SECRET_KEY=your_production_secret_key
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

## CORS Configuration

Add to your FastAPI app for production:

```python
# In main.py, update CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com", "https://your-app.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
