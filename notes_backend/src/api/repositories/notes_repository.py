"""
Repository abstraction for Notes and a simple in-memory implementation.

This layer isolates persistence from the rest of the application so that
future integration with the 'notes_database' service can be accomplished by
swapping the repository implementation without changing the routers.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Optional, Dict
from datetime import datetime, timezone
import uuid

from ..models.schemas import Note, NoteCreate, NoteUpdate


class NotesRepository(ABC):
    """Repository interface for notes persistence."""

    # PUBLIC_INTERFACE
    @abstractmethod
    def list_notes(self) -> List[Note]:
        """List all notes, most recently updated first."""
        raise NotImplementedError

    # PUBLIC_INTERFACE
    @abstractmethod
    def get_note(self, note_id: str) -> Optional[Note]:
        """Retrieve a note by its ID or return None if not found."""
        raise NotImplementedError

    # PUBLIC_INTERFACE
    @abstractmethod
    def create_note(self, payload: NoteCreate) -> Note:
        """Create and persist a new note from the provided payload."""
        raise NotImplementedError

    # PUBLIC_INTERFACE
    @abstractmethod
    def update_note(self, note_id: str, payload: NoteUpdate) -> Optional[Note]:
        """Update a note by ID with provided fields. Returns updated note or None if not found."""
        raise NotImplementedError

    # PUBLIC_INTERFACE
    @abstractmethod
    def delete_note(self, note_id: str) -> bool:
        """Delete a note by ID. Returns True if deleted, False if not found."""
        raise NotImplementedError


class InMemoryNotesRepository(NotesRepository):
    """
    Simple in-memory repository backed by a dict.

    Notes:
    - Not suitable for production; intended as a mock/stub for early development.
    - Provides deterministic ordering by updated_at descending.
    """
    def __init__(self) -> None:
        self._store: Dict[str, Note] = {}

    def list_notes(self) -> List[Note]:
        return sorted(self._store.values(), key=lambda n: n.updated_at, reverse=True)

    def get_note(self, note_id: str) -> Optional[Note]:
        return self._store.get(note_id)

    def create_note(self, payload: NoteCreate) -> Note:
        now = datetime.now(timezone.utc)
        note_id = uuid.uuid4().hex
        note = Note(
            id=note_id,
            title=payload.title,
            content=payload.content,
            tags=payload.tags,
            created_at=now,
            updated_at=now,
        )
        self._store[note_id] = note
        return note

    def update_note(self, note_id: str, payload: NoteUpdate) -> Optional[Note]:
        existing = self._store.get(note_id)
        if not existing:
            return None
        updated = existing.model_copy(update={
            "title": payload.title if payload.title is not None else existing.title,
            "content": payload.content if payload.content is not None else existing.content,
            "tags": payload.tags if payload.tags is not None else existing.tags,
            "updated_at": datetime.now(timezone.utc),
        })
        self._store[note_id] = updated
        return updated

    def delete_note(self, note_id: str) -> bool:
        return self._store.pop(note_id, None) is not None
