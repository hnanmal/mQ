from pydantic import BaseModel, Field
from typing import List

from pydantic import BaseModel, Field
from typing import List, Optional


# ---------- Projects ----------
class ProjectUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=100)


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)


class ProjectOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


# ---------- Nodes ----------
class NodeUpdate(BaseModel):
    x: Optional[float] = None
    y: Optional[float] = None
    z: Optional[float] = None


class NodeCreate(BaseModel):
    x: float
    y: float
    z: float


class NodeBatchCreate(BaseModel):
    nodes: List[NodeCreate]


class NodeOut(BaseModel):
    id: int
    x: float
    y: float
    z: float
    project_id: int

    class Config:
        from_attributes = True


# ---------- Analysis (Job mock) ----------
class AnalysisRunRequest(BaseModel):
    type: str = Field(default="linear_static")  # 예: linear_static
    note: str | None = None


class AnalysisRunStatus(BaseModel):
    job_id: str
    status: str  # queued|running|succeeded|failed
    message: str | None = None
