# Report Writing Assistant - Architecture Diagrams

This document contains visual diagrams explaining the system architecture, data flow, and key processes.

## 1. System Architecture Overview

```mermaid
graph TB
    subgraph "Frontend Layer"
        UI[React + TypeScript UI]
        Store[Zustand State Management]
        Router[React Router]
    end

    subgraph "API Layer"
        API[FastAPI Backend]
        Auth[JWT Authentication]
        CORS[CORS Middleware]
    end

    subgraph "Processing Layer"
        Celery[Celery Worker]
        PDF[PDF Processing]
        OCR[OCR Processing]
        AI[OpenAI Integration]
    end

    subgraph "Storage Layer"
        DB[(SQLite/PostgreSQL)]
        S3[MinIO S3 Storage]
        Redis[(Redis Cache)]
        Vector[(Qdrant Vector DB)]
    end

    UI --> Store
    Store --> Router
    Router --> API
    API --> Auth
    API --> CORS
    
    API --> DB
    API --> S3
    API --> Redis
    API --> Vector
    
    API --> Celery
    Celery --> PDF
    Celery --> OCR
    Celery --> AI
    
    PDF --> S3
    OCR --> S3
    AI --> Vector
    
    Celery --> DB
    Celery --> Redis

    style UI fill:#61dafb
    style API fill:#009688
    style Celery fill:#37b24d
    style DB fill:#336791
    style S3 fill:#c92a2a
    style Redis fill:#d32f2f
    style Vector fill:#7c4dff
```

## 2. User Authentication Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant DB
    participant JWT

    User->>Frontend: Enter credentials
    Frontend->>API: POST /auth/login
    API->>DB: Verify user credentials
    DB-->>API: User data
    API->>JWT: Generate tokens
    JWT-->>API: Access + Refresh tokens
    API-->>Frontend: Return tokens
    Frontend->>Frontend: Store tokens
    Frontend-->>User: Redirect to dashboard

    Note over Frontend,API: Subsequent requests include JWT token
    
    User->>Frontend: Access protected resource
    Frontend->>API: GET /reports (with JWT)
    API->>JWT: Validate token
    JWT-->>API: Token valid
    API->>DB: Fetch user data
    DB-->>API: Return data
    API-->>Frontend: Protected resource
    Frontend-->>User: Display data
```

## 3. Template Upload & Processing Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant S3
    participant Celery
    participant PDF Service
    participant DB

    User->>Frontend: Upload PDF template
    Frontend->>API: POST /uploads/template
    API->>API: Validate file
    API->>S3: Upload PDF file
    S3-->>API: File URL
    API->>DB: Create upload job (status: queued)
    API->>Celery: Queue processing task
    API-->>Frontend: Upload job ID
    Frontend-->>User: Show "Processing..."

    Note over Celery,PDF Service: Background Processing

    Celery->>DB: Update status: processing
    Celery->>S3: Download PDF
    S3-->>Celery: PDF content
    Celery->>PDF Service: Extract text & structure
    PDF Service->>PDF Service: Identify sections
    PDF Service-->>Celery: Sections data
    Celery->>DB: Save template structure
    Celery->>DB: Create report sections
    Celery->>DB: Update status: completed
    
    Frontend->>API: Poll upload status
    API->>DB: Get upload job
    DB-->>API: Status: completed
    API-->>Frontend: Processing complete
    Frontend->>API: GET /reports/{id}/sections
    API->>DB: Fetch sections
    DB-->>API: Sections list
    API-->>Frontend: Return sections
    Frontend-->>User: Display sections
```

## 4. AI Content Generation Flow

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant DB
    participant Qdrant
    participant OpenAI
    participant Celery

    User->>Frontend: Request AI content for section
    Frontend->>API: POST /content/generate
    API->>DB: Get report & section data
    DB-->>API: Report context
    API->>DB: Get user notes
    DB-->>API: Notes list
    API->>Qdrant: Search relevant embeddings
    Qdrant-->>API: Similar content
    API->>OpenAI: Generate content with context
    Note over API,OpenAI: Includes: section title,<br/>report context, notes,<br/>similar content
    OpenAI-->>API: Generated content
    API->>DB: Save generated content
    API-->>Frontend: Return content
    Frontend-->>User: Display generated text

    Note over Celery: Async embedding generation
    Celery->>OpenAI: Generate embeddings
    OpenAI-->>Celery: Embedding vectors
    Celery->>Qdrant: Store embeddings
