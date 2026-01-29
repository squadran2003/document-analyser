"""
Database initialization script

Run this script to:
1. Enable pgvector extension
2. Create all tables defined in models.py
3. Create necessary indexes

Usage:
    python -m database.init_db
"""
from sqlalchemy import text
from .connection import engine, Base
from .models import Document, DocumentChunk


def init_database():
    """Initialize database with pgvector extension and create tables"""

    print("🔧 Initializing database...")

    # Create pgvector extension
    with engine.connect() as conn:
        print("📦 Enabling pgvector extension...")
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()

    # Create all tables
    print("📋 Creating tables...")
    Base.metadata.create_all(bind=engine)

    # Create vector index for similarity search
    with engine.connect() as conn:
        print("🔍 Creating vector similarity index...")
        # IVFFlat index for fast approximate nearest neighbor search
        conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_chunks_embedding
            ON document_chunks
            USING ivfflat (embedding vector_cosine_ops)
            WITH (lists = 100)
        """))
        conn.commit()

    print("✅ Database initialized successfully!")


if __name__ == "__main__":
    init_database()
