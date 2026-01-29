# Document Analyser - LangChain & LangGraph Learning Project

## Project Overview
A document analysis system where users can upload documents (PDF, DOCX, TXT), get AI-generated summaries, and ask questions about the content. Built to teach LangChain and LangGraph concepts through practical implementation.

## Learning Approach
**You will code, I will guide and review.**
- I'll give you step-by-step instructions for each component
- You write the code based on the requirements
- Ask questions whenever you're stuck or want to understand something better
- When done with each step, let me know and I'll review your code
- We'll iterate and learn from any issues together

## Project Architecture

```
doc_analyser/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration & environment
│   ├── models.py               # Pydantic models
│   └── api/
│       ├── __init__.py
│       └── routes.py           # API endpoints
├── langchain_components/
│   ├── __init__.py
│   ├── document_processor.py   # Document loading & splitting
│   ├── embeddings.py           # Embedding generation
│   ├── vectorstore.py          # PostgreSQL/pgvector integration
│   └── chains.py               # LangChain LCEL chains
├── langgraph_components/
│   ├── __init__.py
│   ├── document_workflow.py    # Document processing graph
│   └── qa_agent.py             # Conversational Q&A agent
├── database/
│   ├── __init__.py
│   ├── connection.py           # Database connection
│   └── schema.sql              # PostgreSQL schema
├── uploads/                    # Temporary document storage
├── requirements.txt
├── .env.example
├── docker-compose.yml          # PostgreSQL with pgvector
└── README.md
```

---

## Learning Path

### Phase 1: LangChain Fundamentals ⭐ START HERE
**Concepts Covered:**
- **DocumentLoaders**: Load different file formats
  - `PyPDFLoader` for PDF files
  - `Docx2txtLoader` for Word documents
  - `TextLoader` for plain text files

- **TextSplitters**: Break documents into chunks
  - `RecursiveCharacterTextSplitter` - Smart splitting on paragraph/sentence boundaries
  - `TokenTextSplitter` - Split by token count for LLM context windows
  - Chunk size and overlap strategies

- **Embeddings**: Convert text to vector representations
  - OpenAI embeddings (`text-embedding-3-small`)
  - Understanding vector dimensions (1536 for OpenAI)
  - Why embeddings capture semantic meaning

- **VectorStores**: Store and query vectors
  - PostgreSQL with pgvector extension
  - Similarity search (cosine, euclidean)
  - Metadata filtering

**Implementation Files:**
- `langchain_components/document_processor.py`
- `langchain_components/embeddings.py`
- `langchain_components/vectorstore.py`

**Key Learning Outcomes:**
- How to load and preprocess documents
- Why chunking matters for retrieval quality
- How embeddings represent semantic meaning
- Vector similarity search fundamentals

---

### Phase 2: LangChain Expression Language (LCEL)
**Concepts Covered:**
- **Chains**: Composable units of LLM logic
  - Sequential chains with `|` operator
  - `RunnablePassthrough` for data flow
  - `RunnableLambda` for custom functions

- **Prompts**: Structured LLM instructions
  - `PromptTemplate` for dynamic prompts
  - `ChatPromptTemplate` for chat models
  - Few-shot prompting techniques

- **Runnables**: Building blocks of LCEL
  - Input/output schemas
  - Streaming responses
  - Batch processing

- **Output Parsers**: Structure LLM responses
  - `StrOutputParser` for text
  - `JsonOutputParser` for structured data
  - Custom parsers

**Implementation Files:**
- `langchain_components/chains.py`

**Example Chain:**
```python
summarize_chain = (
    {"text": RunnablePassthrough()}
    | summarize_prompt
    | llm
    | StrOutputParser()
)
```

**Key Learning Outcomes:**
- Build reusable LLM chains
- Compose complex workflows from simple components
- Handle inputs and outputs cleanly
- Use prompts effectively

---

### Phase 3: RAG (Retrieval Augmented Generation)
**Concepts Covered:**
- **Retrievers**: Query interface for vector stores
  - Similarity search retrievers
  - MMR (Maximum Marginal Relevance) for diversity
  - Contextual compression

- **RAG Chain**: Combine retrieval + generation
  - Retrieve relevant chunks
  - Pass context to LLM
  - Generate grounded answers

- **Context Management**:
  - Formatting retrieved documents
  - Context window optimization
  - Relevance filtering

- **Prompt Engineering for RAG**:
  - System prompts for grounded answers
  - Handling "I don't know" cases
  - Citation and source tracking

**Implementation Files:**
- `langchain_components/chains.py` (RAG chain)