```

## 5. Notes Upload & OCR Processing

```mermaid
sequenceDiagram
    participant User
    participant Frontend
    participant API
    participant S3
    participant Celery
    participant OCR Service
    participant DB
    participant Qdrant

    User->>Frontend: Upload notes (PDF/Images)
    Frontend->>API: POST /uploads/notes
    API->>API: Validate files
    
    loop For each file
        API->>S3: Upload file
        S3-->>API: File URL
        API->>DB: Create note record
        API->>Celery: Queue OCR task
    end
    
    API-->>Frontend: Upload jobs created
    Frontend-->>User: Show "Processing..."

    Note over Celery,OCR Service: Background Processing

    Celery->>S3: Download file
    S3-->>Celery: File content
    
    alt PDF File
        Celery->>OCR Service: Extract text from PDF
    else Image File
        Celery->>OCR Service: Run Tesseract OCR
    end
    
    OCR Service-->>Celery: Extracted text
    Celery->>DB: Update note with content
    Celery->>Qdrant: Generate & store embeddings
    Celery->>DB: Update status: completed
    
    Frontend->>API: Poll note status
    API->>DB: Get note
    DB-->>API: Note with content
    API-->>Frontend: Processing complete
    Frontend-->>User: Display note content
```

## 6. Database Schema Overview

```mermaid
erDiagram
    USERS ||--o{ REPORTS : creates
    USERS ||--o{ NOTES : uploads
    USERS ||--o{ UPLOAD_JOBS : initiates
    
    REPORTS ||--o{ REPORT_SECTIONS : contains
    REPORTS ||--o{ NOTES : belongs_to
    REPORTS ||--o{ TEMPLATE_STRUCTURES : has
    REPORTS ||--o{ UPLOAD_JOBS : tracks
    
    TEMPLATE_STRUCTURES ||--o{ TEMPLATE_SECTIONS : contains
    
    UPLOAD_JOBS ||--o| NOTES : creates
    
    USERS {
        int id PK
        string email UK
        string password_hash
        string name
        datetime created_at
        datetime last_login
        boolean is_active
    }
    
    REPORTS {
        int id PK
        int user_id FK
        string title
        string description
        string status
        datetime created_at
        datetime updated_at
    }
    
    REPORT_SECTIONS {
        int id PK
        int report_id FK
        string title
        text content
        int order
        int word_count
        boolean is_completed
    }
    
    NOTES {
        int id PK
        int report_id FK
        int user_id FK
        string filename
        string file_type
        text content
        string status
        datetime created_at
    }
    
    TEMPLATE_STRUCTURES {
        int id PK
        int report_id FK
        string filename
        int total_pages
        text full_text
        json metadata
        datetime processed_at
    }
    
    TEMPLATE_SECTIONS {
        int id PK
        int template_id FK
        int parent_id FK
        int level
        string title
        text content
        int page_number
        int word_count
    }
    
    UPLOAD_JOBS {
        int id PK
        int user_id FK
        int report_id FK
        string filename
        string file_type
        string status
        int progress
        datetime created_at
        datetime completed_at
    }
```

## 7. Component Architecture (Frontend)

```mermaid
graph TB
    subgraph "Pages"
        Landing[Landing Page]
        Login[Login Page]
        Register[Register Page]
        Dashboard[Dashboard]
        ReportDetail[Report Detail]
    end

    subgraph "Components"
        Header[Header]
        Sidebar[Sidebar]
        SectionCard[Section Card]
        NotesList[Notes List]
        ContentEditor[Content Editor]
        UploadModal[Upload Modal]
    end

    subgraph "State Management"
        AuthStore[Auth Store]
        ReportStore[Report Store]
        UIStore[UI Store]
    end

    subgraph "Services"
        API_Client[API Client]
        AuthService[Auth Service]
        FileService[File Service]
    end

    Landing --> Header
    Dashboard --> Header
    Dashboard --> Sidebar
    ReportDetail --> Header
    ReportDetail --> SectionCard
    ReportDetail --> NotesList
    ReportDetail --> ContentEditor
    ReportDetail --> UploadModal

    Dashboard --> AuthStore
    Dashboard --> ReportStore
    ReportDetail --> ReportStore
    
    AuthStore --> API_Client
    ReportStore --> API_Client
    
    API_Client --> AuthService
    API_Client --> FileService

    style Landing fill:#e3f2fd
    style Dashboard fill:#e3f2fd
    style ReportDetail fill:#e3f2fd
    style AuthStore fill:#fff3e0
    style ReportStore fill:#fff3e0
    style API_Client fill:#f3e5f5
```

## 8. Deployment Architecture

```mermaid
graph TB
    subgraph "Client"
        Browser[Web Browser]
    end

    subgraph "Frontend Server"
        Vite[Vite Dev Server<br/>Port 5174]
    end

    subgraph "Backend Server"
        Uvicorn[Uvicorn<br/>Port 8000]
        CeleryWorker[Celery Worker]
    end

    subgraph "Docker Services"
        Redis[Redis<br/>Port 6379]
        MinIO[MinIO<br/>Port 9000/9001]
        Qdrant[Qdrant<br/>Port 6333]
        Postgres[PostgreSQL<br/>Port 5432]
    end

    subgraph "External Services"
        OpenAI[OpenAI API]
    end

    Browser -->|HTTP| Vite
    Vite -->|API Calls| Uvicorn
    Uvicorn -->|Tasks| CeleryWorker
    
    Uvicorn --> Redis
    Uvicorn --> MinIO
    Uvicorn --> Qdrant
    Uvicorn --> Postgres
    
    CeleryWorker --> Redis
    CeleryWorker --> MinIO
    CeleryWorker --> Qdrant
    CeleryWorker --> Postgres
    CeleryWorker --> OpenAI

    style Browser fill:#61dafb
    style Vite fill:#646cff
    style Uvicorn fill:#009688
    style CeleryWorker fill:#37b24d
    style Redis fill:#d32f2f
    style MinIO fill:#c92a2a
    style Qdrant fill:#7c4dff
    style Postgres fill:#336791
    style OpenAI fill:#10a37f
```

## 9. Technology Stack

```mermaid
mindmap
  root((Report Writing<br/>Assistant))
    Frontend
      React 18
      TypeScript
      Vite
      TailwindCSS
      Zustand
      React Router
      Axios
    Backend
      FastAPI
      Python 3.11+
      Pydantic
      SQLAlchemy
      Alembic
      JWT Auth
    Processing
      Celery
      PyMuPDF
      Tesseract OCR
      OpenAI API
      Embeddings
    Storage
      SQLite/PostgreSQL
      MinIO S3
      Redis
      Qdrant Vector DB
    DevOps
      Docker
      Docker Compose
      Git
      Render Deploy
```

## 10. Request Flow Summary

```mermaid
flowchart LR
    A[User Action] --> B{Request Type?}
    
    B -->|Sync| C[API Handler]
    B -->|Async| D[Celery Task]
    
    C --> E[Validate Request]
    E --> F[Process Business Logic]
    F --> G[Database Operation]
    G --> H[Return Response]
    
    D --> I[Queue Task]
    I --> J[Worker Picks Up]
    J --> K[Process in Background]
    K --> L[Update Database]
    L --> M[Task Complete]
    
    H --> N[Frontend Updates]
    M --> O[Frontend Polls Status]
    O --> N

    style A fill:#e3f2fd
    style C fill:#c8e6c9
    style D fill:#fff9c4
    style N fill:#f8bbd0
```

---

## Key Features Highlighted in Architecture

### 1. **Asynchronous Processing**
- PDF processing happens in background via Celery
- Non-blocking user experience
- Progress tracking for long-running tasks

### 2. **Scalable Storage**
- S3-compatible object storage (MinIO)
- Vector database for semantic search (Qdrant)
- Relational database for structured data
- Redis for caching and message queuing

### 3. **AI Integration**
- OpenAI GPT-4 for content generation
- Embeddings for semantic search
- Context-aware content suggestions

### 4. **Security**
- JWT-based authentication
- CORS protection
- File validation
- User authorization checks

### 5. **Modular Design**
- Separation of concerns
- Service-oriented architecture
- Easy to extend and maintain
- Independent scaling of components

---

## Performance Considerations

1. **Caching Strategy**: Redis caches frequently accessed data
2. **Async Processing**: Heavy tasks don't block API responses
3. **Vector Search**: Fast semantic search using Qdrant
4. **Connection Pooling**: Efficient database connections
5. **File Streaming**: Large files handled efficiently

## Monitoring & Observability

- Celery task monitoring
- API request logging
- Error tracking
- Upload job status tracking
- Processing progress indicators
