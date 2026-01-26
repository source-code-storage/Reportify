# 📁 Reportify - Folder Structure

**Clean, organized, and professional structure for hackathon submission**

---

## 🎯 Root Directory

```
reportify/
├── 📄 README.md                    # Main project documentation
├── 📄 PROJECT_OVERVIEW.md          # Project summary and status
├── 📄 DEPLOY_NOW.md                # Quick deployment guide (15 min)
├── 📄 READY_TO_DEPLOY.md           # Deployment checklist
├── 📄 render.yaml                  # Render deployment configuration
├── 📄 docker-compose.yml           # Docker services configuration
├── 📄 .gitignore                   # Git ignore rules
├── 📄 PFE_Project_Template.pdf     # Test template for demo
│
├── 📁 backend/                     # FastAPI backend application
├── 📁 frontend/                    # React frontend application
├── 📁 docs/                        # Documentation files
├── 📁 scripts/                     # Utility scripts
├── 📁 examples/                    # Example files (from template)
├── 📁 .kiro/                       # Kiro CLI configuration
├── 📁 .vscode/                     # VS Code settings
├── 📁 .git/                        # Git repository
└── 📁 venv/                        # Python virtual environment
```

---

## 📂 Backend Structure

```
backend/
├── 📁 app/                         # Main application code
│   ├── 📁 api/                     # API endpoints
│   │   └── 📁 v1/
│   │       ├── 📁 endpoints/       # Route handlers
│   │       │   ├── auth.py         # Authentication endpoints
│   │       │   ├── reports.py      # Report management
│   │       │   ├── notes.py        # Note upload
│   │       │   ├── content.py      # Search & generation
│   │       │   ├── uploads.py      # File uploads
│   │       │   └── export.py       # PDF/DOCX export
│   │       └── api.py              # API router
│   │
│   ├── 📁 core/                    # Core configuration
│   │   ├── config.py               # Settings
│   │   ├── database.py             # Database connection
│   │   └── security.py             # JWT & auth
│   │
│   ├── 📁 models/                  # Database models
│   │   ├── user.py                 # User model
│   │   ├── report.py               # Report model
│   │   ├── note.py                 # Note model
│   │   └── template_structure.py  # Template model
│   │
│   ├── 📁 services/                # Business logic
│   │   ├── auth_service.py         # Authentication
│   │   ├── report_service.py       # Report management
│   │   ├── upload_service.py       # File uploads
│   │   ├── pdf_service.py          # PDF processing
│   │   ├── embedding_service.py    # Embeddings
│   │   ├── vector_service.py       # Qdrant search
│   │   ├── content_service.py      # AI generation
│   │   └── export_service.py       # Export
│   │
│   ├── 📁 worker/                  # Celery tasks
│   │   ├── celery_app.py           # Celery configuration
│   │   └── 📁 tasks/
│   │       ├── pdf_processing.py   # PDF tasks
│   │       └── ocr_processing.py   # OCR tasks
│   │
│   └── main.py                     # FastAPI application
│
├── 📁 alembic/                     # Database migrations
│   ├── versions/                   # Migration files
│   └── env.py                      # Alembic config
│
├── 📄 requirements.txt             # Python dependencies
├── 📄 .env.example                 # Environment template
├── 📄 .env                         # Environment variables (gitignored)
└── 📄 alembic.ini                  # Alembic configuration
```

---

## 🎨 Frontend Structure

```
frontend/
├── 📁 src/                         # Source code
│   ├── 📁 components/              # React components
│   │   ├── 📁 ui/                  # shadcn/ui components
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── input.tsx
│   │   │   └── ...
│   │   ├── ProtectedRoute.tsx      # Auth guard
│   │   ├── RichTextEditor.tsx      # Content editor
│   │   ├── NoteUpload.tsx          # File upload
│   │   ├── NotesSearch.tsx         # Search interface
│   │   ├── NotesList.tsx           # Notes display
│   │   └── ExportModal.tsx         # Export dialog
│   │
│   ├── 📁 pages/                   # Page components
│   │   ├── Landing.tsx             # Landing page
│   │   ├── Login.tsx               # Login page
│   │   ├── Register.tsx            # Registration page
│   │   ├── Dashboard.tsx           # Dashboard
│   │   └── ReportDetail.tsx        # Report editor
│   │
│   ├── 📁 services/                # API services
│   │   └── api.ts                  # API client
│   │
│   ├── 📁 stores/                  # State management
│   │   ├── authStore.ts            # Auth state
│   │   └── reportStore.ts          # Report state
│   │
│   ├── 📁 lib/                     # Utilities
│   │   └── utils.ts                # Helper functions
│   │
│   ├── 📁 config/                  # Configuration
│   │   └── api.ts                  # API config
│   │
│   ├── App.tsx                     # Main app component
│   ├── main.tsx                    # Entry point
│   └── index.css                   # Global styles
│
├── 📁 public/                      # Static assets
│   ├── logo.svg                    # Reportify logo
│   └── favicon.svg                 # Favicon
│
├── 📄 package.json                 # Node dependencies
├── 📄 tsconfig.json                # TypeScript config
├── 📄 vite.config.ts               # Vite config
├── 📄 tailwind.config.js           # Tailwind config
├── 📄 index.html                   # HTML template
└── 📄 .env                         # Environment variables
```

