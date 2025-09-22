"""
Pydantic schemas for Notes domain.
"""
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    """Base schema that contains common fields for a Note."""
    title: str = Field(..., min_length=1, max_length=200, description="Short, descriptive title for the note")
    content: str = Field(..., min_length=1, description="Main content/body of the note")
    tags: Optional[List[str]] = Field(default=None, description="Optional list of tags for organization")


class NoteCreate(NoteBase):
    """Schema for creating a new note."""
    pass


class NoteUpdate(BaseModel):
    """Schema for updating an existing note (partial updates allowed)."""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200, description="Updated title")
    content: Optional[str] = Field(default=None, min_length=1, description="Updated content")
    tags: Optional[List[str]] = Field(default=None, description="Updated tags list")


class Note(NoteBase):
    """Schema returned to clients representing a stored note."""
    id: str = Field(..., description="Unique identifier for the note")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last updated timestamp")
