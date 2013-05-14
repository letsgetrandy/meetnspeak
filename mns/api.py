class BadRequest(Exception):
    response_code = 400

    def __init__(self, *args, **kwargs):
        self.token_expired = kwargs.get('token_expired', False)


class Unauthorized(Exception):
    response_code = 401


class Forbidden(Exception):
    response_code = 403


class NotFound(Exception):
    response_code = 404


class MethodNotAllowed(Exception):
    response_code = 405


class ServerError(Exception):
    response_code = 500
