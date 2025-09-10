# main.py
from fastapi import FastAPI
from fastapi import HTTPException
from typing import Dict
from pydantic import BaseModel

app = FastAPI()

fake_users = ["Alice", "Bob", "Charlie"]
fake_db = ["Alice", "Bob", "Charlie"]


# 요청/응답 스키마 정의
class User(BaseModel):
    id: int
    name: str
    email: str


# 모든 유저 조회 (GET /users)
@app.get("/users")
def list_users():
    return {"users": fake_users}


# # 특정 유저 조회 (GET /users/{id})
# @app.get("/users/{user_id}")
# def get_user(user_id: int):
#     return {"id": user_id, "name": fake_users[user_id]}


@app.get("/users/{user_id}")
def get_user(user_id: int):
    if user_id >= len(fake_db):
        raise HTTPException(status_code=404, detail="User not found")
    return fake_db[user_id]


# # 이름으로 특정 유저 조회 (GET /users/name/{user_name})
# @app.get("/users/name/{user_name}")
# def get_user_by_name(user_name: str):
#     if user_name in fake_users:
#         return {"name": user_name, "id": fake_users.index(user_name)}
#     return {"error": "User not found"}


# # 이름으로 특정 유저 조회 (GET /users/by-name?name=Alice)
# @app.get("/users/by-name")
# def get_user_by_name(name: str):
#     if name in fake_users:
#         return {"name": name, "id": fake_users.index(name)}
#     return {"error": "User not found"}


# @app.post("/users")  # 1) 클라이언트가 POST 요청
# def create_user(user: Dict):  # 2) 요청 본문(Request Body) 받음
#     fake_db.append(user)  # 3) 서비스 로직(DB 저장 대신 리스트에 추가)
#     return {"status": "success", "user": user}  # 4) 응답 반환


@app.post("/users")
def create_user(user: User):
    fake_db.append(user)
    return user
