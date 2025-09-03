from fastapi import APIRouter, Query, HTTPException, status, Depends
from sqlmodel import select
from ..models import models
from ..dependencies import SessionDep
from datetime import datetime
from typing import Annotated


router = APIRouter(prefix="/api/v2", tags=["V2"])


@router.post("/notes/", response_model=models.Note)
def create_note(note: models.NoteCreate, session: SessionDep):
    db_note = models.Note.model_validate(note)
    session.add(db_note)
    session.commit()
    session.refresh(db_note)
    return db_note


@router.get("/notes/", response_model=list[models.Note])
def get_all_notes(
    session: SessionDep,
    offset: int = 0,
    limit: Annotated[int, Query(le=100)] = 100,
):
    notes = session.exec(select(models.Note))
    return notes


def get_note_dep(session: SessionDep, note_id: int):
    note = session.get(models.Note, note_id)
    if not note:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found.",
        )
    return note


@router.get("/notes/{note_id}", response_model=models.Note)
def get_note(
    note_id: int,
    note: models.Note = Depends(get_note_dep),
):
    return note


@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(
    session: SessionDep,
    note_id: int,
    note: models.Note = Depends(get_note_dep),
) -> None:

    session.delete(note)
    session.commit()
    return None


@router.patch("/notes/{note_id}", response_model=models.Note)
def update_note(
    session: SessionDep,
    note_id: int,
    edited_note: models.NoteUpdate,
    old_note: models.Note = Depends(get_note_dep),
):
    note_data = edited_note.model_dump(exclude_unset=True)
    old_note.sqlmodel_update(note_data)
    old_note.edited_at = datetime.now()
    session.add(old_note)
    session.commit()
    session.refresh(old_note)
    return old_note
