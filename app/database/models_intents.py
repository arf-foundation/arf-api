from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, JSON, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
import datetime
from .base import Base

class IntentDB(Base):
    __tablename__ = "intents"
    id = Column(Integer, primary_key=True, index=True)
    deterministic_id = Column(String(64), unique=True, index=True, nullable=False)
    intent_type = Column(String(64), nullable=False)
    payload = Column(JSON, nullable=False)
    oss_payload = Column(JSON, nullable=True)
    environment = Column(String(32), nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    evaluated_at = Column(DateTime, nullable=True)
    risk_score = Column(String(32), nullable=True)
    outcomes = relationship("OutcomeDB", back_populates="intent", cascade="all, delete-orphan")

class OutcomeDB(Base):
    __tablename__ = "intent_outcomes"
    id = Column(Integer, primary_key=True, index=True)
    intent_id = Column(Integer, ForeignKey("intents.id", ondelete="CASCADE"), nullable=False)
    success = Column(Boolean, nullable=False)
    recorded_by = Column(String(128), nullable=True)
    notes = Column(Text, nullable=True)
    recorded_at = Column(DateTime, default=datetime.datetime.utcnow, nullable=False)
    intent = relationship("IntentDB", back_populates="outcomes")

    __table_args__ = (
        UniqueConstraint("intent_id", name="uq_outcome_intentid"),
    )
