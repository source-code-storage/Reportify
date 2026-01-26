# Quick Start Guide - AI Backend Testing

## 🚀 Start in 3 Minutes

### Step 1: Install Dependencies (1 min)
```bash
cd backend
pip install -r requirements-minimal.txt
```

### Step 2: Start Services (30 sec)
```bash
# Terminal 1: Qdrant
docker run -p 6333:6333 qdrant/qdrant

# Terminal 2: Backend
cd backend
python test_frontend_integration.py
```

### Step 3: Set API Key (30 sec)
```bash
# Edit backend/.env
OPENAI_API_KEY=sk-your-key-here
```

### Step 4: Test! (1 min)
```bash
# Option A: Interactive docs
open http://localhost:8000/docs

# Option B: Test script
python test_api_flow.py

# Option C: Quick check
curl http://localhost:8000/health
```

---

## 📝 Quick Test Flow

```bash
# 1. Create test note
echo "Machine learning is awesome!" > test_note.txt

# 2. Upload note (generates embeddings automatically)
curl -X POST "http://localhost:8000/api/v1/notes/upload" \
  -F "report_id=1" \
  -F "file=@test_note.txt"

# 3. Generate AI content
curl -X POST "http://localhost:8000/api/v1/content/generate" \
  -H "Content-Type: application/json" \
  -d '{"section_id":1,"section_description":"Intro to ML"}'
```

---

## 🎯 Key Endpoints

```
http://localhost:8000/docs          Interactive API docs
http://localhost:8000/health        Health check
http://localhost:8000/api/v1/       API info

POST /api/v1/notes/upload           Upload note
POST /api/v1/content/generate       Generate AI content
POST /api/v1/content/improve        Improve content
POST /api/v1/content/expand         Expand content
GET  /api/v1/content/search         Search notes
```

---

## ✅ Success Checklist

- [ ] Backend running on port 8000
- [ ] Qdrant running on port 6333
- [ ] OpenAI API key set in .env
- [ ] Can access /docs
- [ ] Can upload a note
- [ ] Can generate AI content

---

## 🐛 Quick Fixes

**"Connection refused"**
```bash
docker run -p 6333:6333 qdrant/qdrant
```

**"API key not configured"**
```bash
echo "OPENAI_API_KEY=sk-your-key" >> backend/.env
```

**"Module not found"**
```bash
pip install -r requirements-minimal.txt
```

---

## 💡 What to Test

1. **Upload a note** - System generates embeddings
2. **Search notes** - Semantic search works
3. **Generate content** - AI creates text with citations
4. **Check costs** - Token usage tracked

---

## 📚 Full Documentation

- `API_ENDPOINTS_COMPLETE.md` - All API details
- `READY_TO_TEST.md` - Complete testing guide
- `AI_INFRASTRUCTURE_COMPLETE.md` - Technical details

---

## 🎉 You're Ready!

Everything is set up. Just start the services and test!

```bash
# Start everything
docker run -p 6333:6333 qdrant/qdrant &
cd backend && python test_frontend_integration.py
```

Then open: http://localhost:8000/docs
