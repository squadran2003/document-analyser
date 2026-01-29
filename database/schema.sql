-- Enable pgvector extension for vector operations
-- This needs to run before SQLAlchemy creates tables
CREATE EXTENSION IF NOT EXISTS vector;
