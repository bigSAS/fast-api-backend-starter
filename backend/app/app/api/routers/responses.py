from app.errors import ErrorMessage

# 4 auth protected endpoints
AUTHENTICATED = {
    400: {'model': ErrorMessage},
    401: {'model': ErrorMessage},
}


# 4 auth protected endpoints
PROTECTED = {
    400: {'model': ErrorMessage},
    403: {'model': ErrorMessage},
}

NO_CONTENT = {
    204: {'model': None}
}
