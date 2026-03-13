from fastapi import APIRouter

router = APIRouter()

@router.post("/send")
async def send_message(message: str):
    """
    This route will receive a message from the user.
    For now, it just returns the same message back.
    """
    return {
        "user_message": message,
        "ai_response": f"I received your message: '{message}'. Soon I will use AI to answer!"
    }