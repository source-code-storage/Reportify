# 🚀 Deployment Instructions - Reportify

**Recommended Platform:** Render (Free Tier)  
**Estimated Time:** 15-20 minutes  
**Cost:** $0 (Free tier)

---

## 📋 Pre-Deployment Checklist

Before deploying, make sure:

- [x] All features tested locally
- [x] Landing page looks good
- [x] Database cleaned (fresh start)
- [ ] Code committed to Git
- [ ] GitHub repository created
- [ ] OpenAI API key ready

---

## 🎯 Option 1: Deploy to Render (Recommended)

### Why Render?
- ✅ Free tier available
- ✅ Easy setup (no credit card for free tier)
- ✅ Automatic deployments from Git
- ✅ Built-in PostgreSQL and Redis
- ✅ Good for hackathon demos

### Step 1: Prepare Your Repository

```bash
# 1. Initialize Git (if not already done)
git init

# 2. Add all files
git add .

# 3. Commit
git commit -m "Initial commit - Reportify ready for deployment"

# 4. Create GitHub repository
# Go to https://github.com/new
# Name: reportify
# Description: AI-Powered Report Writing Assistant
# Public repository

# 5. Push to GitHub
git remote add origin https://github.com/YOUR_USERNAME/reportify.git
git branch -M main
git push -u origin main
```

### Step 2: Sign Up for Render

1. Go to https://render.com
2. Click "Get Started"
3. Sign up with GitHub
4. Authorize Render to access your repositories

### Step 3: Create PostgreSQL Database

