# Test Checklist - AI Report Writing Assistant

## Pre-Test Setup ✅

- [ ] Backend dependencies installed (`pip install -r requirements-minimal.txt`)
- [ ] Qdrant running (`docker run -p 6333:6333 qdrant/qdrant`)
- [ ] OpenAI API key set in `backend/.env` ✅ (Already done!)
- [ ] Backend running (`python test_frontend_integration.py`)
- [ ] Frontend running (`npm run dev`)

---

## Test 1: File Upload & Embedding Generation

- [ ] Navigate to http://localhost:5174
- [ ] Login/Register
- [ ] Create a new report
- [ ] Open the report
- [ ] Go to "Notes & Files" tab
- [ ] Upload a .txt file with research notes
- [ ] Verify upload progress shows
- [ ] Verify status changes: uploading → processing → completed
- [ ] Check browser console for success message
- [ ] Check backend logs for embedding generation

**Expected Result:**
```
✅ File uploaded
✅ Text extracted
✅ Embeddings generated (384 dimensions)
✅ Stored in Qdrant
✅ Status: completed
```

---

## Test 2: AI Content Generation (THE MAIN FEATURE!)

- [ ] Go to "Editor" tab
- [ ] Select a section from sidebar
- [ ] Click "Generate" button
- [ ] Wait 5-10 seconds
- [ ] Verify AI-generated content appears
- [ ] Verify content includes citations (Source 1, Source 2, etc.)
- [ ] Check browser console for:
  - [ ] Model: gpt-4
  - [ ] Tokens used
  - [ ] Estimated cost
  - [ ] Number of sources

**Expected Result:**
```
✅ Content generated in 5-10 seconds
✅ Well-written academic text
✅ Citations included
✅ Cost: ~$0.01-0.05
✅ Console shows metadata
```

---

## Test 3: Content Improvement

- [ ] After generating content, click "Improve" button
- [ ] Wait 3-5 seconds
- [ ] Verify content is enhanced
- [ ] Check console for cost

**Expected Result:**
```
✅ Content improved
✅ Better clarity and grammar
✅ Cost tracked
```

---

## Test 4: Content Expansion

- [ ] Click "Expand" button
- [ ] Wait 3-5 seconds
- [ ] Verify content has more detail
- [ ] Check console for cost

**Expected Result:**
```
✅ Content expanded
✅ More depth added
✅ Cost tracked
```

---

## Test 5: Semantic Search

- [ ] Go to "Search Notes" tab
- [ ] Enter query: "What is machine learning?"
- [ ] Verify search results appear
- [ ] Verify relevance scores shown (0.0-1.0)
- [ ] Click "Insert" on a result
- [ ] Verify excerpt inserted into editor
- [ ] Verify auto-switch to Editor tab

**Expected Result:**
```
✅ Search results appear instantly
✅ Relevance scores displayed
✅ Can insert excerpts
✅ Citations maintained
```

---

## Test 6: Multiple Notes

- [ ] Upload 2-3 different notes
- [ ] Wait for all to process
- [ ] Generate content for a section
- [ ] Verify content uses multiple sources
- [ ] Check console for number of sources used

**Expected Result:**
```
✅ Multiple notes processed
✅ Content draws from all relevant notes
✅ Multiple citations
```

---

## Test 7: Error Handling

### Test 7a: No Notes Uploaded
- [ ] Try to generate content without uploading notes
- [ ] Verify error message shown

### Test 7b: Invalid File Type
- [ ] Try to upload a .exe or .zip file
- [ ] Verify error message shown

### Test 7c: Empty Content
- [ ] Try to improve/expand empty section
- [ ] Verify error message shown

**Expected Result:**
```
✅ Appropriate error messages
✅ No crashes
✅ User-friendly feedback
```

---

## Test 8: Cost Tracking

- [ ] Perform multiple AI operations
- [ ] Check console for cost of each operation
- [ ] Verify costs are reasonable

**Expected Costs:**
```
Generate: $0.01-0.05
Improve: $0.01-0.03
Expand: $0.02-0.04
```

---

## Test 9: End-to-End Flow

Complete user journey:
- [ ] Register/Login
- [ ] Create report: "ML Research"
- [ ] Upload 2 research notes
- [ ] Wait for processing
- [ ] Generate content for Introduction
- [ ] Improve the content
- [ ] Expand the content
- [ ] Search for specific information
- [ ] Insert search result
- [ ] Save the section
- [ ] Check final report

**Expected Result:**
```
✅ Complete flow works
✅ All features functional
✅ Content is high quality
✅ Citations maintained
```

---

## Test 10: Performance

- [ ] Upload large file (5-10 MB)
- [ ] Verify processing completes
- [ ] Generate content
- [ ] Verify response time < 15 seconds

**Expected Result:**
```
✅ Large files handled
✅ Reasonable response times
✅ No timeouts
```

---

## Debugging Checklist

If something doesn't work:

### Backend Issues:
- [ ] Check backend is running on port 8000
- [ ] Check backend logs for errors
- [ ] Verify OpenAI API key in .env
- [ ] Check Qdrant is running on port 6333

### Frontend Issues:
- [ ] Check frontend is running on port 5174
- [ ] Check browser console for errors
- [ ] Verify API calls in Network tab
- [ ] Check authentication token

### API Issues:
- [ ] Test API directly: `curl http://localhost:8000/health`
- [ ] Check API docs: `http://localhost:8000/docs`
- [ ] Verify endpoints are accessible

---

## Success Criteria

All tests pass when:

✅ Files upload successfully
✅ Embeddings generated automatically
✅ AI content generation works
✅ Content includes citations
✅ Improve/Expand features work
✅ Semantic search works
✅ Costs are tracked
✅ Error handling works
✅ End-to-end flow completes

---

## Quick Test Commands

```bash
# Check backend health
curl http://localhost:8000/health

# Check API docs
open http://localhost:8000/docs

# Check Qdrant
open http://localhost:6333/dashboard

# Check frontend
open http://localhost:5174

# View backend logs
# (in terminal running backend)

# View browser console
# F12 in browser
```

---

## Test Results

Date: _____________

Tester: _____________

| Test | Status | Notes |
|------|--------|-------|
| 1. File Upload | ⬜ Pass ⬜ Fail | |
| 2. Content Generation | ⬜ Pass ⬜ Fail | |
| 3. Content Improvement | ⬜ Pass ⬜ Fail | |
| 4. Content Expansion | ⬜ Pass ⬜ Fail | |
| 5. Semantic Search | ⬜ Pass ⬜ Fail | |
| 6. Multiple Notes | ⬜ Pass ⬜ Fail | |
| 7. Error Handling | ⬜ Pass ⬜ Fail | |
| 8. Cost Tracking | ⬜ Pass ⬜ Fail | |
| 9. End-to-End | ⬜ Pass ⬜ Fail | |
| 10. Performance | ⬜ Pass ⬜ Fail | |

**Overall Result:** ⬜ All Pass ⬜ Some Failures

**Notes:**
_____________________________________________
_____________________________________________
_____________________________________________

---

## Ready to Test!

Start the services and work through this checklist. Good luck! 🚀
