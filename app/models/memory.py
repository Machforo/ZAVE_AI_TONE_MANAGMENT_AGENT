from sqlalchemy import Column, String, JSON, DateTime
from app.db.base import Base
from datetime import datetime

class Memory(Base):
    __tablename__ = 'memory'

    user_id = Column(String, primary_key=True)
    long_term_memory = Column(JSON)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
