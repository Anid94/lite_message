class AppError(Exception):
    status_code: int = 400
    detail: str = "Request cannot be processed"


class EmailAlreadyIsTaken(AppError):
    status_code = 409
    detail = "Email already is taken"


class UsernameAlreadyIsTaken(AppError):
    status_code = 409
    detail = "Username already is taken"


class UserNotFound(AppError):
    status_code = 404
    detail = "User not found"


class InvalidCredentials(AppError):
    status_code = 401
    detail = "Invalid email or password"


class InvalidToken(AppError):
    status_code = 401
    detail = "Invalid or expired token"


class CantRequestYourself(AppError):
    status_code = 409
    detail = "Can't request yourself"


class ContactAlreadyExists(AppError):
    status_code = 409
    detail = "Contact already is taken"


class ContactNotFound(AppError):
    status_code = 404
    detail = "Contact not found"


class ContactAlreadyAccepted(AppError):
    status_code = 409
    detail = "Contact already accepted"


class ContactNotPending(AppError):
    status_code = 409
    detail = "Contact request is no longer pending"


class ContactNotAccepted(AppError):
    status_code = 409
    detail = "Contact not accepted"