from typing import List                                                                                                                       
from pathlib import Path                                                                                                                      
from langchain_core.documents import Document                                                                                                 
from langchain_community.document_loaders import PyPDFLoader, TextLoader, Docx2txtLoader                                                      
from langchain.text_splitter import RecursiveCharacterTextSplitter  


class DocumentProcessor:
    def __init__(self, chunk_size=1000, chunk_overlap=200):
        self.chunk_size = chunk_size
        self.overlap = chunk_overlap

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.overlap,
            separators=["\n\n", "\n", " ", ""]
        )

    def split_documents(self, documents: List[Document]) -> List[Document]:                                                          
        chunks = self.text_splitter.split_documents(documents)                                                                            
        return chunks

    def process_file(self, file_path: str) -> List[Document]:                                                                                     
        # 1. Load document                                                                                                                        
        documents = self.load_document(file_path)                                                                                                 
        # 2. Split into chunks                                                                                                                    
        chunks = self.split_documents(documents)                                                                                                  
        # 3. Print info                                                                                                                           
        print(f"Created {len(chunks)} chunks")                                                                                                    
        return chunks   

    def load_document(self, file_path):
        path = Path(file_path)                                                                                                                    
        file_extension = path.suffix.lower()  # Gets '.pdf', handles uppercase

        if file_extension == '.pdf':
            loader = PyPDFLoader(file_path)
            content = loader.load()
        elif file_extension == '.txt':
            loader = TextLoader(file_path)
            content = loader.load()
        elif file_extension == '.docx':
            loader = Docx2txtLoader(file_path)
            content = loader.load()
        else:
            raise ValueError("Unsupported file format")
        return content