# Frontend Authentication Testing Guide

## What We've Built

✅ **Task 19.1**: Login and Registration pages with form validation
✅ **Task 19.2**: Authentication state management with Zustand
✅ **Task 19.3**: Protected route wrapper for authenticated pages

## Features Implemented

### Login Page (`/login`)
- Email and password validation
- Error handling and display
- Loading states
- Link to registration page
- Beautiful gradient UI with Tailwind CSS

### Registration Page (`/register`)
- Full name, email, and password fields
- Password confirmation
- **Password strength indicator** with visual feedback:
  - Weak (red) - basic password
  - Fair (yellow) - decent password
  - Good (blue) - strong password
  - Strong (green) - very strong password
- Real-time validation
- Link to login page

### Authentication Store
- Secure token storage (localStorage with persistence)
- Auto-login after registration
- Token refresh mechanism
- Automatic retry on 401 errors
- Logout functionality

### Protected Routes
- Redirects unauthenticated users to login
- Saves attempted location for redirect after login
- Dashboard page for authenticated users

## How to Test

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start the Development Server

```bash
npm run dev
```

The app will be available at: http://localhost:5173

### 3. Test the UI (Without Backend)

Even without the backend running, you can test:

#### ✅ **Visual Testing**
1. Visit http://localhost:5173
2. You'll be redirected to `/login` (not authenticated)
3. Check the login form:
   - Try submitting empty form → see validation errors
   - Enter invalid email → see email validation
   - Enter valid credentials → see loading state

4. Click "create a new account" link
5. Check the registration form:
   - Try submitting empty form → see validation errors
   - Enter a password → **watch the password strength indicator change**
   - Try different passwords to see strength levels:
     - `test` → Weak (red)
     - `test1234` → Fair (yellow)
     - `Test1234` → Good (blue)
     - `Test1234!@#` → Strong (green)
   - Enter mismatched passwords → see confirmation error

#### ✅ **Form Validation Testing**
- **Email validation**: Try `test`, `test@`, `test@test` → all should show errors
- **Password length**: Try passwords < 8 characters → should show error
- **Name validation**: Try empty name or single character → should show error
- **Password match**: Enter different passwords in password and confirm → should show error

### 4. Test with Backend (Once Database Issue is Fixed)

Once the backend is running on `http://localhost:8000`:

#### ✅ **Registration Flow**
1. Go to http://localhost:5173/register
2. Fill in the form:
   - Name: `Test User`
   - Email: `test@example.com`
   - Password: `Test1234!` (watch it turn green!)
   - Confirm Password: `Test1234!`
3. Click "Create account"
4. Should automatically log in and redirect to `/dashboard`
5. Should see welcome message with your name and email

#### ✅ **Login Flow**
1. Logout from dashboard
2. Go to http://localhost:5173/login
3. Enter credentials:
   - Email: `test@example.com`
   - Password: `Test1234!`
4. Click "Sign in"
5. Should redirect to `/dashboard`
6. Should see your user information

#### ✅ **Protected Routes**
1. While logged out, try to visit http://localhost:5173/dashboard
2. Should automatically redirect to `/login`
3. After logging in, should redirect back to `/dashboard`

#### ✅ **Token Refresh**
1. Log in successfully
2. Wait for access token to expire (30 minutes by default)
3. Make any API call
4. Should automatically refresh token and retry the request
5. Should stay logged in

#### ✅ **Logout**
1. Click "Logout" button in dashboard
2. Should redirect to `/login`
3. Should clear all tokens from localStorage
4. Trying to access `/dashboard` should redirect to login

## Testing Checklist

### Visual/UI Testing (No Backend Required)
- [ ] Login page loads correctly
- [ ] Registration page loads correctly
- [ ] Forms have proper validation
- [ ] Error messages display correctly
- [ ] Password strength indicator works
- [ ] Loading states show during form submission
- [ ] Links between login/register work
- [ ] Responsive design works on mobile

### Integration Testing (Backend Required)
- [ ] User can register successfully
- [ ] User can login successfully
- [ ] Invalid credentials show error
- [ ] Duplicate email shows error
- [ ] Protected routes redirect when not authenticated
- [ ] Dashboard shows user information
- [ ] Logout clears session
- [ ] Token refresh works automatically
- [ ] Auto-login after registration works

## Files Created

```
frontend/
├── src/
│   ├── pages/
│   │   ├── Login.tsx           # Login page with validation
│   │   ├── Register.tsx        # Registration with password strength
│   │   └── Dashboard.tsx       # Protected dashboard page
│   ├── stores/
│   │   └── authStore.ts        # Zustand auth state management
│   ├── components/
│   │   └── ProtectedRoute.tsx  # Route protection wrapper
│   └── App.tsx                 # Updated with all routes
├── .env                        # Environment configuration
└── TESTING_GUIDE.md           # This file
```

## API Endpoints Used

The frontend expects these backend endpoints:

- `POST /api/v1/auth/register` - Create new user
- `POST /api/v1/auth/login` - Login user
- `POST /api/v1/auth/logout` - Logout user
- `POST /api/v1/auth/refresh` - Refresh access token
- `GET /api/v1/auth/me` - Get current user info

## Environment Variables

Make sure `.env` file has:

```env
VITE_API_URL=http://localhost:8000/api/v1
```

## Next Steps

Once you can test with the backend:

1. **Test the complete authentication flow**
2. **Verify token storage in browser DevTools** (Application → Local Storage)
3. **Test token refresh** by waiting for expiration
4. **Test error scenarios** (wrong password, network errors, etc.)
5. **Move to Task 20**: Build report management UI

## Troubleshooting

### Frontend won't start
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### CORS errors
- Make sure backend has `http://localhost:5173` in CORS origins
- Check backend `.env` file: `ALLOWED_ORIGINS=http://localhost:5173`

### Tokens not persisting
- Check browser console for errors
- Clear localStorage: DevTools → Application → Local Storage → Clear
- Try logging in again

## Summary

✅ **All authentication UI is complete and ready to test!**

The frontend authentication is fully functional. You can test the UI and form validation right now without the backend. Once the backend database issue is resolved, you'll be able to test the complete authentication flow end-to-end.
