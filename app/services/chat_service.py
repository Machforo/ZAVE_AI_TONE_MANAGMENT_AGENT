import uuid, os, requests
from collections import Counter
from datetime import datetime
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.user import User
from app.services.faiss_service import generate_embedding, add_message_to_faiss, search_similar_messages
import json
from app.services.memory_service import update_tone_preferences   

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def detect_tone(messages):
    tones = [m.tone_feedback for m in messages if m.tone_feedback]
    return Counter(tones).most_common(1)[0][0] if tones else "neutral"

def generate_llm_response(context, user_input, tone):
    system = f"You are a helpful AI that responds in a '{tone}' tone."
    msgs = [{"role":"system","content":system}] + \
           [{"role": meta.get("sender","user"), "content": meta["text"]} for meta in context]
    msgs.append({"role":"user","content":user_input})
    resp = requests.post(GROQ_API_URL, headers={"Authorization":f"Bearer {GROQ_API_KEY}", "Content-Type":"application/json"},
                         json={"model":"llama-3.1-8b-instant","messages":msgs,"temperature":0.7})
    return resp.json().get("choices",[{}])[0].get("message",{}).get("content","Sorry, error.")

def get_or_create_user(db: Session, user_id: str):
    user = db.query(User).filter(User.user_id==user_id).first()
    if not user:
        user = User(user_id=user_id, tone_preferences={}, communication_style={}, interaction_history={})
        db.add(user); db.commit(); db.refresh(user)
    return user

from app.services.groq_tone_classifier import detect_tone_with_groq  # import this at the top

def create_or_respond(conversation_id: str, user_id: str, user_input: str, tone_feedback=None):
    print(f"\n🔄 [create_or_respond] Called with user_id={user_id}, input='{user_input}', tone_feedback='{tone_feedback}'")
    db: Session = next(get_db())
    user = get_or_create_user(db, user_id)

    # Ensure interaction_history dict is safely initialized with all expected keys
    default_history = {
        "total_interactions": 0,
        "successful_tone_matches": 0,
        "feedback_score": 0,
        "last_interaction": datetime.utcnow().isoformat()
    }

    if user.interaction_history is None:
        user.interaction_history = default_history
    else:
        for key, val in default_history.items():
            if key not in user.interaction_history:
                user.interaction_history[key] = val

    # ✅ Apply tone feedback to adjust user tone preferences (NEW)
    if tone_feedback:
        update_tone_preferences(user.user_id, tone_feedback)

    # Create new conversation if needed
    if conversation_id:
        conv = db.query(Conversation).filter_by(id=conversation_id).first()
    else:
        conv = Conversation(id=str(uuid.uuid4()), user_id=user.user_id, started_at=datetime.utcnow())
        db.add(conv)
        db.commit()
        db.refresh(conv)

    # Embedding and context
    new_emb = generate_embedding(user_input)
    context = search_similar_messages(user.user_id, user_input, top_k=5)

    # Tone detection using GROQ
    tone = detect_tone_with_groq(user_input)
    print('TONE')

    # Generate LLM response
    reply = generate_llm_response(context, user_input, tone)

    # Save user and bot messages
    for snd, txt, tf in [("user", user_input, tone), ("assistant", reply, None)]:
        msg = Message(
            id=str(uuid.uuid4()),
            conversation_id=conv.id,
            sender=snd,
            text=txt,
            timestamp=datetime.utcnow(),
            tone_feedback=json.dumps(tf) if snd == "user" else None
        )
        db.add(msg)
        add_message_to_faiss(user.user_id, msg.id, txt)

    # Update interaction history
    user.interaction_history["total_interactions"] += 1
    user.interaction_history["last_interaction"] = datetime.utcnow().isoformat()

    db.commit()

    return {
        "response": reply,
        "tone_applied": user.tone_preferences or tone,
        "memory_updated": True,
        "conversation_id": conv.id
    }



def get_history(conv_id: str):
    db: Session = next(get_db())
    conv = db.query(Conversation).filter_by(id=conv_id).first()
    if not conv: return None
    return [{"id":m.id, "sender":m.sender, "text":m.text, "tone_feedback":m.tone_feedback, "timestamp":m.timestamp.isoformat()} for m in conv.messages]


from app.db.session import SessionLocal as db_session 
from app.models.conversation import Conversation

def get_all_conversations():
    db: Session = next(get_db())
    conversations = db.query(Conversation).all()
    return [
        {
            "conversation_id": conv.id,
            "user_id": conv.user_id,
            #"created_at": conv.created_at,
            #"updated_at": conv.updated_at
        }
        for conv in conversations
    ]
