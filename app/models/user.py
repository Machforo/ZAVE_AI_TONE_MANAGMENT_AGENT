from sqlalchemy import Column, String, JSON, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class User(Base):
    __tablename__ = 'users'
    user_id = Column(String, primary_key=True)
    name = Column(String, default="Anonymous")
    email = Column(String, unique=True, nullable=True)
    avatar_url = Column(String, nullable=True)
    location = Column(String, nullable=True)
    tone_preferences = Column(JSON, default=dict)
    communication_style = Column(JSON, default=dict)
    interaction_history = Column(JSON, default=dict)
    conversations = relationship("Conversation", back_populates="user", cascade="all, delete-orphan")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
