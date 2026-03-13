import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # Create 'data' folder if it does not exist
    if not os.path.exists("data"):
        os.makedirs("data")

    upload_path = f"data/{file.filename}"
    
    try:
        # Save the file
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # We need to import these here to avoid circular imports
        from app.services.rag.document_loader import DocumentLoaderService
        from app.services.rag.vector_store import VectorStoreService
        
        loader_service = DocumentLoaderService()
        vector_service = VectorStoreService()

        # Load and Index
        new_docs = loader_service.load_single_document(upload_path)
        if new_docs:
            vector_service.add_documents(new_docs)
            return {"message": "Successfully indexed"}
        else:
            return {"message": "File is empty or not supported"}
            
    except Exception as e:
        print(f"Error: {e}") # This will show in the terminal
        raise HTTPException(status_code=500, detail=str(e))