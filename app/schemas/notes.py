from pydantic import BaseModel
from datetime import datetime

class NoteIn(BaseModel):
    title: str
    body: str


class NoteOut(BaseModel):
    id: int
    title: str
    body: str
    created_at: datetime
    edited_at: datetime
