@echo off
echo ========================================
echo GitHub Repository Setup Script
echo ========================================
echo.

REM Step 1: Remove old remote
echo [1/6] Removing old remote...
git remote remove origin
echo ✓ Old remote removed
echo.

REM Step 2: Add your new remote (REPLACE WITH YOUR REPO URL)
echo [2/6] Adding new remote...
echo IMPORTANT: Edit this file and replace YOUR_USERNAME with your GitHub username!
echo.
set /p username="Enter your GitHub username: "
git remote add origin https://github.com/%username%/reportify.git
echo ✓ New remote added
echo.

REM Step 3: Stage all files
echo [3/6] Staging all files...
git add .
echo ✓ Files staged
echo.

REM Step 4: Commit
echo [4/6] Creating commit...
git commit -m "Initial commit: Reportify - AI-Powered Report Writing Assistant"
echo ✓ Commit created
echo.

REM Step 5: Push to GitHub
echo [5/6] Pushing to GitHub...
git branch -M main
git push -u origin main
echo ✓ Pushed to GitHub
echo.

REM Step 6: Done
echo [6/6] Setup complete!
echo.
echo ========================================
echo ✅ SUCCESS!
echo ========================================
echo.
echo Your repository is now on GitHub!
echo Visit: https://github.com/%username%/reportify
echo.
pause
