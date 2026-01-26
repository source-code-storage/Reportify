# AI Content Generation Implementation Plan

## Goal
Implement the complete infrastructure needed for AI-powered content generation.

## What We're Building

### User Flow:
1. User uploads research notes (PDFs, text files, images)
2. System extracts text and generates embeddings
3. User navigates to a report section
4. User clicks "Generate Content"
5. AI finds relevant notes and generates content with citations
6. User can improve/expand the generated content

## Implementation Steps

### Step 1: Update Requirements ✅
Add AI/ML dependencies:
- sentence-transformers (for embeddings)
- qdrant-client (vector database)
- openai (for GPT-4)
- langchain (LLM orchestration)

### Step 2: Database Models
Create models for:
- Report (store report metadata)
- ReportSection (store section content)
- Note (store uploaded note content)
- NoteEmbedding (store vector embeddings)

### Step 3: File Upload Service
- S3/MinIO integration
- File validation
- Store uploaded files

### Step 4: Embedding Generation Service
- Extract text from notes
- Generate embeddings using sentence-transformers
- Store in database

### Step 5: Vector Database Integration
- Set up Qdrant
- Store embeddings
- Implement semantic search

### Step 6: Content Generation Service (THE MAIN FEATURE!)
- Build prompts with context
- Call OpenAI API
- Generate content with citations
- Implement improve/expand features

## Technologies

### AI Stack:
- **Embeddings**: sentence-transformers/all-MiniLM-L6-v2 (free, local)
- **Vector DB**: Qdrant (free, self-hosted)
- **LLM**: OpenAI GPT-4 (paid API, ~$0.03/1K tokens)
- **Orchestration**: LangChain (optional, for advanced features)

### Infrastructure:
- FastAPI (backend)
- PostgreSQL (structured data)
- Qdrant (vector search)
- Redis (task queue)
- Celery (async processing)

## Cost Estimate
- Embeddings: Free (runs locally)
- Vector DB: Free (self-hosted Qdrant)
- Content Generation: ~$0.01-0.05 per section (OpenAI API)

## Timeline
- Step 1-2: 1 hour (models and requirements)
- Step 3: 1 hour (file upload)
- Step 4: 2 hours (embedding generation)
- Step 5: 1 hour (vector database)
- Step 6: 2 hours (content generation)
**Total: ~7 hours of focused work**

Let's start! 🚀
