import os
from typing import List
from langchain_community.document_loaders import (
    PyPDFLoader, 
    TextLoader, 
    UnstructuredMarkdownLoader
)
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

class DocumentLoaderService:
    """
    This service helps us load different types of files.
    It supports PDF, Text, Verilog (.v), SDC, and Markdown.
    """

    def __init__(self):
        # We split the text into smaller pieces (chunks)
        # chunk_size: How many characters in one piece
        # chunk_overlap: How many characters to repeat from the last piece
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, 
            chunk_overlap=100
        )

    def load_single_document(self, file_path: str) -> List[Document]:
        """
        Load one file based on its extension.
        """
        ext = os.path.splitext(file_path)[-1].lower()
        
        try:
            if ext == ".pdf":
                loader = PyPDFLoader(file_path)
            elif ext in [".v", ".sv", ".sdc", ".tcl", ".txt"]:
                loader = TextLoader(file_path)
            elif ext == ".md":
                loader = UnstructuredMarkdownLoader(file_path)
            else:
                print(f"Unsupported file type: {ext}")
                return []
            
            docs = loader.load()
            return self.text_splitter.split_documents(docs)
            
        except Exception as e:
            print(f"Error loading file {file_path}: {e}")
            return []

    def load_directory(self, directory_path: str) -> List[Document]:
        """
        Load all supported files from a folder.
        """
        all_documents = []
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            if os.path.isfile(file_path):
                all_documents.extend(self.load_single_document(file_path))
        
        return all_documents