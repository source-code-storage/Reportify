# API Endpoints Complete! 🎉

## What We Built

We've created comprehensive REST API endpoints to expose all AI services! Here's what's available:

### 📋 Report Management API
**Base URL:** `/api/v1/reports`

#### Endpoints:
- `POST /` - Create a new report
- `GET /` - List all user's reports
- `GET /{report_id}` - Get specific report with sections
- `PUT /{report_id}` - Update report
- `DELETE /{report_id}` - Delete report
- `POST /{report_id}/sections` - Create a section
- `PUT /{report_id}/sections/{section_id}` - Update section content

### 📝 Note Management API
**Base URL:** `/api/v1/notes`

#### Endpoints:
- `POST /upload` - Upload and process a note file
- `GET /` - List all notes for a report
- `GET /{note_id}` - Get specific note
- `DELETE /{note_id}` - Delete note

**Features:**
- Automatic text extraction
- Embedding generation
- Vector storage in Qdrant
- Support for .txt and .md files (PDF coming soon)

### 🤖 AI Content Generation API (THE MAIN FEATURE!)
**Base URL:** `/api/v1/content`

#### Endpoints:
- `POST /generate` - Generate AI content for a section
- `POST /improve` - Improve existing content
- `POST /expand` - Expand content with more detail
- `GET /search` - Semantic search across notes

**Features:**
- Semantic search to find relevant notes
- GPT-4 powered content generation
- Citations from source notes
- Token usage and cost tracking

---

## API Examples

### 1. Create a Report
```bash
curl -X POST "http://localhost:8000/api/v1/reports" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "My Research Report",
    "description": "A comprehensive report on machine learning"
  }'
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "title": "My Research Report",
  "description": "A comprehensive report on machine learning",
  "status": "draft",
  "progress_percentage": 0.0,
  "total_word_count": 0,
  "created_at": "2024-01-09T10:00:00Z",
  "sections": []
}
```

### 2. Create a Section
```bash
curl -X POST "http://localhost:8000/api/v1/reports/1/sections" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Introduction",
    "order": 1
  }'
```

### 3. Upload a Note
```bash
curl -X POST "http://localhost:8000/api/v1/notes/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "report_id=1" \
  -F "file=@research_notes.txt"
```

**What happens:**
1. File is uploaded
2. Text is extracted
3. Embeddings are generated
4. Stored in Qdrant for semantic search
5. Note status updated to "completed"

### 4. Generate AI Content (THE MAGIC!)
```bash
curl -X POST "http://localhost:8000/api/v1/content/generate" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "section_id": 1,
    "section_description": "Introduce machine learning concepts"
  }'
```

**Response:**
```json
{
  "content": "Machine learning is a method of data analysis that automates analytical model building (Source 1). It is a branch of artificial intelligence based on the idea that systems can learn from data, identify patterns and make decisions with minimal human intervention (Source 2)...",
  "sources": [
    {
      "score": 0.89,
      "note_id": 1,
      "chunk_index": 0,
      "chunk_text": "Machine learning is a method of data analysis...",
      "filename": "research_notes.txt",
      "file_type": "txt"
    }
  ],
  "metadata": {
    "model": "gpt-4",
    "input_tokens": 450,
    "output_tokens": 320,
    "total_tokens": 770,
    "estimated_cost": 0.0327,
    "instruction": "generate"
  }
}
```

### 5. Improve Content
```bash
curl -X POST "http://localhost:8000/api/v1/content/improve" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "section_id": 1
  }'
```

### 6. Expand Content
```bash
curl -X POST "http://localhost:8000/api/v1/content/expand" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "section_id": 1
  }'
```

### 7. Search Notes
```bash
curl -X GET "http://localhost:8000/api/v1/content/search?query=machine%20learning&report_id=1&limit=5" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Complete User Flow

### Step-by-Step Example:

```bash
# 1. Register/Login (get token)
TOKEN=$(curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}' \
  | jq -r '.access_token')

# 2. Create a report
REPORT_ID=$(curl -X POST "http://localhost:8000/api/v1/reports" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"ML Research Report","description":"Comprehensive ML study"}' \
  | jq -r '.id')

# 3. Create sections
SECTION_ID=$(curl -X POST "http://localhost:8000/api/v1/reports/$REPORT_ID/sections" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Introduction","order":1}' \
  | jq -r '.id')

# 4. Upload research notes
curl -X POST "http://localhost:8000/api/v1/notes/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "report_id=$REPORT_ID" \
  -F "file=@notes1.txt"

curl -X POST "http://localhost:8000/api/v1/notes/upload" \
  -H "Authorization: Bearer $TOKEN" \
  -F "report_id=$REPORT_ID" \
  -F "file=@notes2.txt"

# 5. Generate AI content for the section
curl -X POST "http://localhost:8000/api/v1/content/generate" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"section_id\":$SECTION_ID,\"section_description\":\"Introduce ML concepts\"}" \
  | jq '.'

# 6. Update section with generated content
curl -X PUT "http://localhost:8000/api/v1/reports/$REPORT_ID/sections/$SECTION_ID" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"content":"[Generated content here]","is_completed":true}'

