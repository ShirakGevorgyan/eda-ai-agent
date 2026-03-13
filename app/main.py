from fastapi import FastAPI
from app.core.config import settings
from app.api.v1 import chat


app = FastAPI(title=settings.PROJECT_NAME, version="0.1.0")

# Include the chat router in our app
# All chat routes will now start with /api/v1/chat
app.include_router(chat.router, prefix="/api/v1/chat", tags=["Chat"])


@app.get("/")
async def root():
    """
    This is the home route. 
    It helps us check if the server is running.
    """
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "status": "Running",
        "model_configured": settings.MODEL_NAME
    }

@app.get("/health")
async def health_check():
    """
    This route shows that the API is healthy and working.
    """
    return {"status": "healthy"}