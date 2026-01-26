# 🚀 Quick GitHub Push Guide

## 📋 **5-Minute Setup**

### **Step 1: Create GitHub Repository (2 minutes)**

1. Go to https://github.com/new
2. Repository name: `reportify`
3. Description: "AI-Powered Report Writing Assistant - Built for Dynamous Kiro Hackathon"
4. **Public** ✅
5. **DO NOT** check any initialization options
6. Click "Create repository"

---

### **Step 2: Push Your Code (3 minutes)**

#### **Option A: Use the Automated Script** ⭐ Recommended

```bash
# Just run this:
GITHUB_SETUP.bat
```

When prompted, enter your GitHub username.

#### **Option B: Manual Commands**

```bash
# 1. Remove old remote
git remote remove origin

# 2. Add your new remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/reportify.git

# 3. Stage all files
git add .

# 4. Commit
git commit -m "Initial commit: Reportify - AI-Powered Report Writing Assistant"

# 5. Push
git branch -M main
git push -u origin main
```

---

### **Step 3: Verify (1 minute)**

1. Visit `https://github.com/YOUR_USERNAME/reportify`
2. Check that files are there
3. **CRITICAL**: Verify `.env` files are NOT visible

---

## ⚠️ **CRITICAL SECURITY CHECK**

Before pushing, verify `.env` is ignored:

```bash
git status
```

If you see `backend/.env` in the output, **STOP** and run:

```bash
git reset
```

Then contact me for help.

---

## 🎯 **What Happens Next?**

After pushing to GitHub:

1. ✅ Your code is safely backed up
2. ✅ Judges can review your work
3. ✅ You can deploy to Render
4. ✅ You can share the repository link

---

## 📝 **After Pushing - Update README**

Edit these in your README on GitHub:

1. Replace `YOUR_USERNAME` with your GitHub username
2. Add your email address
3. Add demo video URL (after uploading to YouTube)
4. Add live deployment URL (after deploying to Render)

---

## 🎬 **Demo Video**

### **Render the Video**

```bash
cd remotion-demo
npm run build
```

Video will be in: `remotion-demo/out/reportify-demo.mp4`

### **Upload to YouTube**

1. Go to YouTube Studio
2. Click "Create" → "Upload videos"
3. Select `reportify-demo.mp4`
4. Title: "Reportify - AI-Powered Report Writing Assistant Demo"
5. Description: Copy from README
6. Visibility: "Unlisted" or "Public"
7. Copy video URL
8. Update README with URL

---

## 🚀 **Deploy to Render**

After pushing to GitHub, follow `DEPLOY_NOW.md` to deploy your app.

**Quick steps:**
1. Create Render account
2. Connect GitHub repository
3. Deploy services (15 minutes)
4. Update README with live URLs

---

## ✅ **Success Checklist**

- [ ] Repository created on GitHub
- [ ] Code pushed successfully
- [ ] No `.env` files visible on GitHub
- [ ] README updated with your information
- [ ] Demo video uploaded to YouTube
- [ ] README updated with video URL
- [ ] App deployed to Render (optional)
- [ ] README updated with live URL (optional)

---

## 🆘 **Need Help?**

### **Common Issues**

**"Permission denied"**
- Use Personal Access Token instead of password
- Go to GitHub Settings → Developer settings → Personal access tokens
- Generate token with `repo` scope
- Use token as password

**"Large file" error**
- Remove large files: `git rm --cached path/to/file`
- Commit and push again

**".env visible on GitHub"**
- Remove immediately: `git rm --cached backend/.env`
- Commit and push
- **Change all API keys!**

---

## 🎉 **You're Done!**

Your repository is now on GitHub and ready for the hackathon submission!

**Next steps:**
1. Deploy to Render (optional but recommended)
2. Record and upload demo video
3. Update README with all URLs
4. Submit to hackathon

**Good luck!** 🚀

---

**Quick Links:**
- Full checklist: `GITHUB_PUSH_CHECKLIST.md`
- Deployment guide: `DEPLOY_NOW.md`
- Project overview: `PROJECT_OVERVIEW.md`
