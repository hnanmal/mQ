from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional, List
from fastapi import HTTPException, status
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Todo API (Fake DB)")


# Vite dev 서버의 두 출처를 모두 허용 (필요 시 하나만 남겨도 됨)
origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,        # 또는 ["*"] (사내 개발용은 편하지만, 공개 서비스는 지양)
    allow_credentials=True,
    allow_methods=["*"],          # GET, POST, PUT, PATCH, DELETE, OPTIONS 전부
    allow_headers=["*"],          # "Content-Type: application/json" 등 커스텀 헤더 허용
)

@app.get("/")
def root():    
    return {"message": "OK", "docs": "/docs"}

# --- Fake DB ---
todos: list[dict] = [] # {id, title, done}
next_id: int = 1

# --- Schemas ---
class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    done: bool = False

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    done: Optional[bool] = None

class TodoOut(BaseModel):
    id: int
    title: str
    done: bool


# 유틸

def _find_index(todo_id: int) -> int:
    for i, t in enumerate(todos):
        if t["id"] == todo_id:
            return i
    return -1

# 1) 목록 조회 GET /todos
@app.get("/todos", response_model=List[TodoOut])
def list_todos():
    return todos

# 2) 생성 POST /todos
@app.post("/todos", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate):
    global next_id
    todo = {"id": next_id, "title": payload.title, "done": payload.done}
    todos.append(todo)
    next_id += 1
    return todo

# 3) 전체 수정 PUT /todos/{id} (idempotent 느낌)
@app.put("/todos/{todo_id}", response_model=TodoOut)
def put_todo(todo_id: int, payload: TodoCreate):
    idx = _find_index(todo_id)
    if idx == -1:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos[idx] = {"id": todo_id, "title": payload.title, "done": payload.done}
    return todos[idx]

# 4) 부분 수정 PATCH /todos/{id} (선택)
@app.patch("/todos/{todo_id}", response_model=TodoOut)
def patch_todo(todo_id: int, payload: TodoUpdate):
    idx = _find_index(todo_id)
    if idx == -1:
        raise HTTPException(status_code=404, detail="Todo not found")
    if payload.title is not None:
        todos[idx]["title"] = payload.title
    if payload.done is not None:
        todos[idx]["done"] = payload.done
    return todos[idx]

# 5) 삭제 DELETE /todos/{id}
@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    idx = _find_index(todo_id)
    if idx == -1:
        raise HTTPException(status_code=404, detail="Todo not found")
    todos.pop(idx)
    return None
