@echo off
echo Starting Report Writing Assistant Services...
echo.

echo Starting Docker services (PostgreSQL, Redis, MinIO, Qdrant)...
docker-compose up -d

echo.
echo Waiting for services to be ready...
timeout /t 10 /nobreak

echo.
echo Services started successfully!
echo.
echo PostgreSQL: localhost:5432
echo Redis: localhost:6379
echo MinIO: localhost:9000 (Console: localhost:9001)
echo Qdrant: localhost:6333
echo.
echo Press any key to continue...
pause
