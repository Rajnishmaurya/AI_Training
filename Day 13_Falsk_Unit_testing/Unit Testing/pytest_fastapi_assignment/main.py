from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

app = FastAPI()

tasks=[
  {
    "id": 1,
    "title": "Prepare report",
    "status": "Pending"
  },
  {
    "id": 2,
    "title": "Review invoice",
    "status": "Completed"
  },
  {
    "id": 3,
    "title": "Update dashboard",
    "status": "Pending"
  }
]

class Tasks(BaseModel):
    id:int
    title:str
    status:str

@app.get("/tasks")
def get_tasks():
    return tasks

@app.get("/tasks/{id}")
def get_task(id: int):
    if id>=len(tasks):
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks[id-1]


@app.post("/tasks")
def add_tasks(task: Tasks):
    tasks.append(task)
    return task

@app.put("/tasks/{id}")
def update_tasks(id:int):
    tasks[id]["status"]="done"
    return tasks[id-1]

@app.delete("/tasks/{id}")
def delete_task(id: int):
    for i,task in enumerate(tasks):
        if task["id"] == id:
            return tasks.pop(i)

    raise  HTTPException(status_code=404, detail="Task not found")

