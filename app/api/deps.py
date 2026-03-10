from sqlalchemy.orm import Session
from app.database.session import SessionLocal
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.core.config import settings

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Rate limiter with default limit from settings
limiter = Limiter(key_func=get_remote_address, default_limits=[settings.RATE_LIMIT])
