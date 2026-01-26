# 🧪 Testing Guide - Report Writing Assistant

## Quick Start

### Option 1: Automatic Startup (Recommended)

**Double-click:** `START_TESTING.bat`

This will:
1. Start the backend server (http://localhost:8000)
2. Start the frontend server (http://localhost:5173)
3. Open the application in your browser

### Option 2: Manual Startup

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

**Terminal 3 - Run Tests (Optional):**
```bash
cd backend
python test_auth_endpoints.py
python test_report_endpoints.py
```

---

## 🎯 What to Test

### 1. Authentication Flow ✅

**Test Registration:**
1. Go to http://localhost:5173
2. Click "Sign Up" or "Register"
3. Fill in:
   - Email: `test@example.com`
   - Password: `testpassword123`
   - Name: `Test User`
4. Click "Register"
5. ✅ Should redirect to login or dashboard

**Test Login:**
1. Go to login page
2. Enter credentials:
   - Email: `test@example.com`
   - Password: `testpassword123`
3. Click "Login"
4. ✅ Should redirect to dashboard

**Test Protected Routes:**
1. Try accessing dashboard without login
2. ✅ Should redirect to login page

**Test Logout:**
1. Click logout button
2. ✅ Should redirect to login page
3. ✅ Tokens should be cleared

---

### 2. Report Management ✅

**Test Create Report:**
1. Login to dashboard
2. Click "Create New Report" or "+" button
3. Fill in:
   - Title: `My Final Year Report`
   - Description: `Report for my internship`
4. Click "Create"
5. ✅ Should see new report in list
6. ✅ Progress should show 0%

**Test View Report:**
1. Click on a report from the list
2. ✅ Should see report details
3. ✅ Should see sections (if any)
4. ✅ Should see progress indicator

**Test Create Sections:**
1. Open a report
2. Click "Add Section" or similar
3. Add sections:
   - Introduction
   - Methodology
   - Results
   - Conclusion
4. ✅ Sections should appear in order

**Test Edit Section:**
1. Click on a section
2. Add some content in the editor
3. ✅ Word count should update
4. ✅ Auto-save should trigger (check for indicator)

**Test Mark Section Complete:**
1. Check the "Complete" checkbox on a section
2. ✅ Progress percentage should update
3. ✅ Report progress should show 25% (1 of 4 sections)

**Test Update Report:**
1. Edit report title or description
2. Change status (draft → in_progress)
3. ✅ Changes should save

**Test Delete Report:**
1. Click delete button on a report
2. Confirm deletion
3. ✅ Report should disappear from list

---

### 3. API Testing (Backend Only) ✅

**Test Authentication Endpoints:**
```bash
cd backend
python test_auth_endpoints.py
```

**Expected Output:**
- ✅ User registration (201)
- ✅ Login successful (200)
- ✅ Get user info (200)
- ✅ Token refresh (200)
- ✅ Logout (204)
- ✅ Invalid credentials rejected (401)

**Test Report Endpoints:**
```bash
cd backend
python test_report_endpoints.py
```

**Expected Output:**
- ✅ Create report (201)
- ✅ List reports (200)
- ✅ Get report (200)
- ✅ Create sections (201)
- ✅ Update section (200)
- ✅ Progress calculation (25%)
- ✅ Update report (200)
- ✅ Delete report (204)

---

## 🔍 What's Working vs Not Working

### ✅ Working Features

**Backend:**
- ✅ User registration & login
- ✅ JWT authentication
- ✅ Report CRUD operations
- ✅ Section management
- ✅ Progress calculation
- ✅ Word count tracking
- ✅ User authorization

**Frontend:**
- ✅ Login/Register pages
- ✅ Dashboard with report list
- ✅ Report creation modal
- ✅ Report detail page
- ✅ Section editor
- ✅ Progress indicators

### ❌ Not Working Yet

**Backend (Not Implemented):**
- ❌ File uploads (template, notes)
- ❌ PDF processing
- ❌ OCR for images
- ❌ AI content generation
- ❌ Semantic search
- ❌ Export to PDF/DOCX

**Frontend (No Backend):**
- ❌ Template upload
- ❌ Note uploads
- ❌ AI content generation button
- ❌ Search functionality
- ❌ Export functionality

**These features have UI but no backend to connect to yet.**

---

## 🐛 Troubleshooting

### Backend Won't Start

**Error: "Address already in use"**
```bash
# Kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Error: "Module not found"**
```bash
cd backend
pip install -r requirements.txt
```

**Error: "Database locked"**
```bash
# Delete and recreate database
cd backend
del report_assistant.db
python -c "from app.core.database import init_db; init_db()"
```

### Frontend Won't Start

**Error: "Port 5173 already in use"**
```bash
# Kill process on port 5173
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

**Error: "Dependencies not installed"**
```bash
cd frontend
npm install
```

### API Connection Issues

**Error: "Network Error" or "Failed to fetch"**
1. Check backend is running: http://localhost:8000/health
2. Check CORS settings in `backend/app/core/config.py`
3. Verify frontend is using correct API URL

**Error: "401 Unauthorized"**
1. Check if logged in
2. Check if token is valid
3. Try logging out and back in

---

## 📊 Expected Test Results

### Authentication Flow
- Registration: ✅ 201 Created
- Login: ✅ 200 OK with tokens
- Get User: ✅ 200 OK with user data
- Logout: ✅ 204 No Content

### Report Management
- Create Report: ✅ 201 Created
- List Reports: ✅ 200 OK with array
- Get Report: ✅ 200 OK with sections
- Update Report: ✅ 200 OK
- Delete Report: ✅ 204 No Content

### Progress Calculation
- 0 sections: 0% progress
- 1 of 4 complete: 25% progress
- 2 of 4 complete: 50% progress
- 4 of 4 complete: 100% progress

---

## 🎯 Testing Checklist

### Basic Flow
- [ ] Register new user
- [ ] Login with credentials
- [ ] View dashboard
- [ ] Create new report
- [ ] Add sections to report
- [ ] Edit section content
- [ ] Mark section complete
- [ ] Verify progress updates
- [ ] Update report details
- [ ] Delete report
- [ ] Logout

### Edge Cases
- [ ] Try invalid login credentials
- [ ] Try accessing protected routes without login
- [ ] Try accessing another user's report (should fail)
- [ ] Create report with empty title (should fail)
- [ ] Update section with very long content
- [ ] Delete report with sections (should cascade)

### API Tests
- [ ] Run `test_auth_endpoints.py`
- [ ] Run `test_report_endpoints.py`
- [ ] Check API docs at http://localhost:8000/docs

---

## 📚 Useful URLs

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:8000
- **API Documentation:** http://localhost:8000/docs
- **API Alternative Docs:** http://localhost:8000/redoc
- **Health Check:** http://localhost:8000/health

---

## 💡 Tips

1. **Use API Docs:** The Swagger UI at `/docs` lets you test endpoints directly
2. **Check Browser Console:** Look for errors in the browser developer tools
3. **Check Backend Logs:** Terminal running backend shows request logs
4. **Use Test Scripts:** Automated tests are faster than manual testing
5. **Clear Browser Cache:** If seeing old data, clear cache or use incognito

---

## 🎉 Success Criteria

You'll know everything is working when:

✅ You can register and login  
✅ You can create a report  
✅ You can add sections  
✅ Progress updates automatically  
✅ Word count updates when editing  
✅ You can delete reports  
✅ All test scripts pass  

---

**Happy Testing! 🚀**

If you encounter any issues, check the troubleshooting section or the backend logs for error messages.
