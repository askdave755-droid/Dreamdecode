from sqlalchemy import Column, String, DateTime, Boolean, Integer, Text
from sqlalchemy.sql import func
import uuid
from database import Base

def generate_uuid():
    return str(uuid.uuid4())

class Dream(Base):
    __tablename__ = "dreams"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    dream_text = Column(Text, nullable=False)
    emotion = Column(String(50))
    colors = Column(String(100))
    symbols = Column(String(200))
    
    # Report data
    teaser = Column(Text)
    full_report = Column(Text)  # Stored as JSON string
    
    # Referral system
    referral_code = Column(String(8), unique=True, default=lambda: str(uuid.uuid4())[:8])
    referred_by = Column(String, nullable=True)  # ID of referrer
    referral_count = Column(Integer, default=0)
    discount_applied = Column(Boolean, default=False)
    
    # Payment tracking
    status = Column(String(20), default="pending")  # pending, paid, failed
    paid_at = Column(DateTime)
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
