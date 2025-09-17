# app/api/asce7_10/__init__.py
from fastapi import APIRouter
from .windloads_router import router as windloads_router

api_asce7_10 = APIRouter()
api_asce7_10.include_router(windloads_router, prefix="/windloads")
