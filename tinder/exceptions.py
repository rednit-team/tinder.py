class TinderException(Exception):
    pass


class Unauthorized(TinderException):
    pass


class Forbidden(TinderException):
    pass


class NotFound(TinderException):
    pass


class RequestFailed(TinderException):
    pass
