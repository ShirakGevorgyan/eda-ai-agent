import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    """
    This class holds all the configuration for our project.
    We use it to easily access our API keys and project settings.
    """
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "EDA AI Agent")
    VECTOR_DB_DIR: str = os.getenv("VECTOR_DB_DIR", "./chroma_db")

    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gpt-4o")

    LOCAL_MODEL_NAME: str = os.getenv("LOCAL_MODEL_NAME", "llama3")
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")

    AVAILABLE_MODELS: list = [DEFAULT_MODEL, "gpt-3.5-turbo", LOCAL_MODEL_NAME]

settings = Settings()