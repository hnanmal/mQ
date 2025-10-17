import numpy as np
from typing import Dict, List, Tuple
from .models import AnalysisInput


def assemble_global(input: AnalysisInput):
    # 노드 id → 인덱스(0..N-1) 매핑
    node_ids = [n.id for n in input.nodes]
    id2idx = {nid: i for i, nid in enumerate(node_ids)}
    N = len(node_ids)

    ndof = 2 * N
    K = np.zeros((ndof, ndof), dtype=float)
    F = np.zeros(ndof, dtype=float)

    # 하중 벡터
    for load in input.loads:
        i = id2idx[load.node]
        F[2 * i + 0] += load.fx
        F[2 * i + 1] += load.fy

    # 요소 강성 조립
    for e in input.elements:
        i1 = id2idx[e.n1]
        i2 = id2idx[e.n2]
        n1 = next(n for n in input.nodes if n.id == e.n1)
        n2 = next(n for n in input.nodes if n.id == e.n2)
        dx = n2.x - n1.x
        dy = n2.y - n1.y
        L = np.hypot(dx, dy)
        if L == 0:
            raise ValueError(f"Element {e.id} has zero length")
        c = dx / L
        s = dy / L
        k = (e.E * e.A) / L
        # 2D truss element stiffness in global coords (4x4)
        ke = k * np.array(
            [
                [c * c, c * s, -c * c, -c * s],
                [c * s, s * s, -c * s, -s * s],
                [-c * c, -c * s, c * c, c * s],
                [-c * s, -s * s, c * s, s * s],
            ]
        )
        dofs = [2 * i1, 2 * i1 + 1, 2 * i2, 2 * i2 + 1]
        for a in range(4):
            for b in range(4):
                K[dofs[a], dofs[b]] += ke[a, b]

    # 구속(고정) 자유도
    fixed = set()
    for sp in input.supports:
        i = id2idx[sp.node]
        if sp.ux:
            fixed.add(2 * i)
        if sp.uy:
            fixed.add(2 * i + 1)
    free = [d for d in range(ndof) if d not in fixed]

    if not free:
        raise ValueError("No free DOFs to solve.")

    # 경계조건 적용 (고정 변위=0 가정)
    Kff = K[np.ix_(free, free)]
    Ff = F[free]

    # 선형 해
    Uf = np.linalg.solve(Kff, Ff)

    # 전체 변위 벡터
    U = np.zeros(ndof)
    U[free] = Uf

    # 반력: R = K*U - F  (고정 DOF에서의 반력만 관심)
    R = K.dot(U) - F

    # 결과 구성
    # - 노드 변위
    disps = []
    for nid in node_ids:
        i = id2idx[nid]
        disps.append({"node": nid, "ux": U[2 * i], "uy": U[2 * i + 1]})

    # - 반력
    reacts = []
    for sp in input.supports:
        i = id2idx[sp.node]
        rx = R[2 * i] if sp.ux else 0.0
        ry = R[2 * i + 1] if sp.uy else 0.0
        reacts.append({"node": sp.node, "rx": rx, "ry": ry})

    # - 요소 축응력 sigma
    elements_out = []
    for e in input.elements:
        i1 = id2idx[e.n1]
        i2 = id2idx[e.n2]
        n1 = next(n for n in input.nodes if n.id == e.n1)
        n2 = next(n for n in input.nodes if n.id == e.n2)
        dx = n2.x - n1.x
        dy = n2.y - n1.y
        L = np.hypot(dx, dy)
        c = dx / L
        s = dy / L
        u1 = np.array([U[2 * i1], U[2 * i1 + 1]])
        u2 = np.array([U[2 * i2], U[2 * i2 + 1]])
        t = np.array([c, s])
        delta = np.dot(u2 - u1, t)  # axial extension
        N = (e.E * e.A / L) * delta  # axial force
        sigma = N / e.A  # axial stress
        elements_out.append({"id": e.id, "n1": e.n1, "n2": e.n2, "sigma": float(sigma)})

    return disps, reacts, elements_out
