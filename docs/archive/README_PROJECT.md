# 📝 Report Writing Assistant

> An AI-powered tool that automates report creation by processing documents, extracting relevant information, and generating content using semantic search and GPT-4.

[![Hackathon](https://img.shields.io/badge/Dynamous-Kiro%20Hackathon-blue)](https://dynamous.ai/kiro-hackathon)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-green)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.2.0-blue)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.0-blue)](https://www.typescriptlang.org/)

---

## 🎯 Problem Statement

Writing professional reports is time-consuming and tedious:
- Reading through multiple documents to find relevant information
- Manually extracting and organizing content into sections
- Writing coherent content that synthesizes information from various sources
- Maintaining consistent formatting and structure
- Tracking citations and sources

**This tool automates the entire process.**

---

## ✨ Key Features

### 🤖 AI-Powered Content Generation
- Uses OpenAI GPT-4 to generate section content
- Context-aware generation based on uploaded notes
- Automatic citation tracking
- Multiple generation modes: generate, improve, expand

### 🔍 Semantic Search
- Vector embeddings using Sentence Transformers
- Qdrant vector database for fast similarity search
- Understands meaning, not just keywords
- Finds relevant content across all uploaded documents

### 📄 Document Processing
- Automatic PDF text extraction with PyMuPDF
- OCR for scanned documents and images using Tesseract
- Template structure detection and section extraction
- Async processing with Celery for large files

### 📤 Export Functionality
- Export to PDF with professional formatting (ReportLab)
- Export to DOCX for further editing (python-docx)
- Maintains section structure and formatting
- Includes all generated content and citations

### 🎨 Modern User Interface
- Built with React 18 and TypeScript
- Beautiful UI components from shadcn/ui
- Tailwind CSS for styling
- Smooth animations and transitions
- Responsive design

### 🔐 Secure Authentication
- JWT-based authentication
- Access and refresh tokens
- Protected API endpoints
- User-specific data isolation

---

## 🏗️ Architecture

### Technology Stack

**Backend:**
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **Celery** - Async task processing
- **OpenAI API** - GPT-4 for content generation
- **Sentence Transformers** - Text embeddings
- **Qdrant** - Vector database for semantic search
- **PyMuPDF** - PDF text extraction
- **Tesseract** - OCR for images
- **ReportLab** - PDF generation
- **python-docx** - DOCX generation

**Frontend:**
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **shadcn/ui** - Component library
- **React Router** - Navigation
- **Zustand** - State management
- **Axios** - HTTP client

**Infrastructure:**
- **Docker** - Containerization
- **PostgreSQL** - Primary database
- **Redis** - Caching and message broker
- **MinIO** - S3-compatible object storage
- **Qdrant** - Vector database

### System Architecture

```
┌─────────────┐
│   Browser   │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────┐
│          React Frontend                 │
│  (TypeScript + Tailwind + shadcn/ui)   │
└──────────────────┬──────────────────────┘
                   │ HTTP/REST
                   ▼
┌─────────────────────────────────────────┐
│         FastAPI Backend                 │
│  ┌─────────────────────────────────┐   │
│  │  Authentication Service         │   │
│  │  Report Service                 │   │
│  │  Upload Service                 │   │
│  │  Content Generation Service     │   │
│  │  Search Service                 │   │
│  │  Export Service                 │   │
│  └─────────────────────────────────┘   │
└───┬────────┬────────┬────────┬─────────┘
    │        │        │        │
    ▼        ▼        ▼        ▼
┌────────┐ ┌──────┐ ┌──────┐ ┌────────┐
│Postgres│ │Redis │ │MinIO │ │Qdrant  │
└────────┘ └──────┘ └──────┘ └────────┘
              │
              ▼
    ┌──────────────────┐
    │  Celery Worker   │
    │  - PDF Process   │
    │  - OCR Process   │
    │  - Embeddings    │
    └──────────────────┘
```

---

## 🚀 Getting Started

### Prerequisites

- **Docker Desktop** (for PostgreSQL, Redis, MinIO, Qdrant)
- **Python 3.11+**
- **Node.js 18+**
- **Git**

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/report-writing-assistant
cd report-writing-assistant
```

#### 2. Start Infrastructure Services

```bash
docker-compose up -d
```

This starts:
- PostgreSQL (port 5432)
- Redis (port 6379)
- MinIO (port 9000, console 9001)
- Qdrant (port 6333)

#### 3. Setup Backend

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create environment file
copy .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=sk-your-key-here

# Run database migrations
alembic upgrade head
```

#### 4. Start Backend Services

```bash
# Terminal 1: Start FastAPI server
cd backend
venv\Scripts\activate
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2: Start Celery worker
cd backend
venv\Scripts\activate
celery -A app.worker.celery_app worker --loglevel=info --pool=solo
```

#### 5. Setup Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

#### 6. Access the Application

- **Frontend:** http://localhost:5173
- **Backend API:** http://127.0.0.1:8000
- **API Documentation:** http://127.0.0.1:8000/docs
- **MinIO Console:** http://localhost:9001 (minioadmin/minioadmin)

### Quick Verification

Run the verification script to check all services:

```bash
verify_deployment.bat
```

---

## 📖 Usage Guide

### 1. Register and Login

1. Open http://localhost:5173
2. Click "Create one now" to register
3. Fill in email, password, and full name
4. Login with your credentials

### 2. Create a Report

1. Click "Create New Report" button
2. Enter report title and description
3. (Optional) Upload a PDF template
   - Template sections will be automatically extracted
4. Click "Create Report"

### 3. Upload Notes

1. Open your report
2. Click "Upload Notes" button
3. Select PDF, text, or image files
4. Wait for processing (check Celery worker logs)
5. Notes are processed and embeddings are generated

### 4. Search Your Notes

1. Click "Search Notes" tab
2. Enter a search query
3. View semantically relevant results
4. Results are ranked by similarity, not just keywords

### 5. Generate Content

1. Click on a section in your report
2. Click "Generate Content" button
3. Wait for AI generation (uses GPT-4)
4. Review generated content
5. Edit manually if needed
6. Content is automatically saved

### 6. Export Report

1. Click "Export" button
2. Choose format:
   - **PDF** - Professional formatting, ready to share
   - **DOCX** - Editable in Microsoft Word
3. Download your report

---

## 🎬 Demo Video

[🎥 Watch Demo Video](https://youtube.com/your-demo-video)

*5-minute walkthrough showing all features in action*

---

## 📸 Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)
*Clean dashboard showing all your reports with progress tracking*

### Report Editor
![Report Editor](screenshots/editor.png)
*Rich text editor with AI-powered content generation*

### Semantic Search
![Search](screenshots/search.png)
*Intelligent search that understands context and meaning*

### Export Options
![Export](screenshots/export.png)
*Export to PDF or DOCX with professional formatting*

---

## 🔧 Configuration

### Environment Variables

Key environment variables in `backend/.env`:

```bash
# Database
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/report_assistant

# Redis
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1

# MinIO/S3
S3_ENDPOINT_URL=http://localhost:9000
S3_ACCESS_KEY=minioadmin
S3_SECRET_KEY=minioadmin
S3_BUCKET_NAME=report-assistant-files

# Qdrant
QDRANT_URL=http://localhost:6333

# JWT
SECRET_KEY=your-secret-key-change-in-production

# OpenAI
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-4
```

See `.env.example` for all available options.

---

## 🧪 Testing

### Manual Testing

Follow the complete user workflow:

1. Register → Login
2. Create Report → Upload Template
3. Upload Notes → Wait for Processing
4. Search Notes → Verify Results
5. Generate Content → Review Output
6. Export → Download Files

### Automated Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

---

## 🐛 Troubleshooting

### Docker Services Not Starting

```bash
# Check Docker Desktop is running
docker ps

# Restart services
docker-compose down
docker-compose up -d
```

### Backend Won't Start

```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
pip install -r requirements.txt

# Check database connection
python -c "from app.core.database import engine; print(engine)"
```

### Celery Worker Not Processing

```bash
# Check Redis connection
docker ps | findstr redis

# Restart worker
# Ctrl+C to stop, then:
celery -A app.worker.celery_app worker --loglevel=info --pool=solo
```

### Frontend Build Errors

```bash
# Clear cache
cd frontend
rm -rf node_modules package-lock.json
npm install
```

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for more troubleshooting tips.

---

## 📚 Documentation

- **[DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)** - Comprehensive deployment instructions
- **[PRE_SUBMISSION_CHECKLIST.md](PRE_SUBMISSION_CHECKLIST.md)** - Hackathon submission checklist
- **[DEVLOG.md](DEVLOG.md)** - Development timeline and decisions
- **[API Documentation](http://127.0.0.1:8000/docs)** - Interactive API docs (when running)

---

## 🎯 Project Status

### ✅ Completed Features

- [x] User authentication (register, login, JWT)
- [x] Report management (CRUD operations)
- [x] Template upload and processing
- [x] Note upload and processing
- [x] PDF text extraction
- [x] OCR for images
- [x] Embedding generation
- [x] Semantic search with Qdrant
- [x] AI content generation with GPT-4
- [x] PDF export
- [x] DOCX export
- [x] Modern React UI
- [x] Async processing with Celery

### 🚀 Future Enhancements

- [ ] Collaborative editing
- [ ] Version history
- [ ] Custom templates
- [ ] More export formats
- [ ] Advanced search filters
- [ ] Mobile app
- [ ] API rate limiting
- [ ] User analytics

---

## 🏆 Hackathon Submission

This project was built for the **Dynamous Kiro Hackathon** (January 5-23, 2026).

### Key Highlights

**Innovation:**
- Semantic search using vector embeddings (not just keywords)
- Context-aware AI content generation
- Automatic document structure extraction
- Async processing pipeline for scalability

**Technical Excellence:**
- Modern tech stack (FastAPI, React, TypeScript)
- Clean architecture with service layer pattern
- Comprehensive error handling
- Production-ready deployment with Docker

**Real-World Value:**
- Solves genuine problem (report writing is time-consuming)
- Complete end-to-end workflow
- Professional UI/UX
- Export to standard formats

### Built With Kiro CLI

This project was developed using Kiro CLI for:
- Code generation and scaffolding
- Debugging and troubleshooting
- Documentation writing
- Architecture planning

See [DEVLOG.md](DEVLOG.md) for detailed development process.

---

## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- **Dynamous** for hosting the Kiro Hackathon
- **OpenAI** for GPT-4 API
- **Sentence Transformers** for embedding models
- **Qdrant** for vector database
- **shadcn/ui** for beautiful UI components

---

## 📞 Contact

**Your Name** - your.email@example.com

**Project Link:** https://github.com/yourusername/report-writing-assistant

**Demo Video:** https://youtube.com/your-demo-video

---

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Built with ❤️ for the Dynamous Kiro Hackathon**
