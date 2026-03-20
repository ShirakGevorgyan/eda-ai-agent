from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import chat, documents


app = FastAPI(title=settings.PROJECT_NAME, version="0.1.0")

app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])

app.include_router(documents.router, prefix="/api/v1/documents", tags=["Documents"])

@app.get("/")
async def root():
    """
    This is the home route. 
    It helps us check if the server is running.
    """
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "status": "Running",
        "model_configured": settings.DEFAULT_MODEL
    }

@app.get("/health")
async def health_check():
    """
    This route shows that the API is healthy and working.
    """
    return {"status": "healthy"}