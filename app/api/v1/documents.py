import os
import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.rag.document_loader import DocumentLoaderService
from app.services.rag.vector_store import VectorStoreService

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    This function allows the user to upload a file (Verilog, SDC, or PDF).
    1. It saves the file in the 'data' folder.
    2. It reads the file content.
    3. It adds the information to the AI's memory (Vector Database).
    """
    if not os.path.exists("data"):
        os.makedirs("data")

    upload_path = f"data/{file.filename}"
    
    try:
        #Save the file from the user's computer to our server
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        loader_service = DocumentLoaderService()
        vector_service = VectorStoreService()

        # Load the new document and split it into small pieces (chunks)
        new_docs = loader_service.load_single_document(upload_path)
        if new_docs:
            vector_service.add_documents(new_docs)
            return {"message": "Successfully indexed"}
        else:
            return {"message": "File is empty or not supported"}
            
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))