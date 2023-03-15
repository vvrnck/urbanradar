class AbroadException(Exception):
    pass


class InvalidToken(AbroadException):
    def __init__(self):
        message = dict(
            [
                ("code", 498),
                ("message", "Expired or invalid token."),
                ("error_code", "invalid_token"),
            ]
        )
        super().__init__(message)


class UnexpectedServerError(AbroadException):
    def __init__(self):
        message = dict(
            [
                ("code", 500),
                ("message", "There was a connection error with the server."),
                ("error_code", "unexpected_server_error"),
            ]
        )
        super().__init__(message)


class EntityNotFound(AbroadException):
    def __init__(self):
        message = dict(
            [
                ("code", 404),
                ("message", "The requested entity could not be found."),
                ("error_code", "entity_not_found"),
            ]
        )
        super().__init__(message)


class AccessDenied(AbroadException):
    def __init__(self):
        message = dict(
            [
                ("code", 403),
                ("message", "Insufficient permission."),
                ("error_code", "access_denied"),
            ]
        )
        super().__init__(message)