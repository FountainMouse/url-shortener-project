from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.schema import UniqueConstraint

from app.models.base import Base

class URL(Base):
    __tablename__ = "urls"
    
    id = Column(Integer, primary_key=True, index=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String(10), unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint('short_code'),
    )

    def __repr__(self):
        return f"<URL(original_url='{self.original_url}', short_code='{self.short_code}')>"
