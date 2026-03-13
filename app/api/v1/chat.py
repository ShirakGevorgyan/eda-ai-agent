from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_agent.agent import EDAAgent
from app.core.config import settings

import time
import json
import os
from datetime import datetime

# Create a router for chat API
router = APIRouter()

# Initialize our EDA Agent
agent = EDAAgent()

class ChatRequest(BaseModel):
    """
    A1-A2 Level:
    This is the structure of the user's request.
    It includes the message and the AI model name.
    """
    message: str
    model_name: str = settings.DEFAULT_MODEL

@router.post("/send")
async def send_message(request: ChatRequest):
    """
    A1-A2 Level:
    1. Start a timer to check speed.
    2. Ask the AI Agent for an answer using the selected model.
    3. Save the result and time to a log file.
    4. Return the answer and performance to the UI.
    """
    start_time = time.time()
    
    try:
        # We pass both message AND model_name to our dynamic agent
        response = agent.ask(
            question=request.message, 
            model_name=request.model_name
        )
        
        # Calculate how many seconds it took
        end_time = time.time()
        duration = round(end_time - start_time, 2)

        # Ensure the logs directory exists
        if not os.path.exists("logs"):
            os.makedirs("logs")

        # Prepare the information for the log file
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "model": request.model_name,
            "question": request.message,
            "duration_sec": duration,
            "status": "success"
        }

        # Save the log entry as a new line in chat_history.log
        with open("logs/chat_history.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        return {
            "user_message": request.message, 
            "ai_response": response,
            "performance": f"{duration}s"
        }
        
    except Exception as e:
        # If there is an error, log the failure
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "model": request.model_name,
            "question": request.message,
            "error": str(e),
            "status": "failed"
        }
        with open("logs/chat_history.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
            
        raise HTTPException(status_code=500, detail=str(e))