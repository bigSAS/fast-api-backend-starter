from app.errors import ErrorMessage

# 4 auth protected endpoints
AUTHENTICATED = {
    400: {'model': ErrorMessage},
    401: {'model': ErrorMessage},
}


# 4 permission protected endpoints
PROTECTED = {
    400: {'model': ErrorMessage},
    403: {'model': ErrorMessage},
}

NOT_FOUND = {
    400: {'model': ErrorMessage},
    404: {'model': ErrorMessage},
}

# 4 no response body endpoints
NO_CONTENT = {
    400: {'model': ErrorMessage},
    204: {'model': None}
}
