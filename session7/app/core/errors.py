class AppError(Exception):
    """Base error for application"""
    pass


class ValidationError(AppError):
    pass


class NotFoundError(AppError):
    pass


class PermissionError(AppError):
    pass