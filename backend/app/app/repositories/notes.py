from app.database.models.note import Note as NoteEntity
from app.repositories import Repository


class NotesRepository(Repository):
    """
    todo: ...
    """
    entity = NoteEntity
