from fastapi import FastAPI, HTTPException, Depends, Header
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Todo管理系统")

# 模拟数据库（存在内存里）
todos = []
users = {"admin": "123456"}

# ===== 数据模型 =====
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: int = 1

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = False
    priority: Optional[int] = None

# ===== 鉴权 =====
def verify_token(token: str = Header(None)):
    if token != "test-token-123":
        raise HTTPException(status_code=401, detail="无效token")
    return True

# ===== 接口 =====
@app.post("/api/login")
def login(username: str, password: str):
    if users.get(username) == password:
        return {"token": "test-token-123", "code": 200}
    raise HTTPException(status_code=400, detail="用户名或密码错误")

@app.post("/api/todos", status_code=201)
def create_todo(todo: TodoCreate, auth: bool = Depends(verify_token)):
    new_todo = {
        "id": len(todos) + 1,
        "title": todo.title,
        "description": todo.description,
        "completed": False,
        "priority": todo.priority
    }
    todos.append(new_todo)
    return {"data": new_todo, "code": 201}

@app.get("/api/todos")
def get_todos(completed: Optional[bool] = None, 
              priority: Optional[int] = None,
              auth: bool = Depends(verify_token)):
    result = todos.copy()
    if completed is not None:
        result = [t for t in result if t["completed"] == completed]
    if priority:
        result = [t for t in result if t["priority"] == priority]
    return {"data": result, "total": len(result), "code": 200}

@app.get("/api/todos/{todo_id}")
def get_todo(todo_id: int, auth: bool = Depends(verify_token)):
    todo = next((t for t in todos if t["id"] == todo_id), None)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo不存在")
    return {"data": todo, "code": 200}

@app.put("/api/todos/{todo_id}")
def update_todo(todo_id: int, todo: TodoUpdate, auth: bool = Depends(verify_token)):
    for i, t in enumerate(todos):
        if t["id"] == todo_id:
            update_data = todo.dict(exclude_unset=True)
            todos[i].update(update_data)
            return {"data": todos[i], "code": 200}
    raise HTTPException(status_code=404, detail="Todo不存在")

@app.delete("/api/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int, auth: bool = Depends(verify_token)):
    global todos
    todos = [t for t in todos if t["id"] != todo_id]
    return None