---

## 📚 Documentation Structure

```
docs/
├── 📄 DEPLOYMENT_INSTRUCTIONS.md   # Detailed deployment guide
├── 📄 DEPLOYMENT_GUIDE.md          # Alternative deployment guide
├── 📄 DEPLOYMENT_READY.md          # Deployment status
├── 📄 DEPLOYMENT_SUMMARY.md        # Deployment summary
├── 📄 PRE_SUBMISSION_CHECKLIST.md  # Hackathon checklist
├── 📄 TEST_BEFORE_DEMO.md          # Testing guide
├── 📄 HOW_TO_TEST_WITH_TEMPLATE.md # Template testing guide
├── 📄 LANDING_PAGE_READY.md        # Landing page docs
├── 📄 kiro-guide.md                # Kiro CLI reference
│
└── 📁 archive/                     # Old documentation
    ├── AI_*.md                     # Development logs
    ├── TASK_*.md                   # Task completion logs
    ├── PROJECT_*.md                # Project status logs
    └── ...                         # Other archived docs
```

---

## 🛠️ Scripts Structure

```
scripts/
├── 📄 verify_deployment.bat        # Verify all services
├── 📄 reset_database.py            # Reset database
├── 📄 reset_database.bat           # Reset database (Windows)
├── 📄 reset_now.py                 # Reset without confirmation
├── 📄 delete_all_reports.py        # Delete all reports
├── 📄 check_db.py                  # Check database status
├── 📄 create_test_template.py      # Generate test template
├── 📄 start_backend.bat            # Start backend
├── 📄 start_services.bat           # Start all services
├── 📄 quick_test.bat               # Quick test script
└── 📄 test_template.txt            # Template text version
```

---

## 🎯 Key Files Explained

### Root Level

**README.md**
- Main project documentation
- Getting started guide
- Features overview
- Architecture diagram
- Deployment instructions

**PROJECT_OVERVIEW.md**
- Project summary
- Status and progress
- Technical details
- Hackathon scoring
- Next steps

**DEPLOY_NOW.md**
- Quick deployment guide (15 minutes)
- Step-by-step Render deployment
- Environment variables
- Troubleshooting

**READY_TO_DEPLOY.md**
- Deployment checklist
- Pre-deployment tasks
- Post-deployment tasks
- Timeline

**render.yaml**
- Render deployment configuration
- Services definition
- Environment variables
- Database configuration

**docker-compose.yml**
- Local development services
- PostgreSQL, Redis, MinIO, Qdrant
- Volume configuration
- Health checks

**.gitignore**
- Files to exclude from Git
- Python cache files
- Node modules
- Environment variables
- Database files

**PFE_Project_Template.pdf**
- Test template for demo
- Academic report structure
- Multiple sections
- Professional formatting

---

## 📦 What's Gitignored

```
# Python
__pycache__/
*.pyc
venv/
*.egg-info/

# Database
*.db
*.sqlite

# Environment
.env
.env.local

# Node
node_modules/
dist/

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Temporary
*.tmp
temp/

# Uploads (local only)
uploads/
```

---

## 🎯 For Hackathon Judges

### What to Look At

**Main Documentation:**
1. `README.md` - Start here for overview
2. `PROJECT_OVERVIEW.md` - Project summary
3. `DEPLOY_NOW.md` - How to deploy

**Code Structure:**
1. `backend/app/` - Backend code
2. `frontend/src/` - Frontend code
3. `docker-compose.yml` - Infrastructure

**Deployment:**
1. `render.yaml` - Deployment config
2. `docs/DEPLOYMENT_INSTRUCTIONS.md` - Detailed guide

**Testing:**
1. `scripts/verify_deployment.bat` - Verify services
2. `docs/TEST_BEFORE_DEMO.md` - Testing guide

---

## 🧹 Clean Structure Benefits

### For Development
- ✅ Easy to navigate
- ✅ Clear separation of concerns
- ✅ Logical organization
- ✅ Quick to find files

### For Judges
- ✅ Professional presentation
- ✅ Easy to understand
- ✅ Clear documentation
- ✅ Well-organized code

### For Deployment
- ✅ Clean Git history
- ✅ No unnecessary files
- ✅ Clear configuration
- ✅ Easy to deploy

---

## 📊 File Count Summary

```
Total Files: ~150
├── Backend Code: ~40 files
├── Frontend Code: ~30 files
├── Documentation: ~20 files
├── Scripts: ~15 files
├── Configuration: ~10 files
└── Other: ~35 files
```

---

## 🎉 Summary

**Clean, professional, and ready for submission!**

- ✅ Organized structure
- ✅ Clear documentation
- ✅ Logical separation
- ✅ Easy to navigate
- ✅ Professional presentation

**Perfect for hackathon judges to review!** 🌟

---

**Last Updated:** January 18, 2026  
**Status:** Clean and Organized  
**Ready:** For Deployment and Submission
