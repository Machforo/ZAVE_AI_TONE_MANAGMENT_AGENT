from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    started_at = Column(DateTime, default=datetime.utcnow)
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")
    user = relationship("User", back_populates="conversations")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)