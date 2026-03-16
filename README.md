# Guardian AI - Cybersecurity Chatbot API

A Python-based conversational AI chatbot specialized in cybersecurity with adaptive learning capabilities.

## Features

- **Cybersecurity Expertise**: Specialized knowledge in threat detection, incident response, vulnerability management
- **Adaptive Learning**: Learns from user interactions, corrections, and threat reports
- **User Profiles**: Persistent user security profiles with personalized responses
- **Feedback System**: Real-time feedback collection and answer refinement
- **Threat Reporting**: Structured flow for capturing new threats from users
- **Abuse Detection**: Filters harmful/abusive inputs before processing
- **Admin Dashboard**: Review and approve user corrections and threat reports

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite (configurable for PostgreSQL)
- **ORM**: SQLAlchemy
- **LLM**: Groq API (Llama 3.3 70B)
- **Authentication**: JWT tokens

## Quick Start

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up environment variables:**

   Copy the example file:
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your Groq API key:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   SECRET_KEY=your-secret-key-here
   ```

   Or use export (not recommended for production):
   ```bash
   export GROQ_API_KEY="your-groq-api-key"
   export SECRET_KEY="your-secret-key"
   ```

3. **Run the server:**
```bash
uvicorn main:app --reload
```

4. **Access API docs:** http://localhost:8000/docs

## Security Notes

- **Never commit `.env` files** — they are already in `.gitignore`
- **Keep API keys private** — don't share them or expose in code
- **Rotate keys** if accidentally exposed publicly
- Use strong `SECRET_KEY` in production (generate with: `openssl rand -hex 32`)

## API Endpoints

- `POST /api/v1/chat` - Send a message to the chatbot
- `POST /api/v1/users/profile` - Create/update user profile
- `GET /api/v1/users/{user_id}/profile` - Get user profile
- `POST /api/v1/feedback` - Submit feedback on responses
- `POST /api/v1/threats/report` - Report a new threat
- `GET /api/v1/admin/corrections` - Get pending corrections (admin)
- `GET /api/v1/admin/threats` - Get pending threat reports (admin)
- `POST /api/v1/admin/approve` - Approve correction/threat (admin)
