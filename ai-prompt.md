# Prompt given to the AI

Build me a small Python REST API for managing a to-do list, using FastAPI.

Requirements:
- In-memory storage only, no database. Start with 3 example tasks, each with an id (number),
  title (text) and done (true/false).
- Endpoints:
  - GET / -> basic info about the API
  - GET /health -> health check
  - GET /tasks -> list all tasks
  - GET /tasks/{id} -> get one task, 404 if it doesn't exist
  - POST /tasks -> create a task from a JSON body with a "title" field. Reject empty/missing
    titles with a 400 error. New tasks should start as not done and get the next free id.
  - PUT /tasks/{id} -> update a task's title and/or done status. 404 if unknown id.
  - DELETE /tasks/{id} -> delete a task, return 204 with no body. 404 if unknown id.
- Use proper HTTP status codes throughout (200, 201, 204, 400, 404).
- I want Swagger/OpenAPI docs available automatically.

Please give me the full code in one file.
