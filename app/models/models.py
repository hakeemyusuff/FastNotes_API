from typing import Annotated
from datetime import datetime
from sqlmodel import Field, SQLModel


class NoteBase(SQLModel):
    title: str | None = Field(index=True)
    body: str | None


class Note(NoteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.now)
    edited_at: datetime = Field(default_factory=datetime.now)


class NoteCreate(NoteBase):
    pass


class NoteUpdate(NoteBase):
    title: str | None = None
    body: str | None = None
