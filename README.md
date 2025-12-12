Backend:
set PYTHONPATH=%CD%
uvicorn backend.app:app --reload --host 127.0.0.1 --port 8000


Frontend:
cd frontend/next-app
npm run dev


