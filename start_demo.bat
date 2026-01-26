@echo off
echo ========================================
echo Starting Reportify for Demo Video
echo ========================================
echo.

echo [1/3] Starting Backend API...
start "Reportify Backend" cmd /k "cd backend && ..\..\venv\Scripts\activate && uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
timeout /t 5 /nobreak > nul

echo [2/3] Starting Celery Worker...
start "Reportify Celery" cmd /k "cd backend && ..\..\venv\Scripts\activate && celery -A app.worker.celery_app worker --loglevel=info --pool=solo"
timeout /t 3 /nobreak > nul

echo [3/3] Starting Frontend...
start "Reportify Frontend" cmd /k "cd frontend && npm run dev"
timeout /t 3 /nobreak > nul

echo.
echo ========================================
echo Reportify is Starting!
echo ========================================
echo.
echo Services:
echo - Backend API: http://127.0.0.1:8000
echo - API Docs: http://127.0.0.1:8000/docs
echo - Frontend: http://localhost:5173 (or 5174)
echo.
echo Three windows will open:
echo 1. Backend API
echo 2. Celery Worker
echo 3. Frontend Dev Server
echo.
echo Wait 10-15 seconds for all services to start...
echo Then open: http://localhost:5173
echo.
echo Press any key to continue...
pause > nul
