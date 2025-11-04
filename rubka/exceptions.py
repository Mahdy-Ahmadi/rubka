class APIRequestError(Exception):
    """Base class for all API request errors."""
    def __init__(self, status: str, dev_message: str = None):
        self.status = status
        self.dev_message = dev_message
        msg = f"{self.__class__.__name__}: {status}"
        if dev_message:
            msg += f" | Message : {dev_message}"
        super().__init__(msg)


class InvalidAccessError(APIRequestError):
    """Raised when access is invalid."""

class InvalidTokenError(Exception):
    pass

class InvalidInputError(APIRequestError):
    """Raised when input is invalid."""


class TooRequestError(APIRequestError):
    """Raised when too many requests are made."""


def raise_for_status(response: dict):
    status = response.get("status")
    dev_message = response.get("dev_message")

    if status == "INVALID_ACCESS":
        raise InvalidAccessError(status, dev_message)
    elif status == "INVALID_INPUT":
        raise InvalidInputError(status, dev_message)
    elif status == "TOO_REQUEST":
        raise TooRequestError(status, dev_message)
    elif status != "OK":
        raise APIRequestError(status, dev_message)