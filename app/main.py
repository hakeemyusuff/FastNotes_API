from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()


class Note(BaseModel):
    title: str
    body: str
    created_at: datetime = datetime.now()
    edited_at: datetime = datetime.now()


id = 0
notes: dict[int, dict[str, str]] = {}


@app.get("/api/notes")
async def get_notes(search: str | None = None):
    """This endpoints returns all the notes"""
    if not notes:
        return {"message": "You currently don't have any notes.."}
    if search is not None and search != "":
        normalised_search = search.strip().lower()
        search_result: dict[int, dict[str, str]] = {}
        for key, note_dict in notes.items():
            id = key
            title = note_dict["title"].lower()
            body = note_dict["body"].lower()
            if normalised_search in title or normalised_search in body:
                note = notes[id]
                search_result.update({id: note})
                continue
        return search_result

    return notes


@app.get("/api/notes/{note_id}")
async def get_note(note_id: int):
    note = notes.get(note_id, "This note have been moved or deleted.")
    return note


@app.delete("/api/notes/{note_id}")
async def delete_note(note_id: int):
    if notes.get(note_id):
        notes.pop(note_id)
        return {"message": f"note with id {note_id} deleted successfully."}
    else:
        return {"message": "This note doesn't exist."}


@app.put("/api/notes/{note_id}")
async def update_note(note_id: int, updated_note: Note):
    if not notes.get(note_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The note doesn't exist.",
        )
        
    old_note =  Note.model_validate(notes.get(note_id))
    new_title = updated_note.title
    new_body = updated_note.body
    old_note.title = new_title
    old_note.body = new_body
    old_note.edited_at = datetime.now()
    modified_note = Note.model_dump(old_note)
    notes[note_id] = modified_note
    return {"message": "Note updated successfully."}
    


@app.post("/api/notes/")
async def add_note(note: Note):
    global id
    if note:
        note_dict = Note.model_dump(note)
        note_dict.update({"id": id})
        notes.update({id: note_dict})
        id = id + 1
    return {"message": "Note added successfully.", "note": note_dict}
