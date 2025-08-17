from fastapi import FastAPI, HTTPException, status, Depends
from pydantic import BaseModel
from datetime import datetime
from typing import Any

app = FastAPI()


class NoteIn(BaseModel):
    title: str
    body: str


class NoteOut(BaseModel):
    id: int
    title: str
    body: str
    created_at: datetime
    edited_at: datetime


id = 0
notes: dict[int, dict[str, str]] = {}


@app.get("/api/notes", response_model=dict[int, NoteOut])
async def get_notes(search: str | None = None) -> Any:
    """This endpoints returns all the notes"""
    if not notes:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No Note found"
        )
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


@app.get("/api/notes/{note_id}", response_model=NoteOut)
async def get_note(note_id: int) -> Any:
    note = notes.get(note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found",
        )
    return note


@app.delete("/api/notes/{note_id}")
async def delete_note(note_id: int) -> dict[str, str]:
    if notes.get(note_id):
        notes.pop(note_id)
        return {"message": f"note with id {note_id} deleted successfully."}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.put("/api/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_note(note_id: int, updated_note: NoteIn) -> None:
    if not notes.get(note_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The note doesn't exist.",
        )

    old_note = NoteOut.model_validate(notes.get(note_id))
    new_title = updated_note.title
    new_body = updated_note.body
    old_note.title = new_title
    old_note.body = new_body
    old_note.edited_at = datetime.now()
    modified_note = NoteOut.model_dump(old_note)
    notes[note_id] = modified_note
    return


@app.post(
    "/api/notes/",
    response_model=NoteOut,
    status_code=status.HTTP_201_CREATED,
)
async def add_note(note: NoteIn):
    global id
    if note:
        note_dict = NoteIn.model_dump(note)
        note_dict.update({"id": id})
        note_dict.update({"created_at": datetime.now()})
        note_dict.update({"edited_at": datetime.now()})
        notes.update({id: note_dict})
        id = id + 1
    return note_dict
