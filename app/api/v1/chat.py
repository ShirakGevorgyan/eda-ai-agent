from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_agent.agent import EDAAgent

import time
import json
from datetime import datetime

router = APIRouter()

agent = EDAAgent()
class ChatRequest(BaseModel):
    message: str
    model_name: str = "gpt-4o"

@router.post("/send")
async def send_message(request: ChatRequest):
    start_time = time.time() # Start timer
    
    try:
        agent.llm.model_name = request.model_name 
        response = agent.ask(request.message)
        
        end_time = time.time() # End timer
        duration = round(end_time - start_time, 2) # Time in seconds

        # Create a log entry
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "model": request.model_name,
            "question": request.message,
            "duration_sec": duration,
            "status": "success"
        }

        # Save log to a file
        with open("logs/chat_history.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        return {
            "user_message": request.message, 
            "ai_response": response,
            "performance": f"{duration}s"
        }
        
    except Exception as e:
        # Log error
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