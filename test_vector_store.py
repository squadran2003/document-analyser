from langchain_components.vector_store import VectorStorageManager                                                            
import os                                                                                                                     
from dotenv import load_dotenv                                                                                                
                                                                                                                        
load_dotenv()                                                                                                                 
                                                                                                                            
# Build connection string                                                                                                     
connection_string = f"""postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}:
{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"""                                                                      
                                                                                                                            
# Initialize                                                                                                                  
manager = VectorStorageManager(connection_string, collection_name="test_docs")                                                
                                                                                                                            
# Add some sample documents                                                                                                   
texts = [                                                                                                                     
    "Python is a programming language known for its simple syntax.",                                                          
    "Machine learning uses algorithms to learn patterns from data.",                                                          
    "PostgreSQL is a powerful open-source relational database.",                                                              
    "Vector databases enable semantic search using embeddings."                                                               
]                                                                                                                             
                                                                                                                            
metadatas = [                                                                                                                 
    {"source": "python_intro.txt"},                                                                                           
    {"source": "ml_basics.txt"},                                                                                              
    {"source": "postgres_guide.txt"},                                                                                         
    {"source": "vector_db.txt"}                                                                                               
]                                                                                                                             
                                                                                                                            
print("Adding documents...")                                                                                                  
ids = manager.add_documents(texts, metadatas)                                                                                 
print(f"Added {len(ids)} documents")                                                                                          
                                                                                                                            
# Test similarity search                                                                                                      
print("\nSearching for: 'How do databases store vectors?'")                                                                   
results = manager.similarity_search("How do databases store vectors?", k=2)                                                   
                                                                                                                            
for i, doc in enumerate(results):                                                                                             
    print(f"\n--- Result {i+1} ---")                                                                                          
    print(f"Content: {doc.page_content}")                                                                                     
    print(f"Source: {doc.metadata.get('source', 'N/A')}") 