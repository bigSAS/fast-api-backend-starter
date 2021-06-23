from app.errors import AppError, ErrorMessage


class RepositoryError(AppError):
    """
    General repository error. Inherit from it as much as u wish.
    """

    def __init__(self, message: str):
        super().__init__(message)

    @property
    def error_message(self) -> ErrorMessage:
        return ErrorMessage(message=self.message)


class EntityNotFoundError(RepositoryError):
    """
    Throw when entity is not found.
    """
    pass


class InvalidQueryLimitError(RepositoryError):
    """
    Throw when invalid query limit.
    """
    pass


class InvalidOrderByError(RepositoryError):
    """
    Throw when order by is invalid.
    """
    pass


class TransactionError(RepositoryError):
    """
    Throw when db transaction fails.
    """
    pass
