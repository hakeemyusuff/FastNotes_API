from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


id = 0
notes: dict[int, dict[str, str]] = {}

class Note(BaseModel):
    id: int = id + 1
    title: str
    body: str



@app.get("/api/notes")
async def get_notes():
    """This endpoints returns all the notes"""
    if not notes:
        return {"message": "You currently don't have any notes.."}
    return notes

@app.post("/api/notes/")
async def add_note(note: Note):
    if note:
        note_dict = Note.model_dump(note)
        id = note_dict["id"]
        notes.update({id :note_dict})
    return {"message": "Note added successfully.", "note": note}