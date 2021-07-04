from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.routers import responses as res
from app.api.permissions.user_permissions import IsAdmin
from app.api.schemas.note import Note, NoteCreate, NotesPaginated
from app.api.schemas.user import User
from app.api.dependencies import get_db, authenticated_user, Restricted
from app.repositories.notes import NotesRepository
from app.database.models.note import Note as NoteEntity

router = APIRouter()


@router.get("/notes", tags=['admin'],
            response_model=NotesPaginated,
            responses=res.AUTHENTICATED | res.PROTECTED,
            dependencies=[
                Depends(authenticated_user),
                Depends(Restricted([IsAdmin]))
            ])
async def list_notes(
        page: int = 0, limit: int = 100, order_by: str = None,
        db: Session = Depends(get_db)):
    """
    List notes with pagination.
    """
    return NotesPaginated.from_paginated_query(
        NotesRepository(db).all_paginated(page=page, limit=limit, order=order_by)
    )


@router.get("/notes/mine", tags=['notes'],
            response_model=NotesPaginated,
            responses=res.AUTHENTICATED)
async def read_user_notes(
        page: int = 0, limit: int = 100, order_by: str = None,
        db: Session = Depends(get_db),
        current_user: User = Depends(authenticated_user)):
    """
    List user notes with pagination.
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
             response_model=Note,
             responses=res.AUTHENTICATED)
async def create_note_for_current_user(
        note: NoteCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(authenticated_user)):
    """
    Create note for user.
    """
    new_note = NoteEntity(
        owner_id=current_user.id,
        title=note.title,
        description=note.description
    )
    NotesRepository(db).save(new_note)
    return new_note
