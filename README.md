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
![Uploading api.png…]()

<img width="368" height="344" alt="a1" src="https://github.com/user-attachments/assets/5589e5dc-f368-41f0-a497-8a6491b4b59f" />


## The mortality experiment

Data lives only in a Python list (`tasks`) in memory. If you create tasks and then restart the server (`Ctrl+C` then `uvicorn main:app ...` again), every task you created is gone — you're back to the 3 seed tasks. This is because nothing is written to disk; the list only exists inside the running process's memory. Fixing this is the entire reason Week 3 (databases) exists.

## Stage 7 — AI vs me

**My prompt** (also saved as `ai-prompt.md`, written from memory without re-reading the assignment):

> Build me a small Python REST API for managing a to-do list, using FastAPI.
>
> Requirements:
> - In-memory storage only, no database. Start with 3 example tasks, each with an id (number), title (text) and done (true/false).
> - Endpoints: GET /, GET /health, GET /tasks, GET /tasks/{id} (404 if missing), POST /tasks (from a JSON body with a "title" field, reject empty/missing titles with 400, new tasks start as not done with the next free id), PUT /tasks/{id} (update title and/or done, 404 if unknown), DELETE /tasks/{id} (204 no body, 404 if unknown).
> - Use proper HTTP status codes throughout (200, 201, 204, 400, 404).
> - I want Swagger/OpenAPI docs available automatically.
>
> Please give me the full code in one file.

**What the AI did better / understand well enough to explain:** the AI's code is shorter and more idiomatic in places — e.g. it uses a single `Task` Pydantic model for creation instead of a separate `TaskCreate`, which is fine here since I don't need extra fields. I understand exactly why it works: FastAPI parses the JSON body into that model automatically.

**What it got wrong or quietly ignored:**
- I asked for a `400` on empty/missing titles. The AI declared `title: str` as a *required* Pydantic field, so a **missing** title returns FastAPI's automatic `422 Unprocessable Entity` with a `{"detail": [...]}` body — not the `400` + custom message I asked for.
- Worse: an **empty string** title (`{"title": ""}`) passes Pydantic's `str` type check silently and gets created as a valid task. My spec said "empty... titles" should be rejected — the AI's code doesn't actually catch this case at all.
- I asked for JSON error bodies but didn't specify a shape. The AI kept FastAPI's default `{"detail": "..."}` instead of a custom `{"error": "..."}` shape — a reasonable default, but different from what I ended up building by hand.
- `GET /` returns a generic welcome message instead of the `{"name", "version", "endpoints"}` structure I'd originally settled on — I never actually specified that shape in this prompt, so this isn't the AI's fault, but it's a good example of the AI silently deciding for me.

**What my prompt forgot to specify:**
- The exact shape of `GET /`'s response body.
- The exact shape of error responses (`{"error": ...}` vs `{"detail": ...}`).
- That "empty string" needs explicit `.strip()`-style checking — Pydantic's `str` type alone doesn't enforce non-emptiness.
- Whether 422 vs 400 mattered to me (it does, per the original assignment, but I didn't say so precisely enough in my own words).

**One-sentence rematch note:** after adding "reject empty/whitespace-only titles explicitly in code (don't rely on Pydantic's default 422), and always return errors as `{"error": "..."}`, not FastAPI's default `{"detail": ...}`" to the prompt, a regenerated version correctly returned 400 with the right error shape on both missing and empty titles.

