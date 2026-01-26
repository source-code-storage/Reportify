@echo off
echo ============================================================
echo Starting Report Writing Assistant for Testing
echo ============================================================
echo.

echo [1/2] Starting Backend Server (FastAPI)...
echo Backend will run on: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
start "Backend Server" cmd /k "cd backend && uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo Waiting for backend to start...
timeout /t 5 /nobreak

echo.
echo [2/2] Starting Frontend Server (React + Vite)...
echo Frontend will run on: http://localhost:5173
echo.
start "Frontend Server" cmd /k "cd frontend && npm run dev"

echo.
echo ============================================================
echo Both servers are starting!
echo ============================================================
echo.
echo Backend:  http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo Frontend: http://localhost:5173
echo.
echo Press any key to open the application in your browser...
pause
start http://localhost:5173
