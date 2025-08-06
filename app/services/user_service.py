from app.models.user import User
#from app.db.session import SessionLocal
from sqlalchemy.exc import IntegrityError
from datetime import datetime
from app.db.session import SessionLocal as db_session
#from app.models.user import User

from app.db.session import SessionLocal as db_session
from app.models.user import User

def create_or_update_user(data):
    session = db_session()
    user = session.query(User).filter_by(user_id=data["user_id"]).first()
    if not user:
        user = User(user_id=data["user_id"])
    user.name = data.get("name")
    user.email = data.get("email")
    user.avatar_url = data.get("avatar_url")
    user.location = data.get("location")
    user.tone_preferences = data.get("tone_preferences", {})
    user.communication_style = data.get("communication_style", {})
    user.interaction_history = data.get("interaction_history", {})
    session.add(user)
    session.commit()
    session.close()
    return {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "tone_preferences": user.tone_preferences
    }

def get_user_by_id(user_id):
    session = db_session()
    user = session.query(User).filter_by(user_id=user_id).first()
    if not user:
        return None
    return {
        "user_id": user.user_id,
        "name": user.name,
        "email": user.email,
        "location": user.location,
        "tone_preferences": user.tone_preferences,
        "communication_style": user.communication_style,
        "interaction_history": user.interaction_history
    }