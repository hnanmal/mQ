from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..db import get_db
from .. import models as m, schemas as s

router = APIRouter(prefix="/nodes", tags=["Nodes:Detail"])


@router.get("/{node_id}", response_model=s.NodeOut)
def get_node(node_id: int, db: Session = Depends(get_db)):
    node = db.get(m.Node, node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    return node


@router.patch("/{node_id}", response_model=s.NodeOut)
def update_node(node_id: int, payload: s.NodeUpdate, db: Session = Depends(get_db)):
    node = db.get(m.Node, node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    if payload.x is not None:
        node.x = payload.x
    if payload.y is not None:
        node.y = payload.y
    if payload.z is not None:
        node.z = payload.z
    db.commit()
    db.refresh(node)
    return node


@router.delete("/{node_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_node(node_id: int, db: Session = Depends(get_db)):
    node = db.get(m.Node, node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    db.delete(node)
    db.commit()
    return None
