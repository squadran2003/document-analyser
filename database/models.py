"""
SQLAlchemy ORM Models for Document Analysis System

This module defines the database schema using SQLAlchemy ORM.

Key Concepts:
- Document: Stores metadata about uploaded documents
- DocumentChunk: Stores text chunks with vector embeddings for semantic search
- pgvector: PostgreSQL extension for efficient vector similarity search
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from .connection import Base


class Document(Base):
    """
    Document model - stores metadata about uploaded files

    Attributes:
        id: Primary key
        filename: Original filename
        file_type: File extension (pdf, docx, txt)
        upload_date: Timestamp of upload
        summary: AI-generated summary of the document
        metadata: Additional JSON metadata (file size, page count, etc.)
        chunks: Relationship to DocumentChunk (one-to-many)
    """
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    file_type = Column(String(50))
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    summary = Column(Text, nullable=True)
    metadata = Column(JSON, default={})

    # Relationship to chunks - allows document.chunks to access all chunks
    chunks = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan"  # Delete chunks when document is deleted
    )

    def __repr__(self):
        return f"<Document(id={self.id}, filename='{self.filename}')>"


class DocumentChunk(Base):
    """
    DocumentChunk model - stores text chunks with vector embeddings

    This is the core table for semantic search. Each chunk represents a portion
    of a document with its corresponding vector embedding.

    Attributes:
        id: Primary key
        document_id: Foreign key to documents table
        chunk_text: The actual text content of this chunk
        chunk_index: Order of this chunk in the document (0, 1, 2, ...)
        embedding: Vector embedding (1536 dimensions for OpenAI embeddings)
        metadata: Additional JSON metadata (page number, section, etc.)
        created_at: Timestamp of creation
        document: Relationship back to Document

    Why chunking?
    - LLMs have token limits
    - Smaller chunks give more precise retrieval
    - Better semantic search accuracy

    Why embeddings?
    - Convert text to numerical vectors
    - Capture semantic meaning
    - Enable similarity search (find similar content)
    """
    __tablename__ = "document_chunks"

    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(
        Integer,
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    chunk_text = Column(Text, nullable=False)
    chunk_index = Column(Integer, nullable=False)

    # Vector column - pgvector type for similarity search
    # 1536 is the dimension for OpenAI's text-embedding-3-small model
    embedding = Column(Vector(1536))

    metadata = Column(JSON, default={})
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationship back to document
    document = relationship("Document", back_populates="chunks")

    def __repr__(self):
        preview = self.chunk_text[:50] + "..." if len(self.chunk_text) > 50 else self.chunk_text
        return f"<DocumentChunk(id={self.id}, doc_id={self.document_id}, text='{preview}')>"
