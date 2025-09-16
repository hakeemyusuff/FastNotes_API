from pydantic import BaseModel
from datetime import datetime


class NoteCreate(BaseModel):
    title: str
    body: str


class NoteResponse(NoteCreate):
    id: int
    created_at: datetime
    edited_at: datetime | None

    class Config:
        from_attribute = True
class NoteUpdate(BaseModel):
    title: str | None = None
    body: str | None = None
    