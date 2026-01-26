# Quick Start Guide

## Fastest Way to Test (Windows)

1. **Make sure Docker Desktop is running**

2. **Run the quick setup script:**
   ```bash
   quick_test.bat
   ```

3. **Start the backend server:**
   ```bash
   cd backend
   venv\Scripts\activate
   uvicorn main:app --reload
   ```

4. **In a NEW terminal, run the test:**
   ```bash
   cd backend
   venv\Scripts\activate
   python test_auth.py
   ```

## Manual Steps

### 1. Start Services
```bash
docker-compose up -d
```

### 2. Setup Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

### 3. Initialize
```bash
python scripts/init_services.py
python -m alembic upgrade head
```

### 4. Run Server
```bash
uvicorn main:app --reload
```

### 5. Test
Open http://localhost:8000/docs or run:
```bash
python test_auth.py
```

## What's Working

✅ PostgreSQL, Redis, MinIO, Qdrant (Docker)  
✅ FastAPI Backend  
✅ User Registration  
✅ User Login (JWT)  
✅ Token Refresh  
✅ Protected Endpoints  

## Useful URLs

- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- MinIO Console: http://localhost:9001 (minioadmin/minioadmin)
- Qdrant Dashboard: http://localhost:6333/dashboard

## Need Help?

See [TESTING_GUIDE.md](TESTING_GUIDE.md) for detailed instructions and troubleshooting.
