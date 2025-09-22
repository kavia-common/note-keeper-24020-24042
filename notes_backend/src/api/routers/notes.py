"""
Notes router providing RESTful CRUD operations.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from ..models.schemas import Note, NoteCreate, NoteUpdate
from ..repositories.notes_repository import NotesRepository
from ..dependencies import get_notes_repository

router = APIRouter(
    prefix="/notes",
    tags=["Notes"],
)


# PUBLIC_INTERFACE
@router.get(
    "",
    response_model=List[Note],
    summary="List notes",
    description="Retrieve all notes ordered by last update time (descending).",
    responses={
        200: {"description": "List of notes successfully retrieved."}
    },
)
def list_notes(repo: NotesRepository = Depends(get_notes_repository)) -> List[Note]:
    """Return the list of all notes."""
    return repo.list_notes()


# PUBLIC_INTERFACE
@router.post(
    "",
    response_model=Note,
    status_code=status.HTTP_201_CREATED,
    summary="Create a note",
    description="Create and return a new note using the provided title, content, and optional tags.",
    responses={
        201: {"description": "Note created successfully."},
        422: {"description": "Validation error."}
    },
)
def create_note(payload: NoteCreate, repo: NotesRepository = Depends(get_notes_repository)) -> Note:
    """Create a new note."""
    return repo.create_note(payload)


# PUBLIC_INTERFACE
@router.get(
    "/{note_id}",
    response_model=Note,
    summary="Get a note",
    description="Retrieve a note by its unique identifier.",
    responses={
        200: {"description": "Note found and returned."},
        404: {"description": "Note not found."}
    },
)
def get_note(note_id: str, repo: NotesRepository = Depends(get_notes_repository)) -> Note:
    """Retrieve a single note by ID."""
    note = repo.get_note(note_id)
    if not note:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note


# PUBLIC_INTERFACE
@router.put(
    "/{note_id}",
    response_model=Note,
    summary="Update a note",
    description="Replace fields of a note by its ID. Partial updates are supported; only provided fields are changed.",
    responses={
        200: {"description": "Note updated successfully."},
        404: {"description": "Note not found."}
    },
)
def update_note(note_id: str, payload: NoteUpdate, repo: NotesRepository = Depends(get_notes_repository)) -> Note:
    """Update a note by ID."""
    updated = repo.update_note(note_id, payload)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return updated


# PUBLIC_INTERFACE
@router.delete(
    "/{note_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a note",
    description="Delete a note by its unique identifier.",
    responses={
        204: {"description": "Note deleted successfully."},
        404: {"description": "Note not found."}
    },
)
def delete_note(note_id: str, repo: NotesRepository = Depends(get_notes_repository)) -> None:
    """Delete a note by ID."""
    deleted = repo.delete_note(note_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return None
