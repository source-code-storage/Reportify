# Report Writing Assistant - Backend

FastAPI-based backend service for the Report Writing Assistant application.

## Prerequisites

- Python 3.11+
- Docker and Docker Compose
- PostgreSQL 16
- Redis 7
- MinIO (S3-compatible storage)
- Qdrant (Vector database)

## Quick Start

### 1. Start Infrastructure Services

```bash
# From project root
docker-compose up -d
```

This starts:
- PostgreSQL (port 5432)
- Redis (port 6379)
- MinIO (ports 9000, 9001)
- Qdrant (ports 6333, 6334)

### 2. Set Up Python Environment

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
# Update OPENAI_API_KEY if using OpenAI
```

### 4. Initialize Services

```bash
# Initialize S3 bucket and Qdrant collection
python scripts/init_services.py

# Initialize database (create tables)
alembic upgrade head
```

### 5. Run the Application

```bash
# Development mode with auto-reload
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Or using Python
python main.py
```

The API will be available at:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health

### 6. Run Celery Worker (Optional)

In a separate terminal:

```bash
cd backend
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Start Celery worker
celery -A app.worker.celery_app worker --loglevel=info
```

## Project Structure

```
backend/
├── alembic/                 # Database migrations
│   ├── versions/           # Migration files
│   └── env.py             # Alembic configuration
├── app/
│   ├── api/               # API endpoints
│   │   └── v1/           # API version 1
│   │       └── router.py # Main API router
│   ├── core/             # Core configuration
│   │   ├── config.py     # Settings management
│   │   └── database.py   # Database setup
│   ├── worker/           # Celery workers
│   │   ├── celery_app.py # Celery configuration
│   │   └── tasks/        # Async tasks
│   └── __init__.py
├── scripts/              # Utility scripts
│   └── init_services.py # Service initialization
├── .env                  # Environment variables (not in git)
├── .env.example         # Example environment file
├── alembic.ini          # Alembic configuration
├── Dockerfile           # Docker image definition
├── main.py              # Application entry point
└── requirements.txt     # Python dependencies
```

## Development

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run property-based tests
pytest tests/property/ -v
```

### Code Quality

```bash
# Format code
black app/

# Lint code
ruff check app/

# Type checking
mypy app/
```

## API Documentation

Once the server is running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Environment Variables

Key environment variables (see `.env.example` for full list):

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | postgresql://postgres:postgres@localhost:5432/report_assistant |
| REDIS_URL | Redis connection string | redis://localhost:6379/0 |
| S3_ENDPOINT_URL | MinIO/S3 endpoint | http://localhost:9000 |
| OPENAI_API_KEY | OpenAI API key | (required) |
| SECRET_KEY | JWT secret key | (change in production) |

## Troubleshooting

### Database Connection Issues

```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# View PostgreSQL logs
docker logs report-assistant-postgres

# Test connection
psql -h localhost -U postgres -d report_assistant
```

### Redis Connection Issues

```bash
# Check if Redis is running
docker ps | grep redis

# Test connection
redis-cli ping
```

### MinIO/S3 Issues

```bash
# Check if MinIO is running
docker ps | grep minio

# Access MinIO console
# Open http://localhost:9001 in browser
# Login: minioadmin / minioadmin
```

### Celery Worker Issues

```bash
# Check Celery worker status
celery -A app.worker.celery_app inspect active

# Purge all tasks
celery -A app.worker.celery_app purge
```

## Production Deployment

### Using Docker

```bash
# Build image
docker build -t report-assistant-backend .

# Run container
docker run -p 8000:8000 --env-file .env report-assistant-backend
```

### Environment Configuration

For production:
1. Change `SECRET_KEY` to a secure random value
2. Set `DEBUG=False`
3. Configure proper CORS origins
4. Use production-grade database
5. Set up proper logging
6. Configure SSL/TLS certificates

## License

[Your License Here]
