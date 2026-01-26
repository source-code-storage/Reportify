@echo off
echo ========================================
echo Push to New GitHub Repository
echo ========================================
echo.

echo Your new repository: https://github.com/MuLIAICHI/Reportify.git
echo.

REM Remove old remote
echo [1/6] Removing old remote...
git remote remove origin
echo ✓ Old remote removed
echo.

REM Add new remote
echo [2/6] Adding new remote...
git remote add origin https://github.com/MuLIAICHI/Reportify.git
echo ✓ New remote added
echo.

REM Check for sensitive files
echo [3/6] Checking for sensitive files...
git status | findstr /C:"backend/.env" >nul
if not errorlevel 1 (
    echo.
    echo ⚠️  WARNING: .env file detected!
    echo Please run: git reset
    pause
    exit /b 1
)
echo ✓ No sensitive files detected
echo.

REM Stage all files
echo [4/6] Staging all files...
git add .
echo ✓ Files staged
echo.

REM Commit
echo [5/6] Creating commit...
git commit -m "Initial commit: Reportify - AI-Powered Report Writing Assistant for Kiro Hackathon"
if errorlevel 1 (
    echo Note: No changes to commit or already committed
)
echo ✓ Commit ready
echo.

REM Push to new repository
echo [6/6] Pushing to GitHub...
git branch -M main
git push -u origin main
if errorlevel 1 (
    echo.
    echo ⚠️  Push failed. You may need to authenticate.
    echo Please check your GitHub credentials.
    pause
    exit /b 1
)
echo ✓ Pushed to GitHub
echo.

echo ========================================
echo ✅ SUCCESS!
echo ========================================
echo.
echo Your code is now on GitHub!
echo Visit: https://github.com/MuLIAICHI/Reportify
echo.
echo Next steps:
echo 1. Visit your repository
echo 2. Verify all files are there
echo 3. Check that .env files are NOT visible
echo 4. Watch your demo video in assets/kiroDemo.mp4
echo.
pause
