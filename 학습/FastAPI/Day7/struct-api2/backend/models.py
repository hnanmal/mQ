from pydantic import BaseModel, Field
from typing import List, Optional, Literal, Dict


# ====== 요청 ======


class Node(BaseModel):
    id: int
    x: float
    y: float


class Element(BaseModel):
    id: int
    n1: int
    n2: int
    E: float  # Young's modulus
    A: float  # Cross-sectional area


class Support(BaseModel):
    node: int
    ux: bool = False  # fix x?
    uy: bool = False  # fix y?


class Load(BaseModel):
    node: int
    fx: float = 0.0
    fy: float = 0.0


class Options(BaseModel):
    solver: Literal["linear"] = "linear"
    unit: str = "SI"


class AnalysisInput(BaseModel):
    nodes: List[Node]
    elements: List[Element]
    supports: List[Support] = Field(default_factory=list)
    loads: List[Load] = Field(default_factory=list)
    options: Options = Options()


# ====== 상태/결과 ======


class RunResponse(BaseModel):
    job_id: str


# class StatusResponse(BaseModel):
#     job_id: str
#     status: Literal["pending", "running", "done", "failed"]
#     progress: float = 0.0


class Displacement(BaseModel):
    node: int
    ux: float
    uy: float


class Reaction(BaseModel):
    node: int
    rx: float
    ry: float


class ResultResponse(BaseModel):
    job_id: str
    meta: Dict[str, float | str]
    nodes: List[Node]
    elements: List[Dict]  # include sigma per element
    displacements: List[Displacement]
    reactions: List[Reaction]


class StatusResponse(BaseModel):
    job_id: str
    status: Literal["pending", "running", "done", "failed"]
    progress: float = 0.0
    error: Optional[str] = None
