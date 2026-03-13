from fastapi import FastAPI
from app.core.config import settings

# Create the main FastAPI application object
# title: We get the name from our config settings
app = FastAPI(title=settings.PROJECT_NAME, version="0.1.0")

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