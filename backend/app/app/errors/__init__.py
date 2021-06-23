from pydantic import BaseModel


class ErrorMessage(BaseModel):
    message: str


class AppError(Exception):
    """
    Base app error class. Use for inheritance.
    """

    def __init__(self, message: str):
        self._message = message

    @property
    def message(self):
        return self._message

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return f'[{self.__class__.__name__}] {self.message}'
