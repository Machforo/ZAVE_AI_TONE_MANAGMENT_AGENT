from app.db.session import SessionLocal as db_session
from app.models.user import User
from sqlalchemy.orm import Session
from app.db.session import get_db

def get_memory(user_id):
    session = db_session()
    user = session.query(User).filter_by(user_id=user_id).first()
    if not user:
        return None
    return {
        "tone_preferences": user.tone_preferences,
        "communication_style": user.communication_style,
        "interaction_history": user.interaction_history
    }

def delete_memory(user_id):
    session = db_session()
    user = session.query(User).filter_by(user_id=user_id).first()
    if not user:
        return False
    user.tone_preferences = {}
    user.communication_style = {}
    user.interaction_history = {}
    session.commit()
    return True

def update_tone_preferences(user_id: str, feedback: str):
    db: Session = next(get_db())
    user = db.query(User).filter_by(user_id=user_id).first()
    if not user:
        return

    prefs = user.tone_preferences or {
        "formality": "balanced",
        "enthusiasm": "medium",
        "verbosity": "balanced",
        "empathy_level": "medium",
        "humor": "none"
    }

    adjustment = {
        "positive": {"enthusiasm": "high", "empathy_level": "high"},
        "neutral": {"enthusiasm": "medium", "empathy_level": "medium"},
        "negative": {"enthusiasm": "low", "empathy_level": "low"}
    }

    if feedback in adjustment:
        for key, value in adjustment[feedback].items():
            prefs[key] = value

    user.tone_preferences = prefs
    db.commit()