**RAG Chain Structure:**
```python
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | qa_prompt
    | llm
    | StrOutputParser()
)
```

**Key Learning Outcomes:**
- Why RAG improves accuracy and reduces hallucinations
- How retrieval enhances LLM responses
- Trade-offs between retrieval quality and speed
- Handling multi-document queries

---

### Phase 4: LangGraph Workflows
**Concepts Covered:**
- **State Management**: TypedDict for workflow state
  ```python
  class DocumentState(TypedDict):
      document: str
      chunks: list[str]
      embeddings: list[list[float]]
      summary: str
  ```

- **Nodes**: Functions that process state
  - Pure functions that take state, return updates
  - Async node execution
  - Error handling in nodes

- **Edges**: Define workflow flow
  - Normal edges: `graph.add_edge("A", "B")`
  - Conditional edges: Route based on state
  - Entry and finish points

- **Graph Compilation**: Create executable workflows
  - `StateGraph` class
  - Compilation and invocation
  - Streaming intermediate results

**Implementation Files:**
- `langgraph_components/document_workflow.py`

**Example Workflow:**
```
START → load_document → split_text → generate_embeddings → store_vectors → summarize → END
```

**Key Learning Outcomes:**
- Build stateful, multi-step workflows
- Handle complex branching logic
- Track workflow state throughout execution
- Debug and visualize graph execution

---

### Phase 5: LangGraph Agents
**Concepts Covered:**
- **Agent State**: Manage conversation context
  ```python
  class AgentState(TypedDict):
      messages: list[BaseMessage]
      documents: list[Document]
      next_step: str
  ```

- **Tool Integration**: Give agents capabilities
  - Vector store retrieval tool
  - Document metadata tool
  - Custom tools

- **Memory**: Conversation persistence
  - Message history management
  - Context window management
  - Long-term memory strategies

- **Agent Loop**: Iterative reasoning
  - Thought → Action → Observation cycle
  - Self-correction
  - Max iterations and stopping criteria

- **Human-in-the-Loop**: Optional approval
  - Pause for user input
  - Review before execution
  - Override agent decisions

**Implementation Files:**
- `langgraph_components/qa_agent.py`

**Agent Architecture:**
```
User Question → Agent (with tools) → Retrieve Docs → Generate Answer → Store in Memory → Return
                    ↑                                                        ↓
                    └──────────── Iterative Refinement ────────────────────┘
```

**Key Learning Outcomes:**
- Build autonomous agents with tools
- Manage conversational context
- Implement agent reasoning loops
- Balance autonomy with control

---

## Technical Stack

### Core Libraries
- **LangChain** (`langchain`, `langchain-openai`, `langchain-community`)
  - Document processing and embeddings
  - Chain building with LCEL
  - RAG implementation

- **LangGraph** (`langgraph`)
  - Workflow orchestration
  - Agent state management
  - Graph-based execution

- **Database**
  - PostgreSQL 15+
  - pgvector extension for vector operations

- **API Framework**
  - FastAPI for REST endpoints
  - Pydantic for data validation

- **LLM Provider**
  - OpenAI API (GPT-4 for generation, text-embedding-3-small for embeddings)

### Additional Dependencies
- `pypdf` - PDF parsing
- `docx2txt` - Word document parsing
- `python-multipart` - File upload handling
- `psycopg2-binary` - PostgreSQL adapter
- `python-dotenv` - Environment management

---

## Database Schema

```sql
-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Documents table
CREATE TABLE documents (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    file_type VARCHAR(50),
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    summary TEXT,
    metadata JSONB DEFAULT '{}'::jsonb
);

-- Document chunks with vector embeddings
CREATE TABLE document_chunks (
    id SERIAL PRIMARY KEY,
    document_id INTEGER REFERENCES documents(id) ON DELETE CASCADE,
    chunk_text TEXT NOT NULL,
    chunk_index INTEGER NOT NULL,
    embedding vector(1536),  -- OpenAI embedding dimension
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Index for vector similarity search
CREATE INDEX ON document_chunks USING ivfflat (embedding vector_cosine_ops)
WITH (lists = 100);

-- Index for document lookups
CREATE INDEX idx_chunks_document_id ON document_chunks(document_id);
```

---

## API Endpoints

### 1. Upload Document
```
POST /api/documents/upload
Content-Type: multipart/form-data

Body:
  - file: Document file (PDF, DOCX, TXT)

Response:
  {
    "document_id": 1,
    "filename": "example.pdf",
    "chunks_created": 25,
    "status": "processed"
  }
```

