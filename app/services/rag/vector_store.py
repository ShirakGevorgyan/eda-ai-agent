import os
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma 
from app.core.config import settings

class VectorStoreService:
    """
    This service helps our AI remember information.
    It turns text into numbers (vectors) and saves them in a database.
    """

    def __init__(self):
        # We use OpenAI to convert text to numbers
        # api_key: our secret key for OpenAI
        self.embeddings = OpenAIEmbeddings(api_key=settings.OPENAI_API_KEY)
        
        # This is the folder where we save our database files
        self.db_dir = settings.VECTOR_DB_DIR

    def add_documents(self, documents):
        """
        This function takes text chunks and saves them in the memory.
        """
        print(f"Adding {len(documents)} chunks to the vector store...")
        
        # Chroma is our database. We give it:
        # 1. Our text chunks (documents)
        # 2. Our embedding model (self.embeddings)
        # 3. The folder to save the data (persist_directory)
        vector_db = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.db_dir
        )
        return vector_db

    def get_retriever(self):
        """
        This function helps us search for information in our memory.
        """
        # We open the existing database from the folder
        vector_db = Chroma(
            persist_directory=self.db_dir, 
            embedding_function=self.embeddings
        )
        
        # We return a 'retriever'. 
        # k=3 means: Find the 3 most similar pieces of information for our question.
        return vector_db.as_retriever(search_kwargs={"k": 3})