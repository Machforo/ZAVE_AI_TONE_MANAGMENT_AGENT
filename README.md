# 🤖 ZAVE AI – Tone Adaptive Conversational Agent

ZAVE AI is an intelligent tone-aware conversational agent built using **Flask**, **FAISS**, **GROQ LLMs**, and **Streamlit**. It dynamically adapts tone and style based on real-time interactions, memory, and user preferences to provide personalized communication experiences.

---

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Machforo/ZAVE_AI_TONE_MANAGEMENT_AGENT.git
cd ZAVE_AI_TONE_MANAGEMENT_AGENT
```

### 2. Install the dependencies

```bash
pip install -r requirements.txt
```

### 3. Initialize Database

```bash
python init_db.py
```

### 4. Start th Flask Backend

```bash
python run.py
```

### 5. Start the streamlit Frontend

```bash
streamlit run frontend.py
```
✅ Make sure tone_aidb (SQLite DB) and faiss_index/ are present in the root.

## System Architecture
```
ZAVE_AI_TONE_MANAGEMENT_AGENT/
│
├── app/                    # App entry point and config
│
├── db/                     # SQLAlchemy base and DB session
│   ├── base.py
│   └── session.py
│
├── models/                 # ORM models for user, message, memory
│   ├── conversation.py
│   ├── memory.py
│   ├── message.py
│   └── user.py
│
├── routes/                 # Flask route definitions
│   ├── chats.py
│   ├── memory.py
│   └── user_routes.py
│
├── services/               # Business logic and orchestration
│   ├── chat_service.py
│   ├── faiss_service.py
│   ├── groq_tone_classifier.py
│   ├── llm_service.py
│   ├── memory_service.py
│   └── user_service.py
│
├── utils/
│   └── vector_store.py     # FAISS vector indexing/searching
│
├── frontend.py             # Streamlit chat interface
├── run.py                  # Run Flask backend
├── init_db.py              # Initialize DB and tables
├── tone_aidb               # SQLite DB
├── faiss_index/            # FAISS vector indices
├── POSTMAN.json            # API collection for testing
├── requirements.txt
└── README.md
```

## 🧠 Tone Adaptation Logic

### 🔍 Tone Classification
-> Uses GROQ LLM to classify input message tone (zero-shot prompting)

-> Classifier resides in groq_tone_classifier.py


### 💾 Memory-Based Personalization
-> FAISS retrieves previous user messages using sentence-transformer embeddings

-> Top relevant responses guide context-aware tone generation


### 📊 Dynamic Adaptation Flow
```
User Input ➜ GROQ Tone Classification
           ➜ Memory Retrieval via FAISS
           ➜ Context Construction
           ➜ Tone-Adaptive LLM Response
           ➜ Memory Update + Feedback Logging

```

### 👍 Feedback Loop
-> Users can give thumbs up/down via frontend

-> Feedback updates tone memory (memory.py) for better future responses


### 📡 API Guide

## 🧠 POST /api/chats
Get a contextual, tone-adaptive response from the chatbot.

REQUEST
```json

{
  "user_id": "user123",
  "user_input": "How do I prepare for a promotion?",
  "context": "career"
}
```


RESPONSE

```json
{
  "response": "Here are some effective ways to position yourself for a promotion...",
  "tone_applied": {
    "formality": "professional",
    "enthusiasm": "moderate",
    "verbosity": "detailed"
  },
  "conversation_id": "conv123",
  "memory_updated": true
}
```


## 👤 POST /api/users
Create or update a user profile.

```json
{
  "user_id": "user123",
  "name": "Riya",
  "email": "riya@example.com"
}
```

## 📄 GET /api/users/<user_id>
Retrieve a specific user's profile and tone preferences.

## 💾 POST /api/memory/tone-feedback
Submit tone feedback for memory training.

```json
{
  "user_id": "user123",
  "conversation_id": "conv123",
  "feedback": "positive"
}
```



## Sample Test

## ✅ 1. POST /api/chats

REQUEST
```json
POST /api/chats

