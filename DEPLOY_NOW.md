# 🚀 Deploy Reportify Now - Quick Guide

**Time:** 15 minutes  
**Cost:** Free  
**Platform:** Render

---

## Step 1: Push to GitHub (5 minutes)

```bash
# 1. Initialize Git
git init

# 2. Add all files
git add .

# 3. Commit
git commit -m "Reportify - Ready for deployment"

# 4. Create GitHub repo
# Go to: https://github.com/new
# Name: reportify
# Public repository
# Click "Create repository"

# 5. Push
git remote add origin https://github.com/YOUR_USERNAME/reportify.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy on Render (10 minutes)

### A. Sign Up
1. Go to https://render.com
2. Click "Get Started"
3. Sign up with GitHub

### B. Create Database
1. Click "New +" → "PostgreSQL"
2. Name: `reportify-db`
3. Plan: **Free**
4. Click "Create"
5. **Copy Internal Database URL**

### C. Create Redis
1. Click "New +" → "Redis"
2. Name: `reportify-redis`
3. Plan: **Free**
4. Click "Create"
5. **Copy Internal Redis URL**

### D. Deploy Backend
1. Click "New +" → "Web Service"
2. Connect your `reportify` repo
3. Name: `reportify-backend`
4. Build Command:
   ```
   cd backend && pip install -r requirements.txt
   ```
5. Start Command:
   ```
   cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT
   ```
6. Plan: **Free**
7. Add Environment Variables:
   ```
   DATABASE_URL = [Paste Database URL]
   REDIS_URL = [Paste Redis URL]
   CELERY_BROKER_URL = [Paste Redis URL]
   OPENAI_API_KEY = [Your OpenAI Key]
   SECRET_KEY = [Random string - use: openssl rand -hex 32]
   ALLOWED_ORIGINS = https://reportify-frontend.onrender.com
   DEBUG = False
   ```
8. Click "Create Web Service"
9. **Wait 5 minutes**
10. **Copy backend URL**

### E. Run Migrations
1. Go to backend service
2. Click "Shell" tab
3. Run:
   ```bash
   cd backend
   alembic upgrade head
   ```

### F. Deploy Frontend
1. Click "New +" → "Static Site"
2. Connect your `reportify` repo
3. Name: `reportify-frontend`
4. Build Command:
   ```
   cd frontend && npm install && npm run build
   ```
5. Publish Directory: `frontend/dist`
6. Add Environment Variable:
   ```
   VITE_API_URL = [Paste backend URL]
   ```
7. Click "Create Static Site"
8. **Wait 3 minutes**
9. **Copy frontend URL**

### G. Update CORS
1. Go back to backend service
2. Update `ALLOWED_ORIGINS`:
   ```
   ALLOWED_ORIGINS = [Paste frontend URL]
   ```
3. Save

---

## Step 3: Test (2 minutes)

1. Open your frontend URL
2. See the landing page ✅
3. Click "Get Started"
4. Register an account
5. Create a report
6. Done! 🎉

---

## 🎯 Your URLs

After deployment, you'll have:

- **Frontend:** https://reportify-frontend.onrender.com
- **Backend:** https://reportify-backend.onrender.com
- **API Docs:** https://reportify-backend.onrender.com/docs

---

## ⚠️ Important Notes

### First Load
- Free tier services sleep after 15 min
- First request takes 30-60 seconds
- This is normal for free tier
- Perfect for hackathon demo

### Keep Warm (Optional)
Use UptimeRobot to ping your app every 5 minutes:
1. Go to https://uptimerobot.com
2. Add monitor for your frontend URL
3. Check every 5 minutes

---

## 🐛 If Something Goes Wrong

### Backend won't start?
- Check logs in Render dashboard
- Verify all environment variables
- Check DATABASE_URL is correct

### Frontend shows blank page?
- Check VITE_API_URL is correct
- Check browser console for errors
- Verify backend is running

### Database error?
- Run migrations: `alembic upgrade head`
- Check DATABASE_URL format

---

## ✅ Deployment Checklist

- [ ] Code pushed to GitHub
- [ ] PostgreSQL created
- [ ] Redis created
- [ ] Backend deployed
- [ ] Migrations run
- [ ] Frontend deployed
- [ ] CORS updated
- [ ] App tested
- [ ] URLs saved

---

## 🎬 For Your Demo

**Mention in video:**
"Reportify is fully deployed and live at [your-url]. It's running on Render with PostgreSQL and Redis, demonstrating a production-ready architecture."

---

## 🚀 You're Done!

Your app is now live and accessible to anyone!

**Share your URL:**
- Add to README
- Add to hackathon submission
- Share with judges
- Show in demo video

**Congratulations!** 🎉
