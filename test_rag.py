from langchain_components.vector_store import VectorStorageManager                                                            
from langchain_components.rag_chain import RAGChain                                                                           
import os                                                                                                                     
from dotenv import load_dotenv                                                                                                
                                                                                                                            
load_dotenv()                                                                                                                 
                                                                                                                            
# Build connection string (same pattern as your database/connection.py)                                                       
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")                                                                        
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")                                                                
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")                                                                       
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")                                                                            
POSTGRES_DB = os.getenv("POSTGRES_DB", "doc_analyser")                                                                        
                                                                                                                            
CONNECTION_STRING = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"         
                                                                                                                            
# Initialize components                                                                                                       
vector_store = VectorStorageManager(connection_string=CONNECTION_STRING)                                                      
rag = RAGChain(vector_store=vector_store)                                                                                     
                                                                                                                            
test_docs = [                                                                                                                 
      """Python is a high-level programming language known for its simple syntax and readability.",                               
      "Machine learning is a subset of artificial intelligence that enables systems to learn from data.",                       
      "RAG stands for Retrieval-Augmented Generation. It combines document retrieval with LLM generation to answer questions    
  based on specific documents."""                                                                                                
]                                                                                                                             
                                                                                                                                
vector_store.add_documents(test_docs)                                                                                         
print("Documents added!\n")                                                                                                   
                                                                                                                                
# Now ask a specific question                                                                                                 
question = "What is RAG?"                                                                                                     
answer = rag.query(question)                                                                                                  
                                                                                                                                
print(f"Question: {question}")                                                                                                
print(f"Answer: {answer}")              