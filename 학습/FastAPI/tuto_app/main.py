# main.py
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Depends
from typing import Dict
from pydantic import BaseModel

app = FastAPI()

fake_users = ["Alice", "Bob", "Charlie"]
fake_db = ["Alice", "Bob", "Charlie"]


# 요청/응답 스키마 정의
class UserIn(BaseModel):
    name: str
    email: str
    password: str


class UserOut(BaseModel):
    name: str
    email: str


@app.post("/users", response_model=UserOut)
def create_user(user: UserIn):
    # password는 저장되지만 클라이언트엔 반환 안 함
    return user


# 모든 유저 조회 (GET /users)
@app.get("/users")
def list_users():
    return {"users": fake_users}


def get_token_header(x_token: str):
    if x_token != "mysecret":
        raise HTTPException(status_code=400, detail="Invalid Token")


@app.get("/secure-data")
def read_secure_data(token: str = Depends(get_token_header)):
    return {"message": "You are authorized"}


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


# @app.post("/users")
# def create_user(user: UserIn):
#     fake_db.append(user)
#     return user
