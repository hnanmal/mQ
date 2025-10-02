from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.responses import JSONResponse
from .models import AnalysisInput, RunResponse, StatusResponse
from .jobs import store, run_job
from .config import add_cors

app = FastAPI(
    title="Structural Analysis API",
    openapi_url="/api/openapi.json",
    docs_url="/api/docs",
)

# CORS (개발 시 편의용)
add_cors(app)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/analysis/run", response_model=RunResponse, status_code=202)
async def analysis_run(payload: AnalysisInput, bg: BackgroundTasks):
    # Job 생성
    job_id = await store.create(payload)
    # 백그라운드 실행
    bg.add_task(run_job, job_id, payload)
    return RunResponse(job_id=job_id)


@app.get("/api/analysis/status/{job_id}", response_model=StatusResponse)
async def analysis_status(job_id: str):
    status = await store.get_status(job_id)
    if not status:
        raise HTTPException(status_code=404, detail="Job not found")
    return StatusResponse(**status)


@app.get("/api/analysis/result/{job_id}")
async def analysis_result(job_id: str):
    job = await store.get_result(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job["status"] != "done":
        # 아직 완료 전: 409로 알려줌 (프론트는 폴링 계속)
        raise HTTPException(
            status_code=409, detail=f"Not ready. Current status={job['status']}"
        )
    out = {"job_id": job_id, **job["result"]}
    return JSONResponse(content=out)
