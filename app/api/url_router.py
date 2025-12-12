from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from typing import List
import logging

from app.services.url_service import URLService
from app.dependencies import get_url_service
from app.schemas.url import URLCreate, URLResponse, URLBase, URLListResponse
from app.models.url import URL

logger = logging.getLogger(__name__)
router = APIRouter()

# 1. POST /urls: Create Short Link (Alice's Feature)
@router.post(
    "/urls", 
    response_model=URLResponse, 
    status_code=status.HTTP_201_CREATED,
    tags=["URLs"]
)
def create_url(
    url_in: URLCreate,
    url_service: URLService = Depends(get_url_service)
):
    """Creates a new short URL from a long URL."""
    try:
        db_url: URL = url_service.create_short_url(url_in)
        return URLResponse(
            data=URLBase.model_validate(db_url),
            message="Short URL created successfully."
        )
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "failure", "message": "An unexpected error occurred."}
        )

# 2. GET /urls: View All Shortened Links (Alice's Feature)
@router.get(
    "/urls",
    response_model=URLListResponse,
    status_code=status.HTTP_200_OK,
    tags=["URLs"]
)
def get_all_urls(
    url_service: URLService = Depends(get_url_service)
):
    """Retrieves a list of all shortened URLs."""
    try:
        db_urls: List[URL] = url_service.get_all_urls()
        
        url_schemas = [URLBase.model_validate(url) for url in db_urls]
        
        return URLListResponse(
            data=url_schemas,
            message="Successfully retrieved all short URLs."
        )
    except Exception as e:
        logger.error(f"Error fetching all URLs: {e}") 
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "failure", "message": "An unexpected error occurred while fetching URLs."}
        )

# 3. GET /u/{code}: Redirect to Original URL (Bob's Feature)
@router.get(
    "/u/{code}",
    status_code=status.HTTP_302_FOUND,
    tags=["Redirects"],
)
def redirect_to_original_url(
    code: str,
    url_service: URLService = Depends(get_url_service)
):
    """Retrieves the original URL and redirects the user."""
    try:
        db_url: URL = url_service.get_original_url(code)
        
        return RedirectResponse(url=str(db_url.original_url), status_code=status.HTTP_302_FOUND)
    except HTTPException as e:
        # Returns the 404 response as JSON, as defined in the service
        return JSONResponse(status_code=e.status_code, content=e.detail) 
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "failure", "message": "An unexpected error occurred."}
        )

# 4. DELETE /urls/{code}: Delete Short Link (Bob's Feature)
@router.delete(
    "/urls/{code}",
    response_model=URLResponse,
    status_code=status.HTTP_200_OK,
    tags=["URLs"]
)
def delete_url(
    code: str,
    url_service: URLService = Depends(get_url_service)
):
    """Deletes a short URL by its short code."""
    try:
        url_service.delete_short_url(code)
        
        return URLResponse(
            message="URL deleted successfully.", 
            status="success"
        )
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "failure", "message": "An unexpected error occurred during deletion."}
        )
