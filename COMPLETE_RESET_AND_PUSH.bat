@echo off
echo ========================================
echo Complete Git Reset and Clean Push
echo ========================================
echo.

echo This will completely reset git history and create a fresh commit.
echo.
set /p confirm="Are you sure? (y/n): "
if /i not "%confirm%"=="y" (
    echo Cancelled.
    pause
    exit /b 0
)
echo.

REM Step 1: Remove .git folder completely
echo [1/7] Removing git history...
rmdir /s /q .git
echo ✓ Git history removed
echo.

REM Step 2: Initialize fresh git repository
echo [2/7] Initializing fresh git repository...
git init
echo ✓ Git initialized
echo.

REM Step 3: Add remote
echo [3/7] Adding remote...
git remote add origin https://github.com/MuLIAICHI/Reportify.git
echo ✓ Remote added
echo.

REM Step 4: Stage all files
echo [4/7] Staging all files...
git add .
echo ✓ Files staged
echo.

REM Step 5: Check for sensitive files
echo [5/7] Checking for sensitive files...
git status | findstr /C:"backend/.env" >nul
if not errorlevel 1 (
    echo.
    echo ⚠️  WARNING: backend/.env is being committed!
    echo This should NOT happen. Checking .gitignore...
    echo.
    type .gitignore | findstr /C:"backend/.env"
    echo.
    pause
    exit /b 1
)
echo ✓ No sensitive files detected
echo.

REM Step 6: Create fresh commit
echo [6/7] Creating fresh commit...
git commit -m "Initial commit: Reportify - AI-Powered Report Writing Assistant for Kiro Hackathon"
echo ✓ Commit created
echo.

REM Step 7: Push to GitHub
echo [7/7] Pushing to GitHub...
git branch -M main
git push -u origin main --force
if errorlevel 1 (
    echo.
    echo ⚠️  Push failed.
    echo.
    echo This might be because:
    echo 1. Authentication issue
    echo 2. Network issue
    echo 3. Repository doesn't exist
    echo.
    pause
    exit /b 1
)
echo ✓ Pushed successfully!
echo.

echo ========================================
echo ✅ SUCCESS!
echo ========================================
echo.
echo Your code is now on GitHub with clean history!
echo Visit: https://github.com/MuLIAICHI/Reportify
echo.
echo ⚠️  IMPORTANT: Revoke your old API key!
echo https://platform.openai.com/api-keys
echo.
pause
