class AppError(Exception):
    status_code: int = 400
    detail: str = "Request cannot be processed"


class EmailAlreadyIsTaken(AppError):
    status_code = 409
    detail = "Email already is taken"


class UsernameAlreadyIsTaken(AppError):
    status_code = 409
    detail = "Username already is taken"


class InvalidCredentials(AppError):
    status_code = 401
    detail = "Invalid email or password"


class InvalidToken(AppError):
    status_code = 401
    detail = "Invalid or expired token"