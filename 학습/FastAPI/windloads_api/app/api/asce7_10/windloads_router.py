# app/api/asce7_10/windloads.py
from fastapi import APIRouter
from ...schemas import SolveRequest, SolveResponse, BatchIn, BatchOut, ValidateResult
from ...compute import solve

router = APIRouter(tags=["ASCE 7-10 Wind Loads"])


@router.post("/solve", response_model=SolveResponse)
def windloads_solve(req: SolveRequest) -> SolveResponse:
    """
    ASCE 7-10 기준 풍하중 계산 (Stateless).
    """
    return solve(req)


@router.post("/solve:batch", response_model=BatchOut)
def windloads_batch(body: BatchIn) -> BatchOut:
    """
    여러 입력을 한 번에 계산 (Stateless).
    """
    return BatchOut(results=[solve(item) for item in body.items])


@router.post("/validate", response_model=ValidateResult)
def validate_only(req: SolveRequest) -> ValidateResult:
    """
    계산 없이 입력 규칙만 가볍게 점검.
    Pydantic 1차 검증을 통과한 상태에서 도메인 규칙만 추가 확인.
    """
    errs: list[dict] = []

    # 권장 범위 (필요시 조정)
    if not (0.0 <= req.x_deg <= 60.0):
        errs.append({"field": "x_deg", "msg": "권장 범위는 0~60° 입니다."})

    # 토포그래피가 켜진 경우 추가 체크
    if req.topographic.enabled:
        # 이미 gt=0 검증 있음: 여기선 의미적 제약만 예시
        if req.topographic.Lh and req.topographic.H_hill:
            ratio = req.topographic.H_hill / req.topographic.Lh
            if ratio <= 0:
                errs.append(
                    {"field": "topographic.H_hill/Lh", "msg": "양수 비율이어야 합니다."}
                )
        if req.topographic.topho is None or req.topographic.UD is None:
            errs.append(
                {
                    "field": "topographic.topho/UD",
                    "msg": "enabled=true면 topho/UD가 필요합니다.",
                }
            )

    return ValidateResult(valid=(len(errs) == 0), errors=errs)
