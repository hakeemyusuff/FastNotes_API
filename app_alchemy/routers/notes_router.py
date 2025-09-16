from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated, Any

from sqlalchemy.orm import Session

# from app_alchemy.crud.note_crud import get_note
from app_alchemy.dependencies import get_db
from ..models.models import Note
from app_alchemy.schemas.notes_schema import NoteCreate, NoteResponse, NoteUpdate
from datetime import datetime

router = APIRouter(prefix="/api/notes", tags=["Notes"])


@router.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    note_count = db.query(Note).count()
    return {"number_of_notes": note_count}


@router.get("/", response_model=list[NoteResponse])
def list_notes(db: Session = Depends(get_db)):
    notes = db.query(Note).all()
    return notes


@router.get("/{note_id}", response_model=NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found.",
        )
    return note


@router.post(
    "/",
    response_model=NoteResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_note(note: NoteCreate, db: Session = Depends(get_db)):
    new_note = Note(**note.model_dump())
    db.add(new_note)
    db.commit()
    db.refresh(new_note)
    return new_note

@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(Note).filter(Note.id == note_id).first()
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found.",
        )
    db.delete(note)
    db.commit()
    return {"OK": True}
            
@router.patch("/{note_id}", response_model=NoteResponse)
def update_note(note_id: int, note: NoteUpdate ,db: Session = Depends(get_db)):
    db_note = db.query(Note).filter(Note.id == note_id).first()
    if not db_note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found.",
        )
    edited_note = note.model_dump(exclude_unset=True)
    for key, value in edited_note.items():
        setattr(db_note, key, value)
    db.commit()
    db.refresh(db_note)
    return db_note