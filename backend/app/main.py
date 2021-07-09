from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.api.routers import users
from app.api.routers import permissions
from app.api.routers import notes
from app.api.routers import user_groups
from app.config import settings
from app.errors.api import ApiError, UnknownApiError

tags_metadata = [
    {
        "name": "auth",
        "description": "Authenticate operations"
    },
    {
        "name": "admin",
        "description": "Admin operations"
    },
    {
        "name": "users",
        "description": "Operations with users"
    },
    {
        "name": "notes",
        "description": "Operation with notes"
    },
]

app = FastAPI(
    title=settings.APP_NAME,
    description="This is a sas-kodzi project, with auto docs for the API and everything",
    version="0.2.0",
    openapi_tags=tags_metadata
)


app.include_router(users.router)
app.include_router(user_groups.router)
app.include_router(permissions.router)
app.include_router(notes.router)


# todo: log requests in error handlers -> read about fast api logging first


# noinspection PyUnusedLocal
@app.exception_handler(ApiError)
def handle_api_error(request, error: ApiError):
    """
    Api error handler.
    todo: how to utilize request ? -> error logging ???
    """
    return JSONResponse(
        status_code=error.status_code,
        content={'message': error.error_message.message}
    )


# noinspection PyUnusedLocal
@app.exception_handler(Exception)
def handle_unknown_api_error(request, exception: Exception):
    """
    Unknown Api error handler 500 - bug :(
    """
    error = UnknownApiError(f'{exception.__class__.__name__} - {str(exception)}')
    return JSONResponse(
        status_code=error.status_code,
        content={'message': error.error_message.message}
    )
