from typing import ClassVar


class BaseError(Exception):
    MESSAGE: ClassVar[str] = ""
