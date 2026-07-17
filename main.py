from typing import Optional

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A small in-memory to-do list API built for FlyRank Internship W2 A1.",
)


@app.exception_handler(HTTPException)
def http_exception_handler(request: Request, exc: HTTPException):
    # The assignment spec wants {"error": "..."} instead of FastAPI's default {"detail": "..."}
    return JSONResponse(status_code=exc.status_code, content={"error": exc.detail})


# --- "database" ---------------------------------------------------------
# In-memory only: a plain Python list. Fast and simple, but everything is
# lost when the server restarts. That's on purpose (see README "mortality
# experiment") -- persistence is next week's problem (a real database).
SEED_TASKS = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Write README", "done": False},
    {"id": 3, "title": "Learn FastAPI", "done": True},
]
tasks = [dict(t) for t in SEED_TASKS]
next_id = 4


class TaskCreate(BaseModel):
    title: Optional[str] = None


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None


# --- root / health -------------------------------------------------------

@app.get("/", summary="API info", description="Describes this API and its endpoints.")
def root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"],
    }


@app.get("/health", summary="Health check", description="Used by uptime monitors to confirm the server is alive.")
def health():
    return {"status": "ok"}


# --- read ------------------------------------------------------------

@app.get("/tasks", summary="List tasks", description="Returns all tasks. Supports optional filtering and search.")
def list_tasks(
    done: Optional[bool] = None,
    search: Optional[str] = None,
    limit: Optional[int] = None,
    offset: int = 0,
):
    result = tasks

    if done is not None:
        result = [t for t in result if t["done"] == done]

    if search:
        needle = search.lower()
        result = [t for t in result if needle in t["title"].lower()]

    result = result[offset:]
    if limit is not None:
        result = result[:limit]

    return result


@app.get("/tasks/{task_id}", summary="Get one task", description="Returns a single task by id, or 404 if it doesn't exist.")
def get_task(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.get("/stats", summary="Task stats", description="Returns counts of total / done / open tasks.")
def stats():
    done_count = sum(1 for t in tasks if t["done"])
    return {"total": len(tasks), "done": done_count, "open": len(tasks) - done_count}


# --- create ------------------------------------------------------------

@app.post("/tasks", status_code=201, summary="Create a task", description="Creates a task. Requires a non-empty title.")
def create_task(body: TaskCreate):
    global next_id
    if not body.title or not body.title.strip():
        raise HTTPException(status_code=400, detail="title is required and cannot be empty")

    task = {"id": next_id, "title": body.title.strip(), "done": False}
    tasks.append(task)
    next_id += 1
    return task


# --- update / delete -----------------------------------------------------

@app.put("/tasks/{task_id}", summary="Update a task", description="Replaces title and/or done for a task. 404 if unknown, 400 if body invalid.")
def update_task(task_id: int, body: TaskUpdate):
    for task in tasks:
        if task["id"] == task_id:
            if body.title is not None:
                if not body.title.strip():
                    raise HTTPException(status_code=400, detail="title cannot be empty")
                task["title"] = body.title.strip()
            if body.done is not None:
                task["done"] = body.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


@app.delete("/tasks/{task_id}", status_code=204, summary="Delete a task", description="Removes a task. 404 if unknown.")
def delete_task(task_id: int):
    for i, task in enumerate(tasks):
        if task["id"] == task_id:
            tasks.pop(i)
            return
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")


# --- extras --------------------------------------------------------------

@app.post("/reset", summary="Reset data", description="Restores the 3 example tasks. Handy for demos.")
def reset():
    global tasks, next_id
    tasks = [dict(t) for t in SEED_TASKS]
    next_id = 4
    return {"message": "reset", "tasks": tasks}
