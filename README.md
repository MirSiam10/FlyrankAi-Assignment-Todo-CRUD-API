# Task API

A small in-memory to-do list API — built for FlyRank Internship, Backend Track, Week 2, Assignment A1.

Supports full CRUD (Create, Read, Update, Delete) on tasks, with interactive Swagger docs.

## How to run

```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

Then visit `http://localhost:8000/` in your browser, or `http://localhost:8000/docs` for Swagger UI.

## Endpoints

| Method | Path            | Description                          | Success | Errors        |
|--------|-----------------|---------------------------------------|---------|---------------|
| GET    | `/`             | API info                              | 200     | –             |
| GET    | `/health`       | Health check                          | 200     | –             |
| GET    | `/tasks`        | List all tasks (supports `?done=`, `?search=`, `?limit=`, `?offset=`) | 200 | – |
| GET    | `/tasks/{id}`   | Get a single task                     | 200     | 404           |
| POST   | `/tasks`        | Create a task (`{"title": "..."}`)    | 201     | 400           |
| PUT    | `/tasks/{id}`   | Update a task's title and/or done     | 200     | 400, 404      |
| DELETE | `/tasks/{id}`   | Delete a task                         | 204     | 404           |
| GET    | `/stats`        | Task counts: total / done / open      | 200     | –             |
| POST   | `/reset`        | Restore the 3 seed tasks              | 200     | –             |

## Example

```
$ curl -i -X POST http://localhost:8000/tasks -H "Content-Type: application/json" -d '{"title":"Buy milk"}'
HTTP/1.1 201 Created
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

## Swagger UI

![Swagger UI screenshot](swagger-screenshot.png)

*(Take your own screenshot from `http://localhost:8000/docs` after trying the CRUD cycle via "Try it out", and drop it in this folder as `swagger-screenshot.png`.)*

## The mortality experiment

Data lives only in a Python list (`tasks`) in memory. If you create tasks and then restart the server (`Ctrl+C` then `uvicorn main:app ...` again), every task you created is gone — you're back to the 3 seed tasks. This is because nothing is written to disk; the list only exists inside the running process's memory. Fixing this is the entire reason Week 3 (databases) exists.
