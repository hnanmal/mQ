import asyncio
import time
import uuid
from typing import Dict, Any

import logging

logger = logging.getLogger(__name__)


from .models import AnalysisInput
from .solver import assemble_global


class JobStore:
    def __init__(self):
        self._jobs: Dict[str, Dict[str, Any]] = {}
        self._lock = asyncio.Lock()

    async def create(self, payload: AnalysisInput) -> str:
        job_id = uuid.uuid4().hex[:8]
        async with self._lock:
            self._jobs[job_id] = {
                "status": "pending",
                "progress": 0.0,
                "payload": payload,
                "result": None,
                "error": None,
                "started_at": None,
                "finished_at": None,
            }
        return job_id

    async def set_status(self, job_id: str, status: str, progress: float | None = None):
        async with self._lock:
            job = self._jobs[job_id]
            job["status"] = status
            if progress is not None:
                job["progress"] = progress

    async def set_result(self, job_id: str, result: dict):
        async with self._lock:
            job = self._jobs[job_id]
            job["result"] = result

    async def set_error(self, job_id: str, message: str):
        async with self._lock:
            job = self._jobs[job_id]
            job["error"] = message

    async def mark_started(self, job_id: str):
        async with self._lock:
            self._jobs[job_id]["started_at"] = time.time()

    async def mark_finished(self, job_id: str):
        async with self._lock:
            self._jobs[job_id]["finished_at"] = time.time()

    async def get_status(self, job_id: str):
        async with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return None
            return {
                "job_id": job_id,
                "status": job["status"],
                "progress": job["progress"],
            }

    async def get_result(self, job_id: str):
        async with self._lock:
            job = self._jobs.get(job_id)
            if not job:
                return None
            return job


store = JobStore()


async def run_job(job_id: str, payload: AnalysisInput):
    try:
        await store.mark_started(job_id)
        await store.set_status(job_id, "running", 0.05)
        await asyncio.sleep(0.2)  # 초기화

        t0 = time.time()
        # 중간 진행률 업데이트 (실제 계산 단계에 맞춰 조정 가능)
        await store.set_status(job_id, "running", 0.3)
        await asyncio.sleep(0.1)

        disps, reacts, elems = assemble_global(payload)
        await store.set_status(job_id, "running", 0.8)
        await asyncio.sleep(0.1)

        runtime = time.time() - t0
        result = {
            "meta": {
                "solver": payload.options.solver,
                "runtime_sec": round(runtime, 4),
            },
            "nodes": [n.model_dump() for n in payload.nodes],
            "elements": elems,
            "displacements": disps,
            "reactions": reacts,
        }

        await store.set_result(job_id, result)
        await store.set_status(job_id, "done", 1.0)
        await store.mark_finished(job_id)
    except Exception as e:
        logger.exception(f"[{job_id}] analysis failed: {e}")
        await store.set_error(job_id, str(e))
        await store.set_status(job_id, "failed", 1.0)
        await store.mark_finished(job_id)
