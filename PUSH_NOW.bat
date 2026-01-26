@echo off
echo ========================================
echo Reportify - GitHub Push Script
echo ========================================
echo.

REM Check if we're in a git repository
git status >nul 2>&1
if errorlevel 1 (
    echo ERROR: Not a git repository!
    echo Please run this script from the project root directory.
    pause
    exit /b 1
)

echo Current repository status:
echo.
git remote -v
echo.

REM Ask for confirmation
set /p confirm="Do you want to push to GitHub? (y/n): "
if /i not "%confirm%"=="y" (
    echo Push cancelled.
    pause
    exit /b 0
)

echo.
echo [1/5] Checking for sensitive files...
git status | findstr /C:"backend/.env" >nul
if not errorlevel 1 (
    echo.
    echo ⚠️  WARNING: .env file detected in git status!
    echo This file contains sensitive information and should NOT be committed.
    echo.
    echo Please run: git reset
    echo Then check your .gitignore file.
    pause
    exit /b 1
)
echo ✓ No sensitive files detected
echo.

echo [1.5/5] Checking demo video...
if exist "assets\kiroDemo.mp4" (
    echo ✓ Demo video found: assets\kiroDemo.mp4
    for %%A in ("assets\kiroDemo.mp4") do set size=%%~zA
    echo   File size: %size% bytes
    if %size% GTR 104857600 (
        echo.
        echo ⚠️  WARNING: Video file is larger than 100MB!
        echo GitHub has a 100MB file size limit.
        echo Consider uploading to YouTube instead and linking in README.
        echo.
        set /p continue="Continue anyway? (y/n): "
        if /i not "!continue!"=="y" (
            echo Push cancelled.
            pause
            exit /b 0
        )
    )
) else (
    echo ⚠️  Demo video not found at assets\kiroDemo.mp4
    echo This is okay if you're linking to YouTube instead.
)
echo.

echo [2/5] Staging all files...
git add .
if errorlevel 1 (
    echo ERROR: Failed to stage files
    pause
    exit /b 1
)
echo ✓ Files staged
echo.

echo [3/5] Creating commit...
git commit -m "Initial commit: Reportify - AI-Powered Report Writing Assistant for Kiro Hackathon"
if errorlevel 1 (
    echo ERROR: Failed to create commit
    echo This might be because there are no changes to commit.
    pause
    exit /b 1
)
echo ✓ Commit created
echo.

echo [4/5] Pushing to GitHub...
git push
if errorlevel 1 (
    echo.
    echo ⚠️  Push failed. This might be because:
    echo   1. You need to set up the remote first
    echo   2. You need to authenticate
    echo   3. The branch doesn't exist on remote
    echo.
    echo Trying to push with upstream...
    git push -u origin main
    if errorlevel 1 (
        git push -u origin master
        if errorlevel 1 (
            echo.
            echo ERROR: Failed to push to GitHub
            echo Please check your remote configuration and authentication.
            pause
            exit /b 1
        )
    )
)
echo ✓ Pushed to GitHub
echo.

echo [5/5] Verifying...
git log --oneline -1
echo.

echo ========================================
echo ✅ SUCCESS!
echo ========================================
echo.
echo Your code is now on GitHub!
echo.
echo Next steps:
echo 1. Visit your repository on GitHub
echo 2. Verify all files are there
echo 3. Check that .env files are NOT visible
echo 4. Update README with your YouTube video URL
echo.
pause
