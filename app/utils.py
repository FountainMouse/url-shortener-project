from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.settings import settings

# --- Database Session Dependency Injection ---

engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Session:
    """Dependency for getting a database session."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Base62 Conversion (ID -> Short Code) ---

ALPHABET = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def encode_base62(num: int) -> str:
    """Encodes an integer (like a DB ID) into a Base62 string."""
    if num == 0:
        return ALPHABET[0]
    
    arr = []
    base = len(ALPHABET)
    
    while num:
        num, rem = divmod(num, base)
        arr.append(ALPHABET[rem])
    
    arr.reverse()
    return ''.join(arr)
