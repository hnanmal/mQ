# app/schemas.py
from typing import Literal, Optional, Annotated, List
from pydantic import BaseModel, Field, model_validator

# --- 리터럴 타입 ---
Exposure = Literal["Exposure B", "Exposure C", "Exposure D"]
BldgType = Literal["OM", "OP"]
Blockage = Literal["C", "O"]
Structural = Literal["Steel", "Concrete", "Other"]
TopoType = Literal["2Dridges", "2Descarpments", "3Daxisymmetric"]
UDType = Literal["Up", "Down"]


# --- 토포그래피 입력 ---
class TopographicInput(BaseModel):
    enabled: bool = Field(False, description="지형 영향 고려 여부")
    BldgH: Optional[Annotated[float, Field(gt=0)]] = None
    Lh: Optional[Annotated[float, Field(gt=0)]] = None
    H_hill: Optional[Annotated[float, Field(gt=0)]] = None
    x: Optional[float] = None
    topho: Optional[TopoType] = None
    UD: Optional[UDType] = None

    @model_validator(mode="after")
    def check_fields(self):
        if self.enabled:
            missing = [
                k for k, v in self.model_dump().items() if k != "enabled" and v is None
            ]
            if missing:
                raise ValueError(
                    f"Topographic enabled=true 이면 다음 필드가 필요합니다: {missing}"
                )
        return self


# --- 요청 ---
class SolveRequest(BaseModel):
    exp: Exposure = "Exposure C"
    h: Annotated[float, Field(gt=0)] = 14
    B: Annotated[float, Field(gt=0)] = 15
    L: Annotated[float, Field(gt=0)] = 20
    beta: Annotated[float, Field(gt=0)] = 0.02
    Type: BldgType = "OM"
    blockage: Blockage = "C"
    x_deg: float = 37.0
    Kd: Annotated[float, Field(gt=0)] = 0.85
    V: Annotated[float, Field(gt=0)] = 58.0
    structural_type: Structural = "Steel"
    purlin_s: Annotated[float, Field(gt=0)] = 1.2
    purlin_l: Annotated[float, Field(gt=0)] = 6.0
    topographic: TopographicInput = TopographicInput()


# --- 응답 ---
class BasisOut(BaseModel):
    EffecWindArea: float
    zone_a: float
    EWA: Literal["EWA1", "EWA2", "EWA3"]
    na: float
    G: float
    Kz: float
    Kzt: float


class MainOut(BaseModel):
    CNW: list[float]
    CNL: list[float]
    CNgamma90: list[float]
    PW_Main: list[float]
    PL_Main: list[float]
    Pgamma90_Main: list[float]


class CCZoneOut(BaseModel):
    zone: int
    CNcc_A: float
    CNcc_B: float
    Pcc_A_Pa: float
    Pcc_B_Pa: float


class SolveResponse(BaseModel):
    basis: BasisOut
    main: MainOut
    cc: list[CCZoneOut]


# --- 배치 요청/응답 ---
class BatchIn(BaseModel):
    items: List[SolveRequest]


class BatchOut(BaseModel):
    results: List[SolveResponse]


# --- 검증 전용 응답 ---
class ValidateResult(BaseModel):
    valid: bool
    errors: list[dict]
