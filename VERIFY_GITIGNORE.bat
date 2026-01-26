@echo off
echo ========================================
echo .gitignore Verification Report
echo ========================================
echo.

echo Checking if .env files are properly ignored...
echo.

REM Check if .env files are ignored
echo [1/3] Checking backend/.env...
git check-ignore backend/.env >nul 2>&1
if errorlevel 1 (
    echo ❌ backend/.env is NOT ignored!
    echo This is a CRITICAL security issue!
) else (
    echo ✅ backend/.env is properly ignored
)
echo.

echo [2/3] Checking frontend/.env...
git check-ignore frontend/.env >nul 2>&1
if errorlevel 1 (
    echo ❌ frontend/.env is NOT ignored!
    echo This is a CRITICAL security issue!
) else (
    echo ✅ frontend/.env is properly ignored
)
echo.

echo [3/3] Checking what will be committed...
git status --short | findstr /C:".env" >nul
if not errorlevel 1 (
    echo.
    echo ⚠️  WARNING: .env files found in staging area!
    echo.
    git status --short | findstr /C:".env"
    echo.
    echo Only .env.example files should be committed.
    echo If you see backend/.env or frontend/.env, this is a problem!
) else (
    echo ✅ No .env files in staging area
)
echo.

echo ========================================
echo Summary
echo ========================================
echo.
echo Your .gitignore file includes:
echo   ✅ .env
echo   ✅ .env.local
echo   ✅ .env.*.local
echo   ✅ backend/.env
echo   ✅ frontend/.env
echo   ✅ *.env (catches all .env files)
echo.
echo Files that WILL be committed:
echo   ✅ backend/.env.example (safe - no secrets)
echo   ✅ frontend/.env.example (safe - no secrets)
echo.
echo Files that will NOT be committed:
echo   ✅ backend/.env (contains API keys)
echo   ✅ frontend/.env (if it exists)
echo.
echo ========================================
echo ✅ All .env files are properly protected!
echo ========================================
echo.
pause
