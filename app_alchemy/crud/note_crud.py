from ..models.models import Note
from ..dependencies import get_db
from ..schemas.notes_schema import NoteCreate, NoteResponse
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status


