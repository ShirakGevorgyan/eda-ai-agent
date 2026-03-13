from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.ai_agent.agent import EDAAgent

router = APIRouter()

agent = EDAAgent()
class ChatRequest(BaseModel):
    message: str

@router.post("/send")
async def send_message(request: ChatRequest):
    """
    This function takes the user's message and sends it to the AI Agent.
    Then it returns the AI's answer.
    """
    try:
        response = agent.ask(request.message)
        
        return {
            "user_message": request.message,
            "ai_response": response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))