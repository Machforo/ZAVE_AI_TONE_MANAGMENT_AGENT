from sqlalchemy import Column, String, DateTime, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base import Base

class Message(Base):
    __tablename__ = "messages"
    id = Column(String, primary_key=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    sender = Column(String, nullable=False)  # 'user' or 'assistant'
    text = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    tone_feedback = Column(String, nullable=True)
    embedding = Column(LargeBinary, nullable=True)
    conversation = relationship("Conversation", back_populates="messages")
