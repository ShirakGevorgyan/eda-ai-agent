import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    This class holds all the configuration for our project.
    We use it to easily access our API keys and project settings.
    """
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "EDA AI Agent")

    MODEL_NAME: str = os.getenv("MODEL_NAME", "gpt-4o")
    
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    
    VECTOR_DB_DIR: str = os.getenv("VECTOR_DB_DIR", "./chroma_db")

settings = Settings()