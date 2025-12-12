from fastapi import FastAPI
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO)

from app.api.url_router import router as url_router

app = FastAPI(
    title="URL Shortener Midterm Project",
    version="0.1.0",
    description="Backend service for shortening URLs using FastAPI and PostgreSQL.",
)

@app.get("/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "ok"}

# Include the router
app.include_router(url_router, prefix="")