{
  "user_id": "user123",
  "user_input": "Hey, I need help writing a professional email.",
  "conversation_id": "",
  "feedback_on_previous": "positive"
}
```

RESPONSE
```json

{
    "conversation_id": "36795b4a-baaf-4654-a734-12f025a4b75d",
    "memory_updated": true,
    "response": "What's the email about and who's it to? That'll help me give you a better template.",
    "tone_applied": {
        "empathy_level": "low",
        "enthusiasm": "low",
        "formality": "casual",
        "humor": "none",
        "verbosity": "concise"
    }
}

```


## ✅ 2. GET /api/chats

REQUEST
```json
GET /api/chats
```
RESPONSE
```json

{
    "conversations": [
        {
            "conversation_id": "e8020d78-5aa5-4e46-b844-9669aa12bc79",
            "user_id": "user123"
        },
        {
            "conversation_id": "ad7c3c54-2e58-44cc-af2e-87f04271f111",
            "user_id": "user1234"
        }
    ]
}

```

## ✅ 3. GET /api/chats/{chat_id}

REQUEST
```json
GET /api/chats/chat_id
```
RESPONSE
```json
{
    "conversation_id": "e8020d78-5aa5-4e46-b844-9669aa12bc79",
    "messages": [
        {
            "id": "c5b47778-7de6-4b1e-9013-8125935af05e",
            "sender": "user",
            "text": "Hey, I need help writing a professional email.",
            "timestamp": "2025-08-06T17:49:46.015107",
            "tone_feedback": "{\"formality\": \"casual\", \"enthusiasm\": \"low\", \"verbosity\": \"concise\", \"empathy_level\": \"low\", \"humor\": \"none\"}"
        },
        {
            "id": "1643c4ff-275d-4a1e-896e-1de98c77956e",
            "sender": "assistant",
            "text": "To write a good email, I'll need some more info. Can you tell me:\n\n1. What's the email about?\n2. Who is the email to (e.g. coworker, manager, client)?\n3. What's the purpose of the email (e.g. request, update, question)?\n4. Are there any specific details or attachments you need to include?\n\nOnce I have this info, I can help you create a template.",
            "timestamp": "2025-08-06T17:49:46.053525",
            "tone_feedback": null
        }
    ]
}

```


## ✅ 4. POST /api/users

REQUEST
```json
POST /api/users

{
  "user_id": "user123456",
  "name": "Jane",
  "email": "jane@example.com",
  "location": "NYC",
  "tone_preferences": {
    "formality": "casual",
    "enthusiasm": "low"
  },
  "communication_style": "empathetic"
}

```

RESPONSE
```json
{
    "message": "User created or updated successfully",
    "user_id": "user_123456"
}

```

## ✅ 5. GET /api/users/{user_id}

REQUEST
```json
GET /api/users/user_id
```
RESPONSE
```json
{
    "communication_style": {
        "verbose": true
    },
    "email": "john@example.com",
    "interaction_history": {},
    "location": "New York",
    "name": "John Doe",
    "tone_preferences": {
        "default": "friendly"
    },
    "user_id": "user_123456"
}
```

## ✅ 6. GET /api/memory/{user_id}

REQUEST
```json
GET /api/memory/user_id
```
RESPONSE
```json
{
    "communication_style": {
        "verbose": true
    },
    "interaction_history": {},
    "tone_preferences": {
        "default": "friendly"
    }
}
```

## ✅ 7. DELETE /api/memory/{user_id}

REQUEST
```json
DELETE /api/memory/user_id
```
RESPONSE
```json
{
  "message": "Memory cleared successfully"
}
```


### 💬 Frontend Features (Streamlit)
🔐 User authentication (via user_id)

💬 Chat UI with LLM responses

🎭 Auto-tone detection (no manual selection)

👍👎 Thumbs up/down feedback

📝 Chat summary when session ends (e.g., user says “bye”)


### 🧪 Testing
Use POSTMAN.json to test all API endpoints. Import into Postman and run interactively.


👨‍💻 Authors
Built  by Atharv Kumar 

Powered by GROQ, FAISS, Flask, and Streamlit

Linkedin: https://www.linkedin.com/in/atharv-kumar-270337222/
