from core.errors import ValidationError, NotFoundError, PermissionError


EXCEPTION_CODE_MAP = {
    ValidationError: 2,
    NotFoundError: 3,
    PermissionError: 4,
}


def handle_exception(exc):
    for exc_type, code in EXCEPTION_CODE_MAP.items():
        if isinstance(exc, exc_type):
            return code, str(exc)

    return 1, "Unexpected error"