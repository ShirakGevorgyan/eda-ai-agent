from app.core.config import settings

print(f"--- Project Information ---")
print(f"Project Name: {settings.PROJECT_NAME}")

print(f"Model Name: {settings.MODEL_NAME}")

if settings.OPENAI_API_KEY:
    safe_key = settings.OPENAI_API_KEY[:7] + "****************"
    print(f"API Key: Found! ({safe_key})")
else:
    print(f"API Key: NOT FOUND! Check your .env file.")

print(f"Vector DB Folder: {settings.VECTOR_DB_DIR}")
print(f"---------------------------")