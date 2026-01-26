# 📝 Reportify - AI-Powered Report Writing Assistant

> Transform your report writing with intelligent document processing, semantic search, and GPT-4 content generation.

[![Hackathon](https://img.shields.io/badge/Dynamous-Kiro%20Hackathon-blue)](https://dynamous.ai/kiro-hackathon)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.11+-blue)](https://python.org)
[![React](https://img.shields.io/badge/react-18.2-blue)](https://reactjs.org)


---

## 🎯 Problem & Solution

### The Problem
Writing professional reports is time-consuming and tedious:
- Reading through multiple documents to find relevant information
- Manually extracting and organizing content into sections
- Writing coherent content that synthesizes information from various sources
- Maintaining consistent formatting and structure

### Our Solution
**Reportify** automates the entire report writing process using AI:
- 📄 **Smart Document Processing** - Upload PDFs, auto-extract sections
- 🔍 **Semantic Search** - Find relevant information using AI, not just keywords
- 🤖 **AI Content Generation** - Generate high-quality content with GPT-4
- 📤 **Professional Export** - Export to PDF or DOCX with perfect formatting

---

## ✨ Key Features

### 🤖 AI-Powered Content Generation
- Uses OpenAI GPT-4 for intelligent content creation
- Context-aware generation based on your uploaded notes
- Automatic citation tracking
- Multiple generation modes: generate, improve, expand

### 🔍 Semantic Search
- Vector embeddings using Sentence Transformers
- Qdrant vector database for fast similarity search
- Understands meaning and context, not just keywords
- Find relevant content across all your documents

### 📄 Document Processing
- Automatic PDF text extraction with PyMuPDF
- OCR for scanned documents and images (Tesseract)
- Template structure detection and section extraction
- Async processing with Celery for large files

### 📤 Export Functionality
- Export to PDF with professional formatting (ReportLab)
- Export to DOCX for further editing (python-docx)
- Maintains section structure and formatting
- Ready to submit or share

### 🎨 Modern User Interface
- Built with React 18 and TypeScript
- Beautiful UI components from shadcn/ui
- Tailwind CSS for styling
- Smooth animations and transitions
- Fully responsive design

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

Before you begin, ensure you have the following installed:

- **Docker Desktop** - [Download here](https://www.docker.com/products/docker-desktop/)
  - Required for PostgreSQL, Redis, MinIO, and Qdrant services
- **Python 3.11 or higher** - [Download here](https://www.python.org/downloads/)
- **Node.js 18 or higher** - [Download here](https://nodejs.org/)
- **Git** - [Download here](https://git-scm.com/downloads)

### Installation & Setup

Follow these steps carefully to get the application running on your local machine.

#### Step 1: Clone the Repository

```bash
git clone https://github.com/MuLIAICHI/reportify.git
cd reportify
```

#### Step 2: Start Infrastructure Services with Docker

Open Docker Desktop, then run:

```bash
docker-compose up -d
```

This command starts four essential services:
- **PostgreSQL** - Database (port 5432)
- **Redis** - Message broker and cache (port 6379)
- **MinIO** - File storage (port 9000, console: 9001)
- **Qdrant** - Vector database for semantic search (port 6333)

**Verify services are running:**
```bash
docker ps
```
You should see 4 containers running.

#### Step 3: Setup Backend

Open a new terminal and navigate to the backend directory:

```bash
cd backend
```

**Create and activate a virtual environment:**

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Linux/Mac:
```bash
python -m venv venv
source venv/bin/activate
```

**Install Python dependencies:**
```bash
pip install -r requirements.txt
```

**Configure environment variables:**

Windows:
```bash
copy .env.example .env
```

Linux/Mac:
```bash
cp .env.example .env
```

**IMPORTANT:** Edit the `.env` file and add your OpenAI API key:
```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
```

Get your API key from: https://platform.openai.com/api-keys

**Initialize the database:**
```bash
alembic upgrade head
```

#### Step 4: Start Backend Services

You need **TWO separate terminals** for the backend:

**Terminal 1 - FastAPI Server:**
```bash
cd backend
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 - Celery Worker:**
```bash
cd backend
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux/Mac
celery -A app.worker.celery_app worker --loglevel=info --pool=solo
```

**Verify backend is running:**
- Open http://127.0.0.1:8000/docs in your browser
- You should see the FastAPI interactive documentation

#### Step 5: Setup Frontend

Open a **third terminal** and navigate to the frontend directory:

```bash
cd frontend
```

**Install Node.js dependencies:**
```bash
npm install
```

**Start the development server:**
```bash
npm run dev
```

#### Step 6: Access the Application

Open your browser and navigate to:

- **Frontend Application:** http://localhost:5173
- **Backend API Docs:** http://127.0.0.1:8000/docs
- **MinIO Console:** http://localhost:9001
  - Username: `minioadmin`
  - Password: `minioadmin`

### Verification Checklist

Before using the application, verify all services are running:

- [ ] Docker containers are running (4 containers)
- [ ] FastAPI server is running (Terminal 1)
- [ ] Celery worker is running (Terminal 2)
- [ ] Frontend dev server is running (Terminal 3)
- [ ] Can access http://localhost:5173
- [ ] Can access http://127.0.0.1:8000/docs

### Quick Verification Script

Run this script to check all services (Windows):

```bash
scripts\verify_deployment.bat
```

### Troubleshooting

**Port already in use:**
- Check if another application is using ports 5173, 8000, 5432, 6379, 9000, or 6333
- Stop the conflicting application or change ports in configuration files

**Docker containers not starting:**
- Ensure Docker Desktop is running
- Try: `docker-compose down` then `docker-compose up -d`

**Python dependencies installation fails:**
- Ensure you're using Python 3.11 or higher: `python --version`
- Try upgrading pip: `pip install --upgrade pip`

**OpenAI API errors:**
- Verify your API key is correct in `backend/.env`
- Check you have credits: https://platform.openai.com/usage

**Frontend not loading:**
- Clear browser cache
- Check console for errors (F12)
- Ensure backend is running first

---

## 📖 Usage Guide

### 1. Register and Login

1. Open http://localhost:5173
2. Click "Get Started" to register
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

### 📺 Watch the Full Walkthrough

[![Demo Video](https://img.shields.io/badge/▶️_Watch_Demo-Video-red?style=for-the-badge&logo=youtube)](./assets/kiroDemo.mp4)

**[📥 Download Video](./assets/kiroDemo.mp4)** (8.23 MB) | **[🎥 View in Browser](https://github.com/MuLIAICHI/Reportify/blob/main/assets/kiroDemo.mp4)**

*2-minute walkthrough demonstrating all features*

### What's in the Demo:
- ✅ Smart document processing with PDF parsing
- ✅ Semantic search using AI embeddings  
- ✅ GPT-4 content generation in action
- ✅ Professional PDF/DOCX export

> **💡 Tip:** Click "View in Browser" above to watch the video directly on GitHub with the built-in player!

---

## 📸 Screenshots

### Landing Page
![Landing Page](docs/screenshots/landing.png)
*Modern landing page with clear value proposition*

### Dashboard
![Dashboard](docs/screenshots/dashboard.png)
*Clean dashboard showing all your reports with progress tracking*

### Report Editor
![Report Editor](docs/screenshots/editor.png)
*Rich text editor with AI-powered content generation*

### Semantic Search
![Search](docs/screenshots/search.png)
*Intelligent search that understands context and meaning*

---

## 🏆 Hackathon Submission

This project was built for the **Dynamous Kiro Hackathon** (January 5-26, 2026).

### Key Highlights

**Innovation:**
- Semantic search using vector embeddings (not just keywords)
- Context-aware AI content generation with GPT-4
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

See [docs/DEVLOG.md](docs/DEVLOG.md) for detailed development process.

---

## 🤝 Contributing

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

**LIAICHI Mustapha** - mustaphaliaichi@gmail.com

**Project Link:** https://github.com/MuLIAICHI/reportify

**Demo Video:** [Watch on GitHub](https://github.com/MuLIAICHI/Reportify/blob/main/assets/kiroDemo.mp4) | [Download](./assets/kiroDemo.mp4)

---

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

---

**Built with ❤️ for the Dynamous Kiro Hackathon**

*Transforming report writing with AI, one document at a time.*
