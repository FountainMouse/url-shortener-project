from fastapi import Depends
from sqlalchemy.orm import Session

from app.utils import get_db
from app.repositories.url_repository import URLRepository
from app.services.url_service import URLService

def get_url_repository(db: Session = Depends(get_db)) -> URLRepository:
    return URLRepository(db)

def get_url_service(url_repo: URLRepository = Depends(get_url_repository)) -> URLService:
    return URLService(url_repo)
