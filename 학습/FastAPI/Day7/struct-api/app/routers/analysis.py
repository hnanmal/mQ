# app/routers/analysis.py
import asyncio
import uuid
from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException, status
from sqlalchemy.orm import Session

from ..db import get_db
from .. import models as m, schemas as s

router = APIRouter(prefix="/analysis", tags=["Analysis"])

# --- 간단한 인메모리 Job 저장소 (데모용) ---
JOB_STORE: dict[str, s.AnalysisRunStatus] = {}


async def _simulate_solver(job_id: str, project_id: int, req: s.AnalysisRunRequest):
    """
    실제 솔버 대신 상태 전이만 모킹합니다.
    여기서 필요한 경우: DB 조회(노드 수), 간단 계산, 로그 적재 등을 흉내낼 수 있음.
    """
    try:
        # 1) running
        JOB_STORE[job_id].status = "running"
        # 계산 중… (진짜 환경에선 외부 솔버 호출/큐/컨테이너 작업 등)
        await asyncio.sleep(1.0)

        # 2) 성공 처리 (간단한 결과 메시지 부여)
        msg = f"{req.type} analysis finished for project {project_id}"
        JOB_STORE[job_id].status = "succeeded"
        JOB_STORE[job_id].message = msg
    except Exception as e:
        JOB_STORE[job_id].status = "failed"
        JOB_STORE[job_id].message = f"error: {e}"


@router.post(
    "/projects/{project_id}/runs",
    response_model=s.AnalysisRunStatus,
    status_code=status.HTTP_202_ACCEPTED,
)
def request_run(
    project_id: int,
    payload: s.AnalysisRunRequest,
    bg: BackgroundTasks,
    db: Session = Depends(get_db),
):
    # 0) 프로젝트 존재 여부 확인
    proj = db.get(m.Project, project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")

    # (선택) 사전 검증: 노드 유무, 동결 여부, 메시 존재 등
    # count = db.query(m.Node).filter(m.Node.project_id == project_id).count()
    # if count == 0:
    #     raise HTTPException(status_code=422, detail="No nodes in project")

    # 1) Job 생성
    job_id = str(uuid.uuid4())
    JOB_STORE[job_id] = s.AnalysisRunStatus(
        job_id=job_id, status="queued", message=None
    )

    # 2) 백그라운드 실행
    bg.add_task(_simulate_solver, job_id, project_id, payload)

    return JOB_STORE[job_id]


@router.get("/runs/{job_id}", response_model=s.AnalysisRunStatus)
def get_run(job_id: str):
    job = JOB_STORE.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job


# (선택) 취소 API
@router.post("/runs/{job_id}:cancel", response_model=s.AnalysisRunStatus)
def cancel_run(job_id: str):
    job = JOB_STORE.get(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    if job.status in {"succeeded", "failed"}:
        return job  # 이미 종료
    # 데모: 실제 취소는 실행 컨텍스트 제어가 필요. 여기선 상태만 바꿔줌.
    job.status = "failed"
    job.message = "canceled by user"
    return job
