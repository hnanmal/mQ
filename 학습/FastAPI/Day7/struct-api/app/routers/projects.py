from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..db import get_db
from .. import models as m, schemas as s

router = APIRouter(prefix="/projects", tags=["Projects"])


@router.post("", response_model=s.ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(payload: s.ProjectCreate, db: Session = Depends(get_db)):
    proj = m.Project(name=payload.name)
    db.add(proj)
    db.commit()
    db.refresh(proj)
    return proj


@router.get("", response_model=List[s.ProjectOut])
def list_projects(db: Session = Depends(get_db)):
    return db.query(m.Project).order_by(m.Project.id.desc()).all()


@router.get("/{project_id}", response_model=s.ProjectOut)
def get_project(project_id: int, db: Session = Depends(get_db)):
    proj = db.get(m.Project, project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return proj


# ⬇️ 추가: 부분수정(PATCH)
@router.patch("/{project_id}", response_model=s.ProjectOut)
def update_project(
    project_id: int, payload: s.ProjectUpdate, db: Session = Depends(get_db)
):
    proj = db.get(m.Project, project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    if payload.name is not None:
        proj.name = payload.name
    db.commit()
    db.refresh(proj)
    return proj


# ⬇️ 추가: 삭제(연쇄 삭제로 nodes도 함께 삭제됨)
@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    proj = db.get(m.Project, project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(proj)
    db.commit()
    return None