### 2. Get Document Summary
```
GET /api/documents/{document_id}/summary

Response:
  {
    "document_id": 1,
    "filename": "example.pdf",
    "summary": "This document discusses...",
    "created_at": "2026-01-12T10:30:00Z"
  }
```

### 3. Query Document
```
POST /api/documents/{document_id}/query

Body:
  {
    "question": "What are the main findings?",
    "conversation_id": "optional-uuid"
  }

Response:
  {
    "answer": "The main findings are...",
    "sources": [
      {"chunk_id": 5, "text": "relevant excerpt", "similarity": 0.89}
    ],
    "conversation_id": "uuid"
  }
```

### 4. List Documents
```
GET /api/documents

Response:
  {
    "documents": [
      {
        "id": 1,
        "filename": "example.pdf",
        "upload_date": "2026-01-12T10:30:00Z",
        "chunks_count": 25
      }
    ]
  }
```

### 5. Delete Document
```
DELETE /api/documents/{document_id}

Response:
  {
    "message": "Document deleted successfully",
    "document_id": 1
  }
```

---

## Key Features

### Document Processing Pipeline (LangGraph)
```
Upload → Load Document → Split into Chunks → Generate Embeddings → Store in Vector DB → Create Summary
```

**LangGraph Nodes:**
1. `load_document_node`: Load file and extract text
2. `split_chunks_node`: Chunk text with overlap
3. `embed_chunks_node`: Generate vector embeddings
4. `store_vectors_node`: Save to PostgreSQL
5. `summarize_node`: Create document summary with LLM

**State Flow:**
- Each node receives state, processes it, and returns updates
- Conditional edges can route based on document type or size
- Final state contains all processing results

### Q&A Agent (LangGraph)
```
User Question → Retrieve Relevant Chunks → Generate Answer with Context → Store in Memory → Return Response
```

**Agent Tools:**
1. `vector_search_tool`: Query vector store for relevant chunks
2. `get_document_metadata_tool`: Fetch document information
3. `previous_qa_tool`: Access conversation history

**Agent Loop:**
- Agent decides which tools to use
- Retrieves information iteratively
- Generates final answer with full context
- Stores conversation for future queries

---

## Environment Setup

### Required Environment Variables
```bash
# OpenAI API
OPENAI_API_KEY=sk-...

# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=doc_analyser
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Application
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760  # 10MB
```

### Docker Compose for PostgreSQL
```yaml
version: '3.8'
services:
  postgres:
    image: pgvector/pgvector:pg15
    environment:
      POSTGRES_DB: doc_analyser
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

---

## Learning Milestones

### Milestone 1: Basic Document Processing
- Load a PDF and split it into chunks
- Generate embeddings for chunks
- Store in PostgreSQL with pgvector
- Perform similarity search

### Milestone 2: Simple Summarization
- Create a LangChain chain for summarization
- Use LCEL to pipe document → prompt → LLM
- Extract key points from documents

### Milestone 3: RAG Q&A
- Build a retriever from vector store
- Create RAG chain that retrieves context
- Answer questions grounded in document content

### Milestone 4: Document Workflow
- Convert document processing to LangGraph
- Add state management for each step
- Visualize workflow execution

### Milestone 5: Conversational Agent
- Build LangGraph agent with tools
- Add conversation memory
- Enable multi-turn Q&A sessions

---

## Next Steps

1. **Phase 1: LangChain Fundamentals** ⭐ CURRENT
   - Set up project structure
   - Install dependencies
   - Configure PostgreSQL with pgvector
   - Implement document loaders
   - Create text splitters
   - Set up embeddings and vector store

2. **Phase 2-5**: Progress through remaining phases sequentially

3. **Testing & Refinement**: Test with various document types and queries

4. **Documentation**: Add examples and usage guides

---

## Resources for Learning

### Official Documentation
- [LangChain Docs](https://python.langchain.com/)
- [LangGraph Docs](https://langchain-ai.github.io/langgraph/)
- [pgvector GitHub](https://github.com/pgvector/pgvector)

### Key Concepts to Study
- Vector embeddings and similarity search
- Prompt engineering for LLMs
- RAG architecture patterns
- Agent design patterns
- State machines and workflow orchestration

---

## Success Criteria

By the end of this project, you will understand:
- How to build production LangChain applications
- When to use chains vs agents
- How to implement RAG for grounded Q&A
- How to orchestrate complex workflows with LangGraph
- How to manage state in multi-step AI applications
- Vector database integration for semantic search
- Best practices for LLM application architecture
