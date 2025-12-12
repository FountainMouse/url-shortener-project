from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.url import URL
from app.schemas.url import URLCreate

class URLRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_url(self, url_in: URLCreate, short_code: str) -> URL:
        # FIX: Convert pydantic.HttpUrl to str for psycopg2 compatibility
        original_url_str = str(url_in.original_url) 
        
        db_url = URL(original_url=original_url_str, short_code=short_code)
        self.db.add(db_url)
        return db_url

    def get_url_by_code(self, short_code: str) -> Optional[URL]:
        return self.db.query(URL).filter(URL.short_code == short_code).first()

    def get_all_urls(self) -> List[URL]:
        return self.db.query(URL).all()
        
    def delete_url_by_code(self, short_code: str) -> bool:
        url_record = self.get_url_by_code(short_code)
        if url_record:
            self.db.delete(url_record)
            return True
        return False
