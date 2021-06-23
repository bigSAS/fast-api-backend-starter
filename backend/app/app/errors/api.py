from app.errors import AppError, ErrorMessage


class ApiError(AppError):
    """
    General api error. Inherit from it as much as u wish.
    """
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self._status_code = status_code

    @property
    def status_code(self) -> int:
        return self._status_code

    @property
    def error_message(self) -> ErrorMessage:
        return ErrorMessage(message=self.message)

    def __repr__(self):
        return f'[{self.status_code}] {super().__repr__()}'


class AuthError(ApiError):
    """
    Authentication error [401]
    """
    def __init__(self, message: str):
        super().__init__(message, 401)


class ForbiddenError(ApiError):
    """
    Api resource forbidden error [403]
    """
    def __init__(self, message: str):
        super().__init__(message, 403)


class BadRequestError(ApiError):
    """
    Api request invalid data error [400]
    """
    def __init__(self, message: str):
        super().__init__(message, 400)


class NotFoundError(ApiError):
    """
    Api not found error [404]
    """
    def __init__(self, message: str):
        super().__init__(message, 404)


class UnknownApiError(ApiError):
    """
    Api unknown error (bug) [500]
    """
    def __init__(self, message: str):
        super().__init__(message, 500)

# todo: add missing error classes if necessary
