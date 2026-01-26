@echo off
echo ========================================
echo Fix API Keys and Push to GitHub
echo ========================================
echo.

echo CRITICAL: Removing files with exposed API keys...
echo.

REM Remove the problematic files
echo [1/7] Removing files with API keys...
git rm --cached docs/archive/FRONTEND_CONNECTED.md
git rm --cached docs/archive/START_REAL_BACKEND.md
del docs\archive\FRONTEND_CONNECTED.md
del docs\archive\START_REAL_BACKEND.md
echo ✓ Files removed
echo.

REM Add to gitignore to prevent future issues
echo [2/7] Updating .gitignore...
echo. >> .gitignore
echo # Archive files with sensitive data >> .gitignore
echo docs/archive/FRONTEND_CONNECTED.md >> .gitignore
echo docs/archive/START_REAL_BACKEND.md >> .gitignore
echo ✓ .gitignore updated
echo.

REM Stage changes
echo [3/7] Staging changes...
git add .gitignore
echo ✓ Changes staged
echo.

REM Commit the removal
echo [4/7] Committing changes...
git commit -m "Remove files with exposed API keys"
echo ✓ Committed
echo.

REM Reset to clean state
echo [5/7] Preparing clean push...
git reset --soft HEAD~2
echo ✓ Reset complete
echo.

REM Stage all files again
echo [6/7] Staging all files...
git add .
git commit -m "Initial commit: Reportify - AI-Powered Report Writing Assistant"
echo ✓ New commit created
echo.

REM Push to GitHub
echo [7/7] Pushing to GitHub...
git push -u origin main --force
if errorlevel 1 (
    echo.
    echo ⚠️  Push still failed.
    echo.
    echo IMPORTANT: Your OpenAI API key was exposed in git history.
    echo You MUST revoke this key and create a new one:
    echo.
    echo 1. Go to: https://platform.openai.com/api-keys
    echo 2. Revoke the old key
    echo 3. Create a new key
    echo 4. Update backend/.env with new key
    echo.
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
echo ⚠️  IMPORTANT SECURITY NOTICE:
echo Your OpenAI API key was exposed in the git history.
echo Please revoke it and create a new one:
echo.
echo 1. Go to: https://platform.openai.com/api-keys
echo 2. Revoke the exposed key
echo 3. Create a new API key
echo 4. Update backend/.env with the new key
echo.
pause
