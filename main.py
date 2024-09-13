import time
from fastapi import FastAPI
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

app = FastAPI()

# データベースURLを指定
DATABASE_URL = "mysql+mysqlconnector://root:password@mysql_db:3306/todo_db"

# SQLAlchemyエンジンの作成
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# リトライロジックを追加
def wait_for_db():
    while True:
        try:
            with engine.connect() as connection:
                print("Database is up and running!")
                break
        except OperationalError:
            print("Database is not ready, waiting...")
            time.sleep(5)

# データベース接続待機
wait_for_db()

# Todoモデルの定義
class Todo(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String(255), index=True)
    completed = Column(Boolean, default=False)

# データベースの作成
Base.metadata.create_all(bind=engine)

@app.post("/todos/")
def create_todo(task: str):
    db = SessionLocal()
    new_todo = Todo(task=task)
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    db.close()
    return new_todo

@app.get("/todos/")
def read_todos():
    db = SessionLocal()
    todos = db.query(Todo).all()
    db.close()
    return todos

@app.put("/todos/{todo_id}/")
def update_todo(todo_id: int, completed: bool):
    db = SessionLocal()
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        todo.completed = completed
        db.commit()
        db.refresh(todo)
    db.close()
    return todo

@app.delete("/todos/{todo_id}/")
def delete_todo(todo_id: int):
    db = SessionLocal()
    todo = db.query(Todo).filter(Todo.id == todo_id).first()
    if todo:
        db.delete(todo)
        db.commit()
    db.close()
    return {"message": "Todo deleted"}
