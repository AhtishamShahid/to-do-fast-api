# main.py
from fastapi import FastAPI
from app import models, crud, schemas
from app.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/todos/", response_model=schemas.Todo)
def create_todo(todo: schemas.TodoCreate):
    db = SessionLocal()
    db_todo = crud.create_todo(db=db, todo=todo)
    return db_todo

@app.get("/todos/{todo_id}", response_model=schemas.Todo)
def read_todo(todo_id: int):
    db = SessionLocal()
    db_todo = crud.get_todo(db, todo_id=todo_id)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@app.put("/todos/{todo_id}", response_model=schemas.Todo)
def update_todo(todo_id: int, todo: schemas.TodoUpdate):
    db = SessionLocal()
    db_todo = crud.update_todo(db=db, todo_id=todo_id, todo=todo)
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return db_todo

@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    db = SessionLocal()
    crud.delete_todo(db=db, todo_id=todo_id)
    return {"detail": "Todo deleted"}
