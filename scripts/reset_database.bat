@echo off
echo ========================================
echo DATABASE RESET TOOL
echo ========================================
echo.
echo WARNING: This will delete all reports, sections, and notes!
echo Users will NOT be deleted (you can still login)
echo.
set /p confirm="Are you sure you want to continue? (yes/no): "

if /i "%confirm%"=="yes" (
    echo.
    echo Running reset script...
    python reset_database.py
) else (
    echo.
    echo Reset cancelled. No changes made.
)

echo.
pause
