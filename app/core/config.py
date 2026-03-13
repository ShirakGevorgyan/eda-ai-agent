import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "EDA AI Agent")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "llama3")
    
settings = Settings()