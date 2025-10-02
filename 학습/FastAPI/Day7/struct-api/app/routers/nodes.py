from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..db import get_db
from .. import models as m, schemas as s

router = APIRouter(prefix="/projects", tags=["Nodes"])


@router.post(
    "/{project_id}/nodes",
    response_model=List[s.NodeOut],
    status_code=status.HTTP_201_CREATED,
)
def add_nodes(
    project_id: int, payload: s.NodeBatchCreate, db: Session = Depends(get_db)
):
    proj = db.get(m.Project, project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    nodes = []
    for n in payload.nodes:
        node = m.Node(x=n.x, y=n.y, z=n.z, project_id=project_id)
        db.add(node)
        nodes.append(node)
    db.commit()
    for node in nodes:
        db.refresh(node)
    return nodes


@router.get("/{project_id}/nodes", response_model=List[s.NodeOut])
def list_nodes(project_id: int, db: Session = Depends(get_db)):
    proj = db.get(m.Project, project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return (
        db.query(m.Node)
        .filter(m.Node.project_id == project_id)
        .order_by(m.Node.id)
        .all()
    )


@router.get("/{project_id}/{node_id}", response_model=s.NodeOut)
def get_node(project_id: int, node_id: int, db: Session = Depends(get_db)):
    # 프로젝트 존재 여부 확인
    project = db.get(m.Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # 노드 존재 여부 및 프로젝트 소속 여부 확인
    node = db.get(m.Node, node_id)
    if not node or node.project_id != project_id:
        raise HTTPException(status_code=404, detail="Node not found in this project")

    return node


@router.patch("/{project_id}/{node_id}", response_model=s.NodeOut)
def update_node(
    project_id: int, node_id: int, payload: s.NodeUpdate, db: Session = Depends(get_db)
):
    # 프로젝트 존재 여부 확인
    project = db.get(m.Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # 노드 존재 여부 및 프로젝트 소속 여부 확인
    node = db.get(m.Node, node_id)
    if not node or node.project_id != project_id:
        raise HTTPException(status_code=404, detail="Node not found in this project")

    # 업데이트
    if payload.x is not None:
        node.x = payload.x
    if payload.y is not None:
        node.y = payload.y
    if payload.z is not None:
        node.z = payload.z
    db.commit()
    db.refresh(node)
    return node


@router.delete("/{project_id}/{node_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_node(project_id: int, node_id: int, db: Session = Depends(get_db)):
    # 프로젝트 존재 여부 확인
    project = db.get(m.Project, project_id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    # 노드 존재 여부 및 프로젝트 소속 여부 확인
    node = db.get(m.Node, node_id)
    if not node or node.project_id != project_id:
        raise HTTPException(status_code=404, detail="Node not found in this project")

    db.delete(node)
    db.commit()
    return None
