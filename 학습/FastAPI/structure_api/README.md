# Structural Analysis API (FastAPI)

React(+Vite) 클라이언트와 연동되는 구조해석 데모 백엔드.

## API

- POST `/api/analysis/run` → { "job_id": "xxxx" }
- GET  `/api/analysis/status/{job_id}` → { "job_id", "status", "progress" }
- GET  `/api/analysis/result/{job_id}` → { "job_id", "meta", "nodes", "elements", "displacements", "reactions" }

요청 JSON 스키마: nodes/elements/supports/loads/options (2D 트러스)

## 실행


pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8000