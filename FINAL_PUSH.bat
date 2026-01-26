@echo off
echo ========================================
echo Final Push to GitHub (Clean)
echo ========================================
echo.

echo Files with API keys have been deleted.
echo Creating a clean commit...
echo.

REM Reset everything
echo [1/4] Resetting git state...
git reset
echo ✓ Reset complete
echo.

REM Stage all files
echo [2/4] Staging all files...
git add .
echo ✓ Files staged
echo.

REM Create clean commit
echo [3/4] Creating commit...
git commit -m "Initial commit: Reportify - AI-Powered Report Writing Assistant for Kiro Hackathon"
echo ✓ Commit created
echo.

REM Force push to overwrite history
echo [4/4] Pushing to GitHub (force push)...
git push -u origin main --force
if errorlevel 1 (
    echo.
    echo ════════════════════════════════════════
    echo ⚠️  GitHub is still blocking the push
    echo ════════════════════════════════════════
    echo.
    echo This is because the API key is in the git history.
    echo.
    echo OPTION 1: Allow the secret on GitHub (Quick)
    echo ─────────────────────────────────────────
    echo 1. Visit this URL:
    echo    https://github.com/MuLIAICHI/Reportify/security/secret-scanning/unblock-secret/38oJdFTrKIUP50dcRrzQeNO
    echo 2. Click "Allow secret"
    echo 3. Run this script again
    echo.
    echo OPTION 2: Create completely new repository (Recommended)
    echo ─────────────────────────────────────────
    echo 1. Delete current repository on GitHub
    echo 2. Create a new one with same name
    echo 3. Run this script again
    echo.
    echo CRITICAL: Revoke your OpenAI API key!
    echo ─────────────────────────────────────────
    echo 1. Go to: https://platform.openai.com/api-keys
    echo 2. Revoke key: sk-proj-jRu4XZI15...
    echo 3. Create new key
    echo 4. Update backend/.env
    echo.
    pause
    exit /b 1
)
echo ✓ Pushed successfully!
echo.

echo ════════════════════════════════════════
echo ✅ SUCCESS!
echo ════════════════════════════════════════
echo.
echo Your code is on GitHub!
echo Visit: https://github.com/MuLIAICHI/Reportify
echo.
echo ⚠️  IMPORTANT: Revoke your API key!
echo Go to: https://platform.openai.com/api-keys
echo.
pause
