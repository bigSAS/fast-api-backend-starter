from app.database.models.note import Note as NoteEntity
from app.repositories import Repository

# todo - delete + model
class NotesRepository(Repository):
    """
    Notes repository.
    """
    entity = NoteEntity
