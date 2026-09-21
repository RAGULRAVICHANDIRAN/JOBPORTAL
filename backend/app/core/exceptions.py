"""
JobPilot AI — Custom Exceptions

Structured error handling with consistent HTTP status codes and messages.
"""

from fastapi import HTTPException, status


class AppException(HTTPException):
    """Base application exception."""

    def __init__(self, status_code: int, detail: str, error_code: str = "APP_ERROR"):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code


# --- Auth Exceptions ---

class InvalidCredentialsError(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            error_code="INVALID_CREDENTIALS",
        )


class TokenExpiredError(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired.",
            error_code="TOKEN_EXPIRED",
        )


class TokenInvalidError(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or malformed token.",
            error_code="TOKEN_INVALID",
        )


class UserAlreadyExistsError(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail="A user with this email already exists.",
            error_code="USER_EXISTS",
        )


class UserNotFoundError(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found.",
            error_code="USER_NOT_FOUND",
        )


# --- Resource Exceptions ---

class NotFoundError(AppException):
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} not found.",
            error_code="NOT_FOUND",
        )


class DuplicateError(AppException):
    def __init__(self, resource: str = "Resource"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"{resource} already exists.",
            error_code="DUPLICATE",
        )


# --- Application Exceptions ---

class DuplicateApplicationError(AppException):
    def __init__(self, company: str, title: str):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"You have already applied to '{title}' at {company}.",
            error_code="DUPLICATE_APPLICATION",
        )


class AutomationPausedError(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Automation is currently paused.",
            error_code="AUTOMATION_PAUSED",
        )


class ManualActionRequiredError(AppException):
    def __init__(self, reason: str):
        super().__init__(
            status_code=status.HTTP_428_PRECONDITION_REQUIRED,
            detail=f"Manual action required: {reason}",
            error_code="MANUAL_ACTION_REQUIRED",
        )


class RateLimitExceededError(AppException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later.",
            error_code="RATE_LIMIT_EXCEEDED",
        )


class FileTooLargeError(AppException):
    def __init__(self, max_mb: int):
        super().__init__(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File exceeds maximum size of {max_mb}MB.",
            error_code="FILE_TOO_LARGE",
        )
