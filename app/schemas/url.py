from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, Literal 


class URLCreate(BaseModel):
    """Schema for creating a new short URL."""
    original_url: HttpUrl = Field(..., description="The original long URL to shorten.")

class URLBase(BaseModel):
    """Base schema for a short URL record."""
    id: int
    original_url: str
    short_code: str
    created_at: datetime

    class Config:
        from_attributes = True

class URLResponse(BaseModel):
    """Schema for a standard successful API response."""
    status: Literal["success"] = "success" 
    data: Optional[URLBase] = None
    message: Optional[str] = None

class URLListResponse(BaseModel):
    """Schema for a successful API response returning a list of URLs."""
    status: Literal["success"] = "success"
    data: list[URLBase] = []
    message: Optional[str] = None
