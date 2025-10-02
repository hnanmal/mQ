from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db import engine, Base
from .routers import projects, nodes, analysis

# 테이블 생성 (Alembic 미사용 시 간편 초기화)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Structural Analysis API (E2E Practice)",
    version="0.1.0",
)

# CORS 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(projects.router)
app.include_router(nodes.router)
app.include_router(analysis.router)


@app.get("/")
def read_root():
    return {"message": "OK", "docs": "/docs"}
