@echo off
echo ========================================
echo Report Writing Assistant - Quick Test
echo ========================================
echo.

echo Step 1: Starting Docker services...
docker-compose up -d
if errorlevel 1 (
    echo ERROR: Failed to start Docker services
    echo Make sure Docker Desktop is running
    pause
    exit /b 1
)

echo.
echo Waiting for services to be ready...
timeout /t 10 /nobreak

echo.
echo Step 2: Setting up backend...
cd backend

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate

echo Installing dependencies...
pip install -r requirements.txt -q

if not exist .env (
    echo Creating .env file...
    copy .env.example .env
)

echo.
echo Step 3: Initializing services...
python scripts\init_services.py

echo.
echo Step 4: Running database migrations...
python -m alembic upgrade head

echo.
echo ========================================
echo Setup complete! 
echo ========================================
echo.
echo To start the server, run:
echo   cd backend
echo   venv\Scripts\activate
echo   uvicorn main:app --reload
echo.
echo Then in another terminal, run:
echo   cd backend
echo   venv\Scripts\activate
echo   python test_auth.py
echo.
echo Or open http://localhost:8000/docs in your browser
echo.
pause