1. Click "New +" → "PostgreSQL"
2. **Name:** `reportify-db`
3. **Database:** `reportify`
4. **User:** `reportify`
5. **Region:** Oregon (US West)
6. **Plan:** Free
7. Click "Create Database"
8. **Wait 2-3 minutes** for database to be ready
9. **Copy the Internal Database URL** (you'll need this)

### Step 4: Create Redis Instance

1. Click "New +" → "Redis"
2. **Name:** `reportify-redis`
3. **Region:** Oregon (US West)
4. **Plan:** Free
5. Click "Create Redis"
6. **Wait 1-2 minutes** for Redis to be ready
7. **Copy the Internal Redis URL** (you'll need this)

### Step 5: Deploy Backend API

1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. **Name:** `reportify-backend`
4. **Region:** Oregon (US West)
5. **Branch:** main
6. **Root Directory:** Leave empty
7. **Environment:** Python 3
8. **Build Command:**
   ```bash
   cd backend && pip install -r requirements.txt
   ```
9. **Start Command:**
   ```bash
   cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
10. **Plan:** Free

11. **Environment Variables** - Click "Advanced" and add:
    ```
    DATABASE_URL = [Paste Internal Database URL from Step 3]
    REDIS_URL = [Paste Internal Redis URL from Step 4]
    CELERY_BROKER_URL = [Paste Internal Redis URL from Step 4]
    CELERY_RESULT_BACKEND = [Paste Internal Redis URL from Step 4]
    OPENAI_API_KEY = sk-your-openai-key-here
    SECRET_KEY = [Generate random string: openssl rand -hex 32]
    ALGORITHM = HS256
    ACCESS_TOKEN_EXPIRE_MINUTES = 30
    REFRESH_TOKEN_EXPIRE_DAYS = 7
    DEBUG = False
    ALLOWED_ORIGINS = https://reportify-frontend.onrender.com
    S3_ENDPOINT_URL = http://localhost:9000
    S3_ACCESS_KEY = minioadmin
    S3_SECRET_KEY = minioadmin
    S3_BUCKET_NAME = reportify-files
    QDRANT_URL = http://localhost:6333
    ```

12. Click "Create Web Service"
13. **Wait 5-10 minutes** for deployment
14. **Copy the URL** (e.g., https://reportify-backend.onrender.com)

### Step 6: Run Database Migrations

1. Go to your backend service
2. Click "Shell" tab
3. Run:
   ```bash
   cd backend
   alembic upgrade head
   ```

### Step 7: Deploy Celery Worker

1. Click "New +" → "Background Worker"
2. Connect your GitHub repository
3. **Name:** `reportify-worker`
4. **Region:** Oregon (US West)
5. **Branch:** main
6. **Build Command:**
   ```bash
   cd backend && pip install -r requirements.txt
   ```
7. **Start Command:**
   ```bash
   cd backend && celery -A app.worker.celery_app worker --loglevel=info
   ```
8. **Environment Variables** - Same as backend (copy from Step 5)
9. Click "Create Background Worker"

### Step 8: Deploy Frontend

1. Click "New +" → "Static Site"
2. Connect your GitHub repository
3. **Name:** `reportify-frontend`
4. **Region:** Oregon (US West)
5. **Branch:** main
6. **Root Directory:** Leave empty
7. **Build Command:**
   ```bash
   cd frontend && npm install && npm run build
   ```
8. **Publish Directory:** `frontend/dist`
9. **Environment Variables:**
   ```
   VITE_API_URL = [Paste backend URL from Step 5]
   ```
10. Click "Create Static Site"
11. **Wait 3-5 minutes** for deployment
12. **Copy the URL** (e.g., https://reportify-frontend.onrender.com)

### Step 9: Update Backend CORS

1. Go back to backend service
2. Update `ALLOWED_ORIGINS` environment variable:
   ```
   ALLOWED_ORIGINS = [Paste frontend URL from Step 8]
   ```
3. Save and wait for redeployment

### Step 10: Test Your Deployment

1. Open your frontend URL
2. You should see the landing page
3. Click "Get Started" and register
4. Create a report
5. Upload template
6. Test all features

---

## 🎯 Option 2: Deploy to Railway (Alternative)

### Why Railway?
- ✅ Very easy setup
- ✅ Free tier with $5 credit
- ✅ One-click PostgreSQL and Redis
- ⚠️ Requires credit card (even for free tier)

### Quick Steps

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose your repository
6. Railway will auto-detect and deploy
7. Add PostgreSQL and Redis from marketplace
8. Set environment variables
9. Done!

---

## 🎯 Option 3: Vercel (Frontend) + Render (Backend)

### Why This Combo?
- ✅ Vercel is fastest for frontend
- ✅ Render handles backend well
- ✅ Both have free tiers

### Frontend on Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy frontend
cd frontend
vercel

# Follow prompts
# Set VITE_API_URL to your backend URL
```

### Backend on Render
Follow Steps 3-7 from Option 1 above

---

## ⚠️ Important Notes

### Free Tier Limitations

**Render Free Tier:**
- Services spin down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- 750 hours/month (enough for demo)
- No credit card required

**Solutions:**
- Keep services warm with uptime monitoring (UptimeRobot)
- Mention in demo: "First load may take a moment"
- For hackathon demo, this is perfectly acceptable

### Environment Variables

**Critical variables:**
- `OPENAI_API_KEY` - Your OpenAI API key
- `SECRET_KEY` - Generate with: `openssl rand -hex 32`
- `DATABASE_URL` - From Render PostgreSQL
- `REDIS_URL` - From Render Redis
- `ALLOWED_ORIGINS` - Your frontend URL

### Database

**For production:**
- Use PostgreSQL (not SQLite)
- Run migrations: `alembic upgrade head`
- Backup regularly

### File Storage

**Current setup uses MinIO locally:**
- For production, use AWS S3 or similar
- Or disable file uploads for demo
- Or use Render's disk storage (temporary)

---

## 🐛 Troubleshooting

### Backend Won't Start

**Check:**
1. All environment variables set correctly
2. Database URL is correct
3. Build command succeeded
4. Logs for error messages

**Solution:**
```bash
# In Render Shell
cd backend
python -c "from app.core.database import engine; print(engine)"
```

### Frontend Shows Blank Page

**Check:**
1. Build succeeded
2. `VITE_API_URL` is set correctly
3. Browser console for errors

**Solution:**
- Check Network tab in browser dev tools
- Verify API URL is accessible
- Check CORS settings in backend

### Database Connection Failed

**Check:**
1. Database is running
2. Connection string is correct
3. Database migrations ran

**Solution:**
```bash
# Run migrations
cd backend
alembic upgrade head
```

### Celery Worker Not Processing

**Check:**
1. Redis URL is correct
2. Worker is running
3. Worker logs for errors

**Solution:**
- Restart worker service
- Check Redis connection
- Verify environment variables

---

## 📊 Deployment Checklist

### Before Deployment
- [ ] All features tested locally
- [ ] Code committed to Git
- [ ] GitHub repository created
- [ ] .gitignore configured
- [ ] Environment variables documented
- [ ] OpenAI API key ready

### During Deployment
- [ ] PostgreSQL database created
- [ ] Redis instance created
- [ ] Backend deployed
- [ ] Database migrations run
- [ ] Celery worker deployed
- [ ] Frontend deployed
- [ ] CORS configured

### After Deployment
- [ ] Landing page loads
- [ ] Registration works
- [ ] Login works
- [ ] Report creation works
- [ ] Template upload works
- [ ] Search works
- [ ] AI generation works
- [ ] Export works

---

## 🎬 For Demo Video

### Mention Deployment

**In your demo:**
"Reportify is fully deployed and accessible online at [your-url]. It's running on Render's free tier with PostgreSQL, Redis, and includes a Celery worker for async processing."

### Show Live URL

**Start demo with:**
1. Show the live URL in browser
2. Show the landing page
3. Sign up with a new account
4. Continue with feature demo

### Highlight Architecture

**Mention:**
- "Backend API deployed separately"
- "Frontend static site on CDN"
- "PostgreSQL database for persistence"
- "Redis for caching and task queue"
- "Celery worker for async processing"

---

## 💰 Cost Breakdown

### Free Tier (Recommended for Hackathon)

**Render:**
- PostgreSQL: Free (1GB storage)
- Redis: Free (25MB)
- Web Service (Backend): Free (750 hours/month)
- Background Worker (Celery): Free (750 hours/month)
- Static Site (Frontend): Free (100GB bandwidth)

**Total: $0/month**

### If You Need More

**Render Paid:**
- PostgreSQL: $7/month (10GB)
- Redis: $10/month (100MB)
- Web Service: $7/month (always on)

**Total: ~$24/month**

---

## 🚀 Quick Deploy Script

Save this as `deploy.sh`:

```bash
#!/bin/bash

echo "🚀 Deploying Reportify..."

# Commit changes
git add .
git commit -m "Deploy: $(date)"
git push origin main

echo "✅ Code pushed to GitHub"
echo "📝 Now go to Render and deploy from dashboard"
echo "🔗 https://dashboard.render.com"
```

---

## 📞 Support

If you encounter issues:

1. **Check Render Logs**
   - Go to service → Logs tab
   - Look for error messages

2. **Check Documentation**
   - Render Docs: https://render.com/docs
   - Railway Docs: https://docs.railway.app

3. **Common Issues**
   - Database connection: Check connection string
   - CORS errors: Check ALLOWED_ORIGINS
   - Build failures: Check build logs

---

## 🎉 You're Ready to Deploy!

Follow Option 1 (Render) for the easiest deployment experience.

**Estimated time:** 15-20 minutes  
**Cost:** $0  
**Result:** Fully deployed, production-ready app

**Good luck with your deployment!** 🚀

---

**Next Steps:**
1. Follow Option 1 instructions above
2. Test your deployed app
3. Update README with live URL
4. Record demo video with live app
5. Submit to hackathon!
