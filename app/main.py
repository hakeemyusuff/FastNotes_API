from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()


id = 0
notes: dict[int, dict[str, str]] = {}

class Note(BaseModel):
    title: str
    body: str
    created_at: datetime = datetime.now()
    edited_at: datetime = datetime.now()



@app.get("/api/notes")
async def get_notes():
    """This endpoints returns all the notes"""
    if not notes:
        return {"message": "You currently don't have any notes.."}
    return notes

@app.post("/api/notes/")
async def add_note(note: Note):
    global id
    if note:
        note_dict = Note.model_dump(note)
        note_dict.update({"id": id})
        notes.update({id :note_dict})
        id = id + 1
    return {"message": "Note added successfully.", "note": note_dict}