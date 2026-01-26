@echo off
echo ========================================
echo Push to New Clean Repository
echo ========================================
echo.

echo Repository: https://github.com/MuLIAICHI/Reportify.git
echo.

REM Remove old remote if exists
echo [1/6] Removing old remote...
git remote remove origin 2>nul
echo ✓ Old remote removed
echo.

REM Add new remote
echo [2/6] Adding new remote...
git remote add origin https://github.com/MuLIAICHI/Reportify.git
echo ✓ New remote added
echo.

REM Stage all files
echo [3/6] Staging all files...
git add .
echo ✓ Files staged
echo.

REM Check what's being committed
echo [4/6] Checking for sensitive files...
git status | findstr /C:"backend/.env" >nul
if not errorlevel 1 (
    echo ⚠️  WARNING: .env file detected!
    pause
    exit /b 1
)
echo ✓ No sensitive files detected
echo.

REM Commit
echo [5/6] Creating commit...
git commit -m "Initial commit: Reportify - AI-Powered Report Writing Assistant for Kiro Hackathon"
if errorlevel 1 (
    echo Note: No new changes to commit
)
echo ✓ Commit ready
echo.

REM Push to new repository
echo [6/6] Pushing to GitHub...
git branch -M main
git push -u origin main
if errorlevel 1 (
    echo.
    echo ⚠️  Push failed.
    echo Please check your GitHub credentials.
    pause
    exit /b 1
)
echo ✓ Pushed successfully!
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
echo 2. Check demo video: assets/kiroDemo.mp4
echo 3. Verify no .env files visible
echo 4. Submit to hackathon!
echo.
echo ⚠️  Don't forget to revoke your old API key:
echo https://platform.openai.com/api-keys
echo.
pause
