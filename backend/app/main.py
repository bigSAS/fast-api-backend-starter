from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api.routers import users
from app.core.config import settings
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
]

app = FastAPI(
    title=settings.APP_NAME,
    description="This is a sas-kodzi project, with auto docs for the API and everything",
    version="0.0.1",
    openapi_tags=tags_metadata
)


# app.include_router(items.router)  # todo: remove all items related code ;) -> l8r
app.include_router(users.router)


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

