import logging
from typing import List, Optional

from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.repositories.url_repository import URLRepository
from app.schemas.url import URLCreate
from app.models.url import URL
from app.utils import encode_base62

logger = logging.getLogger(__name__)

class URLService:
    def __init__(self, url_repo: URLRepository):
        self.url_repo = url_repo
        
    def create_short_url(self, url_in: URLCreate) -> URL:
        """Uses flush/refresh for atomic ID generation and updates the short_code."""
        temp_code = "TEMP"
        
        try:
            db_url = self.url_repo.create_url(url_in, temp_code)
            
            # FIX: Force SQLAlchemy to assign the ID without committing (using flush/refresh).
            self.url_repo.db.flush()
            self.url_repo.db.refresh(db_url) 
            
            short_code = encode_base62(db_url.id)
            db_url.short_code = short_code
            
            # FINAL COMMIT: Commit both the insert and the update atomically.
            self.url_repo.db.commit()
            self.url_repo.db.refresh(db_url)
            
            return db_url
        
        except Exception as e:
            # FIX: Rollback on ANY failure
            self.url_repo.db.rollback() 
            logger.error(f"DB error during URL creation: {e}")
            
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"status": "failure", "message": "Internal server error during link creation."}
            )

    # Bob will implement get_original_url later, but we need a stub for now.
    def get_original_url(self, short_code: str) -> URL:
        db_url = self.url_repo.get_url_by_code(short_code)
        if not db_url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail={"status": "failure", "message": "URL not found."}
            )
        return db_url

    def get_all_urls(self) -> List[URL]:
        return self.url_repo.get_all_urls()
    
    # Bob will implement delete_short_url later, but we need a stub for now.
    def delete_short_url(self, short_code: str) -> None:
        try:
            is_deleted = self.url_repo.delete_url_by_code(short_code)
            
            if not is_deleted:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, 
                    detail={"status": "failure", "message": "URL not found."}
                )
            
            self.url_repo.db.commit()

        except HTTPException:
            self.url_repo.db.rollback()
            raise
        except Exception:
            self.url_repo.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"status": "failure", "message": "Internal server error during deletion."}
            )
