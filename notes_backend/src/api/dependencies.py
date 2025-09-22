"""
Dependency providers for the FastAPI app.

Currently provides an in-memory notes repository. Future work can add
a database-backed implementation and switch this provider based on env.
"""
from typing import Generator
from .repositories.notes_repository import InMemoryNotesRepository, NotesRepository


# PUBLIC_INTERFACE
def get_notes_repository() -> Generator[NotesRepository, None, None]:
    """Provide a NotesRepository implementation to route handlers."""
    repo = InMemoryNotesRepository()
    try:
        yield repo
    finally:
        # Nothing to cleanup for in-memory; placeholder for real DB sessions
        pass
