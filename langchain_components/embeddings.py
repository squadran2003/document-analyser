from typing import List, str
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv


class EmbeddingsManager:
    def __init__(self, model: str = "text-embedding-3-small"):
        load_dotenv()  # Load environment variables from .env file
        self.embeddings = OpenAIEmbeddings(model=model)

    def embed_documents(self, documents: List[str]) -> List[List[float]]:
        return self.embeddings.embed_documents(documents)
