import shutil
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.rag.document_loader import DocumentLoaderService
from app.services.rag.vector_store import VectorStoreService

router = APIRouter()

loader_service = DocumentLoaderService()
vector_service = VectorStoreService()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """
    A1-A2 Level Comments:
    This function gets a file from the user.
    It saves the file to the 'data' folder.
    Then, it adds the file information to the AI's memory.
    """
    upload_path = f"data/{file.filename}"
    
    try:
        with open(upload_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        new_docs = loader_service.load_single_document(upload_path)
        
        if not new_docs:
            raise HTTPException(status_code=400, detail="Could not read the file.")

        vector_service.add_documents(new_docs)
        
        return {"message": f"File '{file.filename}' uploaded and indexed successfully!"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))