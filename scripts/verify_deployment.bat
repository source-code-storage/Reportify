@echo off
echo ========================================
echo Report Writing Assistant - Deployment Verification
echo ========================================
echo.

echo [1/7] Checking Docker services...
docker ps --format "table {{.Names}}\t{{.Status}}" | findstr "report-assistant"
if %errorlevel% neq 0 (
    echo ERROR: Docker services not running!
    echo Run: docker-compose up -d
    goto :error
)
echo OK: Docker services running
echo.

echo [2/7] Checking PostgreSQL...
docker exec report-assistant-postgres pg_isready -U postgres > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: PostgreSQL not ready!
    goto :error
)
echo OK: PostgreSQL ready
echo.

echo [3/7] Checking Redis...
docker exec report-assistant-redis redis-cli ping > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Redis not responding!
    goto :error
)
echo OK: Redis responding
echo.

echo [4/7] Checking MinIO...
curl -s http://localhost:9000/minio/health/live > nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: MinIO health check failed (may still work)
) else (
    echo OK: MinIO responding
)
echo.

echo [5/7] Checking Qdrant...
curl -s http://localhost:6333/health > nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Qdrant health check failed (may still work)
) else (
    echo OK: Qdrant responding
)
echo.

echo [6/7] Checking Backend API...
curl -s http://127.0.0.1:8000/health > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Backend API not responding!
    echo Make sure backend is running: uvicorn app.main:app --reload
    goto :error
)
echo OK: Backend API responding
echo.

echo [7/7] Checking Frontend...
curl -s http://localhost:5173 > nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Frontend not responding!
    echo Make sure frontend is running: npm run dev
    goto :error
)
echo OK: Frontend responding
echo.

echo ========================================
echo ALL CHECKS PASSED!
echo ========================================
echo.
echo Your system is ready for deployment!
echo.
echo Next steps:
echo 1. Test complete user workflow
echo 2. Record demo video
echo 3. Update documentation
echo 4. Submit to hackathon
echo.
echo Access points:
echo - Frontend: http://localhost:5173
echo - Backend API: http://127.0.0.1:8000
echo - API Docs: http://127.0.0.1:8000/docs
echo - MinIO Console: http://localhost:9001
echo.
goto :end

:error
echo.
echo ========================================
echo VERIFICATION FAILED!
echo ========================================
echo.
echo Please fix the errors above and try again.
echo See DEPLOYMENT_GUIDE.md for troubleshooting.
echo.
exit /b 1

:end
exit /b 0
