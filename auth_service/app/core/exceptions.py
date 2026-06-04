# Ошибки
from fastapi import HTTPException

class BaseHTTPException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=self.status_code, detail=detail)

class UserAlreadyExistsError(BaseHTTPException):
    status_code = 409
    def __init__(self):
        super().__init__(detail="Пользователь с такой почтой уже существует")

class InvalidCredentialsError(BaseHTTPException):
    status_code = 401
    def __init__(self):
        super().__init__(detail="Неправильная почта или пароль")

class InvalidTokenError(BaseHTTPException):
    status_code = 401
    def __init__(self):
        super().__init__(detail="Неправильный токен")

class TokenExpiredError(BaseHTTPException):
    status_code = 401
    def __init__(self):
        super().__init__(detail="Срок действия токена истек")

class UserNotFoundError(BaseHTTPException):
    status_code = 404
    def __init__(self):
        super().__init__(detail="Такого пользователя не существует")

class PermissionDeniedError(BaseHTTPException):
    status_code = 403
    def __init__(self):
        super().__init__(detail="Отказано в доступе")