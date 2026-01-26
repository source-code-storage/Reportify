# 🚀 Deployment Guide - Report Writing Assistant

**Status:** Ready for Hackathon Submission  
**Deadline:** January 23, 2026  
**Last Updated:** January 18, 2026

---

## 📋 Table of Contents

1. [Pre-Deployment Checklist](#pre-deployment-checklist)
2. [Local Production Testing](#local-production-testing)
3. [Cloud Deployment Options](#cloud-deployment-options)
4. [Environment Configuration](#environment-configuration)
5. [Troubleshooting](#troubleshooting)

---

## ✅ Pre-Deployment Checklist

### System Requirements
- [ ] Docker Desktop installed and running
- [ ] Python 3.11+ installed
- [ ] Node.js 18+ installed
- [ ] Git installed
- [ ] 4GB+ RAM available
- [ ] 10GB+ disk space available

### Services Status
- [ ] PostgreSQL running (port 5432)
- [ ] Redis running (port 6379)
- [ ] MinIO running (ports 9000, 9001)
- [ ] Qdrant running (port 6333)
- [ ] Backend API running (port 8000)
- [ ] Frontend dev server running (port 5173)
- [ ] Celery worker running

### Feature Verification
- [ ] User registration works
- [ ] User login works
- [ ] Report creation works
- [ ] Template upload works
- [ ] Note upload works
- [ ] Semantic search works
- [ ] AI content generation works
- [ ] PDF/DOCX export works

---

## 🏠 Local Production Testing

This is what you need for the hackathon demo and submission.

### Step 1: Verify All Services Running

```bash
# Check Docker services
docker ps

# You should see 4 containers:
# - report-assistant-postgres
# - report-assistant-redis
# - report-assistant-minio
# - report-assistant-qdrant
```

### Step 2: Check Backend Server

```bash
# Backend should be running on http://127.0.0.1:8000
# Test health endpoint
curl http://127.0.0.1:8000/health

# Or visit in browser:
# http://127.0.0.1:8000/docs
```

### Step 3: Check Frontend Server

```bash
# Frontend should be running on http://localhost:5173
# Open in browser and verify UI loads
```

### Step 4: Check Celery Worker

```bash
# Celery worker should show "ready" in logs
# Check for any error messages
```

### Step 5: Full System Test

**Test the complete workflow:**

1. **Register a new user**
   - Go to http://localhost:5173
   - Click "Create one now"
   - Fill in: email, password, full name
   - Submit

2. **Create a report**
   - Click "Create New Report"
   - Title: "Test Report for Hackathon"
   - Description: "Testing all features"
   - Upload a PDF template (optional)
   - Click "Create Report"

3. **Upload notes**
   - In report detail page
   - Click "Upload Notes"
   - Select a PDF or text file
   - Wait for processing (check Celery logs)
   - Verify note appears in list

4. **Test semantic search**
   - Click "Search Notes" tab
   - Enter a search query
   - Verify results appear

5. **Generate AI content**
   - Click on a section
   - Click "Generate Content"
   - Wait for AI generation
   - Verify content appears

6. **Export report**
   - Click "Export" button
   - Choose PDF or DOCX
   - Download and verify file

### Step 6: Record Demo Video

**For hackathon submission:**

1. **Screen recording** (5-10 minutes)
   - Use OBS Studio, Loom, or Windows Game Bar
   - Show the complete workflow above
   - Narrate what you're doing

2. **What to highlight:**
   - Modern, polished UI
   - Smooth user experience
   - AI-powered features
   - Semantic search
   - Export functionality

3. **Upload to:**
   - YouTube (unlisted)
   - Loom
   - Google Drive (public link)

---

## ☁️ Cloud Deployment Options

If you want to deploy online for the hackathon demo.

### Option 1: Railway (Recommended - Easiest)

**Pros:** Free tier, automatic deployments, PostgreSQL included  
**Cons:** Limited free credits

**Steps:**

1. **Create Railway account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Deploy backend**
   ```bash
   # In backend directory, create railway.json
   {
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
       "restartPolicyType": "ON_FAILURE"
     }
   }
   ```

3. **Add services**
   - PostgreSQL (from Railway marketplace)
   - Redis (from Railway marketplace)
   - Add environment variables from `.env`

4. **Deploy frontend**
   - Create new service
   - Connect GitHub repo
   - Set build command: `npm run build`
   - Set start command: `npm run preview`

### Option 2: Render

**Pros:** Free tier, easy setup  
**Cons:** Slower cold starts

**Steps:**

1. **Create Render account**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create Web Service (Backend)**
   - New → Web Service
   - Connect GitHub repo
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Create PostgreSQL database**
   - New → PostgreSQL
   - Copy connection string to environment variables

4. **Create Redis instance**
   - New → Redis
   - Copy connection string

5. **Deploy frontend**
   - New → Static Site
   - Build command: `npm run build`
   - Publish directory: `dist`

### Option 3: Vercel (Frontend) + Railway (Backend)

**Best for:** Fastest frontend, separate backend

**Frontend (Vercel):**
```bash
# Install Vercel CLI
npm i -g vercel

# In frontend directory
cd frontend
vercel

# Follow prompts
# Set environment variable: VITE_API_URL=<your-backend-url>
```

**Backend (Railway):**
- Follow Railway steps above

### Option 4: Docker Compose on VPS

**For full control:** Deploy to DigitalOcean, AWS EC2, or similar

**Steps:**

1. **Get a VPS**
   - DigitalOcean Droplet ($5/month)
   - AWS EC2 t2.micro (free tier)
   - Linode, Vultr, etc.

2. **Install Docker**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   sudo apt install docker-compose
   ```

3. **Clone repo**
   ```bash
   git clone <your-repo>
   cd dynamous-kiro-hackathon
   ```

4. **Configure environment**
   ```bash
   cp backend/.env.example backend/.env
   # Edit backend/.env with production values
   nano backend/.env
   ```

5. **Start services**
   ```bash
   docker-compose up -d
   ```

6. **Setup Nginx reverse proxy**
   ```bash
   sudo apt install nginx
   # Configure nginx to proxy to backend:8000 and frontend:5173
   ```

---

## ⚙️ Environment Configuration

### Production Environment Variables

**Critical changes for production:**

```bash
# backend/.env

# Database - Use PostgreSQL in production
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Security - Generate strong secret key
SECRET_KEY=<generate-with-openssl-rand-hex-32>
DEBUG=False

# CORS - Add your frontend domain
ALLOWED_ORIGINS=https://your-frontend-domain.com

# OpenAI - Use your API key
OPENAI_API_KEY=sk-your-actual-key

# S3 - Use real S3 or keep MinIO
S3_ENDPOINT_URL=https://s3.amazonaws.com  # or keep localhost for MinIO
S3_ACCESS_KEY=<your-aws-access-key>
S3_SECRET_KEY=<your-aws-secret-key>
S3_BUCKET_NAME=report-assistant-prod
```

### Frontend Environment Variables

```bash
# frontend/.env.production

VITE_API_URL=https://your-backend-domain.com
```

### Generate Secure Secret Key

```bash
# On Linux/Mac
openssl rand -hex 32

# On Windows (PowerShell)
-join ((48..57) + (65..90) + (97..122) | Get-Random -Count 32 | % {[char]$_})
```

---

## 🔧 Troubleshooting

### Issue: Docker containers not starting

```bash
# Check Docker Desktop is running
docker ps

# Restart containers
docker-compose down
docker-compose up -d

# Check logs
docker-compose logs
```

### Issue: Backend won't start

```bash
# Check Python version
python --version  # Should be 3.11+

# Reinstall dependencies
cd backend
pip install -r requirements.txt

# Check database connection
python -c "from app.core.database import engine; print(engine)"
```

### Issue: Frontend build fails

```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run build
```

### Issue: Celery worker not processing

```bash
# Check Redis connection
docker ps | findstr redis

# Restart Celery worker
# Ctrl+C to stop
celery -A app.worker.celery_app worker --loglevel=info --pool=solo
```

### Issue: MinIO bucket not found

```bash
# Access MinIO console
# http://localhost:9001
# Login: minioadmin / minioadmin
# Create bucket: report-assistant-files
# Set policy to public or private as needed
```

### Issue: Qdrant shows unhealthy

```bash
# Qdrant may show unhealthy but still work
# Test by uploading a note and searching

# If really broken, restart container
docker restart report-assistant-qdrant
```

### Issue: CORS errors in browser

```bash
# Check ALLOWED_ORIGINS in backend/.env
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Restart backend after changing
```

### Issue: OpenAI API errors

```bash
# Verify API key is valid
# Check OpenAI dashboard for usage/limits
# Ensure you have credits available

# Test API key
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

---

## 📊 Performance Optimization

### For Production Deployment

1. **Use PostgreSQL instead of SQLite**
   - SQLite is for development only
   - PostgreSQL handles concurrent users better

2. **Enable caching**
   - Redis caching for frequently accessed data
   - Browser caching for static assets

3. **Optimize file uploads**
   - Use direct S3 uploads (presigned URLs)
   - Compress images before upload

4. **Scale Celery workers**
   ```bash
   # Run multiple workers
   celery -A app.worker.celery_app worker --concurrency=4
   ```

5. **Use production ASGI server**
   ```bash
   # Instead of uvicorn, use gunicorn + uvicorn workers
   pip install gunicorn
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

---

## 🎯 Hackathon Submission Checklist

### Before Submitting

- [ ] All features tested and working
- [ ] Demo video recorded (5-10 minutes)
- [ ] README.md updated with:
  - [ ] Project description
  - [ ] Setup instructions
  - [ ] Screenshots
  - [ ] Demo video link
- [ ] DEVLOG.md completed with:
  - [ ] Development timeline
  - [ ] Technical decisions
  - [ ] Challenges and solutions
- [ ] Code cleaned up:
  - [ ] Remove debug prints
  - [ ] Remove commented code
  - [ ] Fix any linting errors
- [ ] Environment variables secured:
  - [ ] No API keys in code
  - [ ] .env in .gitignore
  - [ ] .env.example provided
- [ ] Repository ready:
  - [ ] All code committed
  - [ ] Pushed to GitHub
  - [ ] Repository is public

### Submission Materials

1. **GitHub Repository URL**
2. **Demo Video URL** (YouTube, Loom, etc.)
3. **Live Demo URL** (optional, if deployed)
4. **Project Description** (from README.md)
5. **Technologies Used**:
   - Backend: FastAPI, SQLAlchemy, Celery, OpenAI, Sentence Transformers
   - Frontend: React, TypeScript, Tailwind CSS, shadcn/ui
   - Infrastructure: Docker, PostgreSQL, Redis, MinIO, Qdrant

---

## 🎉 You're Ready to Deploy!

Your Report Writing Assistant is fully functional and ready for the hackathon. Choose your deployment strategy:

- **For hackathon demo:** Local production testing is sufficient
- **For online demo:** Use Railway or Render for quick deployment
- **For full control:** Deploy to VPS with Docker Compose

**Good luck with your submission!** 🚀

---

## 📞 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review the logs (backend, Celery, Docker)
3. Test each component individually
4. Verify environment variables are correct

**Remember:** The deadline is January 23, 2026. Plan your deployment accordingly!
