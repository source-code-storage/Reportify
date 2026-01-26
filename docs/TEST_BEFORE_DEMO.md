# 🧪 Test Before Demo - Complete Workflow

**Purpose:** Verify all features work before recording demo video  
**Time Required:** 15-20 minutes  
**Date:** January 18, 2026

---

## ✅ Pre-Test Checklist

### 1. Verify All Services Running

```bash
# Run verification script
verify_deployment.bat

# Should show: ALL CHECKS PASSED!
```

### 2. Prepare Test Data

**You'll need:**
- [ ] A PDF template (your report template)
- [ ] 2-3 note files (PDF, text, or images)
- [ ] Test email address (e.g., test@example.com)
- [ ] Test password (e.g., Test123!)

---

## 🎯 Complete User Workflow Test

### Step 1: Authentication (2 minutes)

#### 1.1 Register New User
1. Open http://localhost:5173
2. Click "Create one now"
3. Fill in:
   - Email: `test@example.com`
   - Password: `Test123!`
   - Full Name: `Test User`
4. Click "Sign Up"
5. **✅ Verify:** Redirected to login page

#### 1.2 Login
1. Enter email: `test@example.com`
2. Enter password: `Test123!`
3. Click "Sign In"
4. **✅ Verify:** Redirected to dashboard

---

### Step 2: Report Creation (3 minutes)

#### 2.1 Create Report Without Template
1. Click "Create New Report" button
2. Fill in:
   - Title: `Test Report 1`
   - Description: `Testing without template`
3. Click "Create Report"
4. **✅ Verify:** Report appears in dashboard
5. **✅ Verify:** Progress shows 0%

#### 2.2 Create Report With Template
1. Click "Create New Report" button
2. Fill in:
   - Title: `Test Report 2 - With Template`
   - Description: `Testing with PDF template`
3. Click "Choose File" and select your PDF template
4. Click "Create Report"
5. **✅ Verify:** Report appears in dashboard
6. Click on the report to open it
7. **✅ Verify:** Sections appear from template
8. **✅ Verify:** Section titles match template structure

**Expected Sections (example):**
- Introduction
- Methodology
- Results
- Conclusion
- References

---

### Step 3: Note Upload (3 minutes)

#### 3.1 Upload First Note
1. In report detail page, click "Upload Notes" button
2. Select a PDF file (e.g., research paper, article)
3. Click "Upload"
4. **✅ Verify:** Upload progress shows
5. **✅ Verify:** Note appears in notes list
6. **✅ Verify:** Status changes to "Processing" then "Completed"

**Check Celery logs:**
```
[INFO] Task app.worker.tasks.pdf.process_note received
[INFO] Task app.worker.tasks.pdf.process_note succeeded
```

#### 3.2 Upload Second Note
1. Click "Upload Notes" again
2. Select a text file or another PDF
3. Click "Upload"
4. **✅ Verify:** Second note appears
5. **✅ Verify:** Processing completes

#### 3.3 Upload Image (Optional)
1. Click "Upload Notes" again
2. Select an image file (PNG, JPG)
3. Click "Upload"
4. **✅ Verify:** OCR processing occurs
5. **✅ Verify:** Text extracted from image

---

### Step 4: Semantic Search (3 minutes)

#### 4.1 Basic Search
1. Click "Search Notes" tab
2. Enter search query: `methodology`
3. Click "Search" or press Enter
4. **✅ Verify:** Results appear
5. **✅ Verify:** Results show relevance scores
6. **✅ Verify:** Results show snippets from notes

#### 4.2 Semantic Search Test
1. Enter query: `how to conduct research`
2. **✅ Verify:** Results include related concepts like:
   - "research methodology"
   - "data collection"
   - "analysis techniques"
3. **Note:** Results are semantic, not just keyword matches

#### 4.3 Different Query
1. Enter query related to your notes
2. **✅ Verify:** Relevant results appear
3. **✅ Verify:** Results ranked by similarity

---

### Step 5: AI Content Generation (4 minutes)

#### 5.1 Generate Content for Section
1. Click on a section (e.g., "Introduction")
2. Click "Generate Content" button
3. **✅ Verify:** Loading indicator appears
4. **✅ Verify:** Content generates (may take 10-30 seconds)
5. **✅ Verify:** Generated content appears in editor
6. **✅ Verify:** Content is relevant to section title
7. **✅ Verify:** Content references uploaded notes

**Check Backend logs:**
```
INFO: Generating content for section...
INFO: Using OpenAI GPT-4...
INFO: Content generated successfully
```

#### 5.2 Edit Generated Content
1. Click in the editor
2. Make manual edits to the text
3. **✅ Verify:** Changes are saved automatically
4. **✅ Verify:** Word count updates

#### 5.3 Generate for Another Section
1. Click on different section (e.g., "Methodology")
2. Click "Generate Content"
3. **✅ Verify:** Different content generated
4. **✅ Verify:** Content appropriate for section

---

### Step 6: Export Functionality (3 minutes)

#### 6.1 Export to PDF
1. Click "Export" button
2. Select "PDF" format
3. Click "Export"
4. **✅ Verify:** Download starts
5. **✅ Verify:** PDF file downloads
6. Open the PDF file
7. **✅ Verify:** All sections included
8. **✅ Verify:** Content formatted properly
9. **✅ Verify:** Professional appearance

