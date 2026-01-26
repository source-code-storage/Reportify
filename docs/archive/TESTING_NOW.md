# 🧪 Testing Guide - Both Servers Running!

## ✅ Current Status

Both servers are now running:

- **Frontend**: http://localhost:5173
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 🎯 What to Test

### 1. Frontend UI Testing (Visual)

Open your browser and go to: **http://localhost:5173**

#### Test Login Page
1. You'll be redirected to `/login` (not authenticated yet)
2. **Test validation**:
   - Click "Sign in" with empty fields → See validation errors
   - Enter invalid email like `test` → See email error
   - Enter valid email but no password → See password error

#### Test Registration Page
1. Click "create a new account" link
2. **Test the Password Strength Indicator**:
   - Type `test` → See 🔴 **Weak** (red bar)
   - Type `test1234` → See 🟡 **Fair** (yellow bar)
   - Type `Test1234` → See 🔵 **Good** (blue bar)
   - Type `Test1234!@#` → See 🟢 **Strong** (green bar)
3. **Test validation**:
   - Try empty name → See error
   - Try short name (1 char) → See error
   - Try invalid email → See error
   - Try short password (< 8 chars) → See error
   - Enter different passwords in password/confirm → See mismatch error

### 2. Full Authentication Flow Testing

#### Register a New User
1. Go to http://localhost:5173/register
2. Fill in the form:
   - **Name**: `Test User`
   - **Email**: `test@example.com`
   - **Password**: `Test1234!` (watch it turn green!)
   - **Confirm Password**: `Test1234!`
3. Click "Create account"
4. ✅ **Should automatically log you in**
5. ✅ **Should redirect to `/dashboard`**
6. ✅ **Should see welcome message with your name**

#### Check Dashboard
1. You should see:
   - Welcome message: "Welcome, Test User!"
   - Your email: test@example.com
   - User ID: test-user-id-123
   - Account Status: Active
   - Logout button

#### Test Logout
1. Click the "Logout" button
2. ✅ **Should redirect to `/login`**
3. ✅ **Tokens should be cleared**

#### Test Login
1. On the login page, enter:
   - **Email**: `test@example.com`
   - **Password**: `Test1234!`
2. Click "Sign in"
3. ✅ **Should redirect to `/dashboard`**
4. ✅ **Should see your user information**

#### Test Protected Routes
1. While logged in, note the URL: `/dashboard`
2. Click logout
3. Try to manually visit: http://localhost:5173/dashboard
4. ✅ **Should automatically redirect to `/login`**
5. Log back in
6. ✅ **Should redirect back to `/dashboard`**

### 3. Browser DevTools Testing

#### Check Token Storage
1. Open DevTools (F12)
2. Go to **Application** tab → **Local Storage** → `http://localhost:5173`
3. Look for `auth-storage` key
4. ✅ **Should see stored tokens and user data**

#### Check Network Requests
1. Open DevTools (F12)
2. Go to **Network** tab
3. Register or login
4. ✅ **Should see POST request to `/api/v1/auth/register` or `/login`**
5. ✅ **Should see GET request to `/api/v1/auth/me`**
6. Check the responses - should see mock data

#### Check Console
1. Open DevTools (F12)
2. Go to **Console** tab
3. ✅ **Should have no errors** (warnings are okay)

### 4. API Documentation Testing

Visit: **http://localhost:8000/docs**

You'll see the interactive API documentation (Swagger UI):

1. **Try the `/health` endpoint**:
   - Click on `GET /health`
   - Click "Try it out"
   - Click "Execute"
   - ✅ Should see: `{"status": "healthy"}`

2. **Try the `/api/v1/auth/register` endpoint**:
   - Click on `POST /api/v1/auth/register`
   - Click "Try it out"
   - Enter test data
   - Click "Execute"
   - ✅ Should see mock user response

3. **Try the `/api/v1/auth/login` endpoint**:
   - Click on `POST /api/v1/auth/login`
   - Click "Try it out"
   - Enter any email/password
   - Click "Execute"
   - ✅ Should see mock tokens

## 📋 Testing Checklist

### Visual/UI Tests
- [ ] Login page loads correctly
- [ ] Registration page loads correctly
- [ ] Forms have proper styling
- [ ] Gradient backgrounds look good
- [ ] Buttons have hover effects
- [ ] Links work between pages
- [ ] Responsive on mobile (resize browser)

### Validation Tests
- [ ] Empty form shows errors
- [ ] Invalid email shows error
- [ ] Short password shows error
- [ ] Password mismatch shows error
- [ ] Short name shows error
- [ ] Error messages are clear

### Password Strength Tests
- [ ] Weak password shows red bar
- [ ] Fair password shows yellow bar
- [ ] Good password shows blue bar
- [ ] Strong password shows green bar
- [ ] Strength updates in real-time

### Authentication Flow Tests
- [ ] Can register new user
- [ ] Auto-login after registration works
- [ ] Redirects to dashboard after registration
- [ ] Dashboard shows user info
- [ ] Can logout successfully
- [ ] Can login with credentials
- [ ] Redirects to dashboard after login

### Protected Route Tests
- [ ] Cannot access dashboard when logged out
- [ ] Redirects to login when not authenticated
- [ ] Can access dashboard when logged in
- [ ] Logout clears authentication

### Token Management Tests
- [ ] Tokens stored in localStorage
- [ ] Tokens persist after page refresh
- [ ] Logout clears tokens
- [ ] User data stored correctly

## 🎨 What You Should See

### Login Page
- Beautiful gradient background (blue to indigo)
- White card with shadow
- Email and password fields
- "Sign in" button (indigo)
- Link to registration

### Registration Page
- Same beautiful gradient
- Name, email, password, confirm password fields
- **Password strength indicator** with colored bar
- "Create account" button
- Link to login

### Dashboard
- White navigation bar with app name
- User name displayed
- Logout button
- Welcome message
- Blue info box with user details

## 🐛 Troubleshooting

### Frontend won't load
- Check if process is running: http://localhost:5173
- Check browser console for errors
- Try refreshing the page

### Backend won't respond
- Check if process is running: http://localhost:8000/health
- Check backend console output
- Verify CORS is configured

### Login/Register doesn't work
- Check browser console for errors
- Check Network tab for failed requests
- Verify backend is running on port 8000

### Tokens not persisting
- Check localStorage in DevTools
- Clear localStorage and try again
- Check for console errors

## 🎉 Success Criteria

You've successfully tested everything if:

✅ You can see the beautiful login/register pages  
✅ Form validation works and shows errors  
✅ Password strength indicator changes colors  
✅ You can register a new user  
✅ You're automatically logged in after registration  
✅ Dashboard shows your user information  
✅ You can logout and login again  
✅ Protected routes redirect when not authenticated  
✅ Tokens are stored in localStorage  
✅ No errors in browser console  

## 📝 Notes

- **This is a MOCK backend** - it accepts any credentials
- **No real database** - data is not persisted
- **Perfect for UI testing** - test all frontend features
- **When real backend is ready** - just switch the API URL

## 🚀 Next Steps

After testing:

1. **If everything works**: Move to Task 20 (Report Management UI)
2. **If issues found**: Let me know and I'll help fix them
3. **To use real backend**: Fix the database connection issue

## 💡 Tips

- Use Chrome DevTools for best debugging experience
- Test on different screen sizes (responsive design)
- Try different passwords to see strength indicator
- Check localStorage to see how tokens are stored
- Use the API docs at `/docs` to test endpoints directly

---

**Happy Testing! 🎉**

Both frontend and backend are running and ready to test!
