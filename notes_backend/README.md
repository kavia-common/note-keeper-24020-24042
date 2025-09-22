# Notes Backend (FastAPI)

Modern, modular FastAPI service for managing notes with CRUD endpoints.

- Theme: Ocean Professional (blue primary, amber secondary)
- Architecture: Routers + Schemas + Repository abstraction
- Storage: In-memory mock repository ready to be replaced with notes_database-backed implementation

## Quick start

1. Install dependencies
   - Using the provided requirements.txt

2. Run the server
   - uvicorn src.api.main:app --host 0.0.0.0 --port 3001 --reload

3. Explore the docs
   - OpenAPI JSON: /openapi.json
   - Swagger UI: /docs
   - ReDoc: /redoc
   - Usage help: /docs/usage

## REST Endpoints

- GET /notes — list all notes
- POST /notes — create a note
- GET /notes/{note_id} — get a note by id
- PUT /notes/{note_id} — update a note
- DELETE /notes/{note_id} — delete a note

## Project structure

- src/api/core/config.py — app metadata and theme
- src/api/models/schemas.py — pydantic models (Note, NoteCreate, NoteUpdate)
- src/api/repositories/notes_repository.py — repository interface + in-memory implementation
- src/api/routers/notes.py — CRUD endpoints
- src/api/main.py — app setup, CORS, OpenAPI customizations, router inclusion

## Future database integration

Replace InMemoryNotesRepository with a database-backed implementation:

- Implement a concrete class that satisfies NotesRepository.
- Provide a dependency override in src/api/dependencies.py based on environment flags.
- Use environment variable NOTES_DATABASE_URL (already read in config but unused here).

Environment variables should be provided via a .env file and loaded by the process manager; do not commit secrets.