#### 6.2 Export to DOCX
1. Click "Export" button again
2. Select "DOCX" format
3. Click "Export"
4. **✅ Verify:** Download starts
5. **✅ Verify:** DOCX file downloads
6. Open in Microsoft Word or similar
7. **✅ Verify:** All sections included
8. **✅ Verify:** Content editable
9. **✅ Verify:** Formatting preserved

---

### Step 7: Additional Features (2 minutes)

#### 7.1 Progress Tracking
1. Go back to dashboard
2. **✅ Verify:** Report shows progress percentage
3. **✅ Verify:** Progress based on completed sections
4. Mark a section as complete
5. **✅ Verify:** Progress updates

#### 7.2 Report Management
1. Click on report title to edit
2. Update title or description
3. **✅ Verify:** Changes saved
4. Go back to dashboard
5. **✅ Verify:** Updated info shows

#### 7.3 Logout and Login
1. Click "Logout" button
2. **✅ Verify:** Redirected to login page
3. Login again
4. **✅ Verify:** All data persists
5. **✅ Verify:** Reports still there
6. **✅ Verify:** Notes still there

---

## 🐛 Common Issues and Solutions

### Issue: Note Upload Fails
**Solution:**
- Check Celery worker is running
- Check file size (max 50MB)
- Check file type is allowed
- Check backend logs for errors

### Issue: Search Returns No Results
**Solution:**
- Wait for note processing to complete
- Check Qdrant is running: `docker ps | findstr qdrant`
- Try different search query
- Check backend logs

### Issue: Content Generation Fails
**Solution:**
- Verify OpenAI API key in `.env`
- Check OpenAI API credits/limits
- Check backend logs for error message
- Try again (may be temporary API issue)

### Issue: Export Doesn't Work
**Solution:**
- Check browser allows downloads
- Check backend logs for errors
- Try different format (PDF vs DOCX)
- Verify report has content

---

## 📊 Test Results Checklist

### Authentication ✅
- [ ] Registration works
- [ ] Login works
- [ ] Logout works
- [ ] Session persists

### Report Management ✅
- [ ] Create report works
- [ ] Template upload works
- [ ] Sections extracted from template
- [ ] Report list shows correctly
- [ ] Report details load

### File Processing ✅
- [ ] Note upload works
- [ ] PDF processing works
- [ ] Text extraction works
- [ ] OCR works (for images)
- [ ] Embeddings generated

### Search ✅
- [ ] Search returns results
- [ ] Results are relevant
- [ ] Semantic matching works
- [ ] Results show snippets

### AI Generation ✅
- [ ] Content generates
- [ ] Content is relevant
- [ ] Content references notes
- [ ] Multiple sections work
- [ ] Manual editing works

### Export ✅
- [ ] PDF export works
- [ ] DOCX export works
- [ ] Formatting preserved
- [ ] All content included

---

## 🎬 Ready for Demo Video?

### If All Tests Pass ✅
**You're ready to record!**

1. Close all test data
2. Create fresh test account for demo
3. Prepare clean demo data
4. Follow demo script in PRE_SUBMISSION_CHECKLIST.md
5. Record with confidence!

### If Tests Fail ❌
**Fix issues first:**

1. Note which tests failed
2. Check logs for errors
3. Fix issues
4. Re-run tests
5. Verify fixes work
6. Then record demo

---

## 📝 Notes for Demo Recording

### What Worked Well
- List features that worked perfectly
- Note any impressive results
- Highlight fast performance

### What to Emphasize
- Semantic search (not just keywords)
- AI content quality
- Professional UI
- Complete workflow

### What to Avoid
- Don't show any errors
- Don't use test data with errors
- Don't rush through features
- Don't skip important steps

---

## ✅ Final Verification

Before recording demo:

```bash
# 1. Restart all services fresh
docker-compose restart
# Restart backend (Ctrl+C and restart)
# Restart Celery (Ctrl+C and restart)
# Restart frontend (Ctrl+C and restart)

# 2. Run verification
verify_deployment.bat

# 3. Test one complete workflow
# Follow steps above

# 4. If all passes, you're ready!
```

---

## 🎯 Success Criteria

### Minimum Requirements
- [x] All services running
- [x] User can register and login
- [x] User can create report
- [x] User can upload notes
- [x] Search returns results
- [x] AI generates content
- [x] Export produces files

### Ideal State
- [x] All features work smoothly
- [x] No errors during workflow
- [x] Fast performance
- [x] Professional appearance
- [x] Impressive results

---

## 🚀 You're Ready!

If all tests pass, you have a **fully functional, production-ready application** that:

✅ Solves a real problem  
✅ Uses cutting-edge AI technology  
✅ Has a professional UI  
✅ Works end-to-end  
✅ Is ready for demo  

**Go record that demo video!** 🎬

---

**Test Date:** _____________  
**Test Result:** ⬜ Pass ⬜ Fail  
**Issues Found:** _____________  
**Ready for Demo:** ⬜ Yes ⬜ No  

---

**Good luck!** 🌟
