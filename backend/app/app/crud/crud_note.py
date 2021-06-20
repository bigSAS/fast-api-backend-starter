from sqlalchemy.orm import Session
from app.database.models.note import Note
from app.api.schemas.note import NoteCreate

# todo: remove crud package, use repositories


def get_notes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Note).offset(skip).limit(limit).all()


def get_note_by_id():  # todo: leve until repositories
    pass


def get_user_notes(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    print("get_user_notes user id", user_id)
    return db.query(Note).filter_by(owner_id=user_id).offset(skip).limit(limit).all()


def create_user_note(db: Session, note: NoteCreate, user_id: int):
    db_note = Note(**note.dict(), owner_id=user_id)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note
