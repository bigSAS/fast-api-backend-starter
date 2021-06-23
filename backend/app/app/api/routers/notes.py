from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.api.schemas.note import Note, NoteCreate, NotesPaginated
from app.api.schemas.user import User
from app.api.dependencies import get_db, authenticated_user
from app.repositories.notes import NotesRepository
from app.database.models.note import Note as NoteEntity

router = APIRouter()


@router.get("/notes", tags=['admin'],
            response_model=NotesPaginated,
            dependencies=[Depends(authenticated_user)])
def list_notes(
        page: int = 0, limit: int = 100, order_by: str = None,
        db: Session = Depends(get_db)):
    """
    todo: ...
    """
    return NotesPaginated.from_paginated_query(
        NotesRepository(db).all_paginated(page=page, limit=limit, order=order_by)
    )


@router.get("/notes/mine", tags=['notes'],
            response_model=NotesPaginated)
def read_user_notes(
        page: int = 0, limit: int = 100, order_by: str = None,
        db: Session = Depends(get_db),
        current_user: User = Depends(authenticated_user)):
    """
    todo: ...
    """
    return NotesPaginated.from_paginated_query(
        NotesRepository(db).filter_paginated(
            NoteEntity.owner_id == current_user.id,
            page=page,
            limit=limit,
            order=order_by
        )
    )


@router.post("/notes/create", tags=['notes'],
             response_model=Note)
def create_note_for_current_user(
        note: NoteCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(authenticated_user)):
    """
    todo: ...
    """
    new_note = NoteEntity(
        owner_id=current_user.id,
        title=note.title,
        description=note.description
    )
    NotesRepository(db).save(new_note)
    return new_note


# todo: delete user note