# 7. Get report with all sections
curl -X GET "http://localhost:8000/api/v1/reports/$REPORT_ID" \
  -H "Authorization: Bearer $TOKEN" \
  | jq '.'
```

---

## Interactive API Documentation

FastAPI provides automatic interactive API documentation!

### Swagger UI:
```
http://localhost:8000/docs
```

### ReDoc:
```
http://localhost:8000/redoc
```

**Features:**
- Try out all endpoints
- See request/response schemas
- Test authentication
- View examples

---

## Testing the API

### Option 1: Using the Test Script

Create `backend/test_api_endpoints.py`:

```python
import requests
import json

BASE_URL = "http://localhost:8000/api/v1"

# 1. Login
response = requests.post(f"{BASE_URL}/auth/login", json={
    "email": "test@example.com",
    "password": "password"
})
token = response.json()["access_token"]
headers = {"Authorization": f"Bearer {token}"}

# 2. Create report
response = requests.post(f"{BASE_URL}/reports", 
    headers=headers,
    json={"title": "Test Report", "description": "Testing API"}
)
report = response.json()
print(f"Created report: {report['id']}")

# 3. Create section
response = requests.post(f"{BASE_URL}/reports/{report['id']}/sections",
    headers=headers,
    json={"title": "Introduction", "order": 1}
)
section = response.json()
print(f"Created section: {section['id']}")

# 4. Upload note
with open("test_note.txt", "rb") as f:
    response = requests.post(f"{BASE_URL}/notes/upload",
        headers=headers,
        data={"report_id": report['id']},
        files={"file": f}
    )
note = response.json()
print(f"Uploaded note: {note['id']}, status: {note['status']}")

# 5. Generate content
response = requests.post(f"{BASE_URL}/content/generate",
    headers=headers,
    json={
        "section_id": section['id'],
        "section_description": "Introduce the topic"
    }
)
result = response.json()
print(f"Generated content ({len(result['content'])} chars)")
print(f"Cost: ${result['metadata']['estimated_cost']}")
print(f"Sources: {len(result['sources'])}")
```

### Option 2: Using Postman

1. Import the API into Postman
2. Set base URL: `http://localhost:8000/api/v1`
3. Add Authorization header with Bearer token
4. Test each endpoint

### Option 3: Using curl (see examples above)

---

## Error Handling

All endpoints return standard HTTP status codes:

- `200 OK` - Success
- `201 Created` - Resource created
- `204 No Content` - Success with no response body
- `400 Bad Request` - Invalid input
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - Access denied
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error
- `503 Service Unavailable` - Service not configured (e.g., missing API key)

**Error Response Format:**
```json
{
  "detail": "Error message here"
}
```

---

## Authentication

All endpoints (except `/auth/login` and `/auth/register`) require authentication.

**Header Format:**
```
Authorization: Bearer YOUR_JWT_TOKEN
```

**Getting a Token:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'
```

---

## Rate Limiting & Costs

### OpenAI API Costs:
- GPT-4: ~$0.01-0.05 per section
- GPT-3.5-Turbo: ~$0.001-0.005 per section (10x cheaper)

### Recommendations:
1. Use GPT-3.5-Turbo for development/testing
2. Switch to GPT-4 for production
3. Monitor token usage in response metadata
4. Set up billing alerts in OpenAI dashboard

---

## Next Steps

### 1. Start the Backend
```bash
cd backend
python test_frontend_integration.py
```

### 2. Start Qdrant
```bash
docker run -p 6333:6333 qdrant/qdrant
```

### 3. Set API Key
```bash
# In backend/.env
OPENAI_API_KEY=sk-your-key-here
```

### 4. Test the API
```bash
# Visit interactive docs
open http://localhost:8000/docs

# Or use curl/Postman
curl http://localhost:8000/api/v1/
```

### 5. Connect Frontend
Update frontend to use real API endpoints instead of mock data!

---

## Summary

### ✅ What's Complete:
1. **Report Management API** - CRUD operations for reports and sections
2. **Note Management API** - Upload, process, and manage notes
3. **AI Content Generation API** - Generate, improve, expand content
4. **Semantic Search API** - Search notes by meaning
5. **Automatic Embedding Generation** - On note upload
6. **Vector Storage** - In Qdrant for fast search
7. **Authentication** - JWT-based security
8. **Error Handling** - Comprehensive error responses
9. **API Documentation** - Auto-generated Swagger/ReDoc

### 🎯 The Complete Flow:
```
Upload notes → Generate embeddings → Store in Qdrant
                                          ↓
Click "Generate" → Find relevant notes → Call GPT-4 → Return content
```

### 🚀 Ready to Test!
All API endpoints are ready. Just need to:
1. Start services (backend + Qdrant)
2. Set OpenAI API key
3. Test endpoints
4. Connect frontend

**The backend is complete! Time to test the AI magic!** ✨
