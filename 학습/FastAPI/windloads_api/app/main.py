# app/main.py
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from .api import api_asce7_10  # asce7-10 라우터 묶음

app = FastAPI(
    title="Shelter Wind Load API (Stateless)",
    version="1.0.0",
    description="ASCE 7 기반 개방형 지붕 구조물 풍하중 계산 API",
)


@app.get("/healthz", response_class=PlainTextResponse, include_in_schema=False)
def healthz():
    return "ok"


@app.get("/meta")
def meta():
    return {
        "name": "Shelter Wind Load API",
        "version": "1.0.0",
        "profiles": ["ASCE7-10"],  # 추후 ["ASCE7-16","ASCE7-22"] 확장
        "units_supported": ["SI"],
    }


# 기준 버전을 경로에서 직접 표현
app.include_router(api_asce7_10, prefix="/asce7-10")
