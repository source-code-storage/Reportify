# 🧪 Testing Guide - Current Features

## What's Working Right Now

✅ Authentication (login, register, logout)  
✅ Report Management (create, list, view, edit, delete)  
✅ Section Management (create, edit sections)  
✅ Progress Tracking (automatic calculation)  
✅ Word Count Tracking  

---

## Prerequisites

### 1. Start Backend Server
```bash
cd backend
uvicorn main:app --reload
```

**Expected Output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete.
```

### 2. Start Frontend Server
```bash
cd frontend
npm run dev
```

**Expected Output:**
```
VITE v5.x.x  ready in xxx ms
➜  Local:   http://localhost:5173/
```

---

## Test Scenarios

### Scenario 1: New User Registration & Login

**Steps:**
1. Open browser: http://localhost:5173
2. Click "Sign up" or go to /register
3. Fill in:
   - Name: Test User
   - Email: testuser@example.com
   - Password: password123
4. Click "Sign Up"

**Expected Result:**
- ✅ Redirected to dashboard
- ✅ See "My Reports" page
- ✅ No reports yet (empty state)

**Then Test Login:**
1. Logout (button in top right)
2. Go to /login
3. Enter same credentials
4. Click "Sign In"

**Expected Result:**
- ✅ Redirected to dashboard
- ✅ See your reports (if any)

---

### Scenario 2: Create a Report

**Steps:**
1. On dashboard, click "Create New Report"
2. Fill in:
   - Title: "My Final Year Report"
   - Description: "Report for my internship project"
   - Template: **Skip this** (or select a file - it will be ignored)
3. Click "Create Report"

**Expected Result:**
- ✅ Modal closes
- ✅ Redirected to report detail page
- ✅ Report shows with 0% progress
- ✅ No sections yet

---

### Scenario 3: Add Sections to Report

**Steps:**
1. In report detail page, you should see empty sections
2. Manually create sections using the API or wait for UI implementation

**Alternative - Use API Directly:**
```bash
# Get your access token from browser localStorage
# Then create sections:

curl -X POST "http://localhost:8000/api/v1/reports/1/sections?title=Introduction&order=1" \
  -H "Authorization: Bearer YOUR_TOKEN"

curl -X POST "http://localhost:8000/api/v1/reports/1/sections?title=Methodology&order=2" \
  -H "Authorization: Bearer YOUR_TOKEN"

curl -X POST "http://localhost:8000/api/v1/reports/1/sections?title=Results&order=3" \
  -H "Authorization: Bearer YOUR_TOKEN"

curl -X POST "http://localhost:8000/api/v1/reports/1/sections?title=Conclusion&order=4" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected Result:**
- ✅ Sections appear in the report
- ✅ Progress still 0% (no content yet)

---

### Scenario 4: Edit Section Content

**Steps:**
1. Click on a section (e.g., "Introduction")
2. Type some content in the editor:
   ```
   This is the introduction section. It provides an overview of the project 
   and its objectives. The main goal was to develop a comprehensive solution 
   for report writing assistance.
   ```
3. Mark section as complete (if UI allows)
4. Save changes

**Expected Result:**
- ✅ Content saved
- ✅ Word count updates
- ✅ Progress updates (25% if 1 of 4 sections complete)

---

### Scenario 5: Check Progress Calculation

**Steps:**
1. Complete 2 out of 4 sections
2. Go back to dashboard
3. View the report card

**Expected Result:**
- ✅ Progress shows 50%
- ✅ Word count shows total words
- ✅ Status can be updated

---

### Scenario 6: Update Report Details

**Steps:**
1. In report detail page
2. Edit report title or description
3. Change status to "in_progress"
4. Save changes

**Expected Result:**
- ✅ Changes saved
- ✅ Updated timestamp changes
- ✅ Status badge updates

---

### Scenario 7: Delete Report

**Steps:**
1. Go to dashboard
2. Click on a report (or use delete button if available)
3. Delete the report

**Expected Result:**
- ✅ Report removed from list
- ✅ All sections deleted (cascade)
- ✅ Redirected to dashboard

---

## API Testing (Alternative)

If frontend has issues, test backend directly:

### 1. Test Authentication
```bash
# Register
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123","name":"Test User"}'

# Login
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"password123"}'

# Save the access_token from response
```

### 2. Test Report Management
```bash
# Create Report
curl -X POST "http://localhost:8000/api/v1/reports" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test Report","description":"Test Description"}'

# List Reports
curl -X GET "http://localhost:8000/api/v1/reports" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Get Specific Report
curl -X GET "http://localhost:8000/api/v1/reports/1" \
  -H "Authorization: Bearer YOUR_TOKEN"

# Update Report
curl -X PUT "http://localhost:8000/api/v1/reports/1" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Updated Title","status":"in_progress"}'

# Delete Report
curl -X DELETE "http://localhost:8000/api/v1/reports/1" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

---

## Automated Test Scripts

### Run Backend Tests
```bash
cd backend

# Test Authentication
python test_auth_endpoints.py

# Test Report Management
python test_report_endpoints.py
```

**Expected Output:**
- All tests should pass with ✓ marks
- No ✗ errors

---

## Known Limitations

### What Doesn't Work Yet:

❌ **Template Upload** - File upload service not implemented (Task 5)
- Workaround: Skip template upload, create report without it

❌ **Note Upload** - File upload service not implemented (Task 5)
- Workaround: Can't upload notes yet

❌ **PDF Processing** - Document processing not implemented (Task 7)
- Workaround: Manually create sections

❌ **AI Content Generation** - LLM integration not implemented (Task 14)
- Workaround: Manually write content

❌ **Search** - Vector search not implemented (Task 11-12)
- Workaround: Can't search notes yet

❌ **Export** - PDF/DOCX export not implemented (Task 16)
- Workaround: Can't export yet

---

## Troubleshooting

### Issue: "Failed to create report"
**Solution:** Make sure you're logged in and have a valid token

### Issue: "Template upload error"
**Solution:** This is expected - skip template upload for now

### Issue: "Sections not showing"
**Solution:** Create sections manually using API (see Scenario 3)

### Issue: "Progress not updating"
**Solution:** Make sure to mark sections as complete

### Issue: "401 Unauthorized"
**Solution:** Token expired - logout and login again

---

## Success Criteria

After testing, you should be able to:

✅ Create an account  
✅ Login and logout  
✅ Create a report (without template)  
✅ View report list  
✅ View report details  
✅ Create sections (via API)  
✅ Edit section content  
✅ See progress update automatically  
✅ Update report details  
✅ Delete reports  

---

## Next Steps After Testing

Once you've verified everything works:

1. **Implement File Upload (Task 5)** - Enable template/note uploads
2. **Implement PDF Processing (Task 7)** - Auto-extract sections from template
3. **Implement AI Features (Task 14)** - Content generation
4. **Implement Search (Task 11-12)** - Semantic search
5. **Implement Export (Task 16)** - PDF/DOCX export

---

**Happy Testing!** 🎉
