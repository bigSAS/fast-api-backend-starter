from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from app.api.schemas.note import NoteSchema, NoteCreate
from app.api.schemas.user import UserSchema
from app.api.deps import get_db, authenticated_user
from app.crud import crud_note


router = APIRouter()


@router.get("/notes", response_model=List[NoteSchema], tags=['admin'])
def read_notes(
        skip: int = 0, limit: int = 100,
        db: Session = Depends(get_db)):
    notes = crud_note.get_notes(db=db, skip=skip, limit=limit)
    return notes


@router.get("/notes/mine", response_model=List[NoteSchema], tags=['notes'])
def read_user_notes(
        skip: int = 0, limit: int = 100,
        db: Session = Depends(get_db),
        current_user: UserSchema = Depends(authenticated_user)):
    notes = crud_note.get_user_notes(db=db, user_id=current_user.id, skip=skip, limit=limit)
    return notes


@router.post("/notes/create", response_model=NoteSchema, tags=['notes'])
def create_note_for_user(
        note: NoteCreate,
        db: Session = Depends(get_db),
        current_user: UserSchema = Depends(authenticated_user)):
    return crud_note.create_user_note(db=db, note=note, user_id=current_user.id)
