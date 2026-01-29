from typing import List, Optional
from langchain_postgres import PGVector
from langchain_openai import OpenAIEmbeddings
from langchain_core.documents import Document
from dotenv import load_dotenv


class VectorStorageManager:
    def __init__(self, connection_string: str, collection_name: str="documents"):
        load_dotenv()

        self.collection_name = collection_name
        self.connection_string = connection_string

        self.embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

        self.vector_store = PGVector(
            connection=self.connection_string,
            collection_name=self.collection_name,
            embeddings=self.embeddings,
            use_jsonb=True
        )
    
    def add_documents(self, texts: List[str], metadatas: Optional[List[dict]] = None) -> List:
        """                                                                                                                       
            Store text chunks in the vector store.                                                                                    
                                                                                                                                        
            Args:                                                                                                                     
                texts: List of text chunks to store                                                                                   
                metadatas: Optional list of metadata dicts (e.g., {"source": "file.pdf", "page": 1})                                  
                                                                                                                                        
            Returns:                                                                                                                  
                List of document IDs                                                                                                  
        """

        documents = []

        for i, text in enumerate(texts):
            metadata = metadatas[i] if metadatas and i < len(metadatas) else {}
            documents.append(Document(page_content=text, metadata=metadata))
        
        ids = self.vector_store.add_documents(documents)
        return ids

    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """                                                                                                                       
            Perform a similarity search in the vector store.                                                                          
                                                                                                                                        
            Args:                                                                                                                     
                query: The query string to search for                                                                                 
                k: Number of top similar documents to retrieve
        """

        results = self.vector_store.similarity_search(query, k=k)
        return results
