from jose import jwt, JWTError, ExpiredSignatureError
from app.core.config import settings

def decode_and_validate(token: str) -> dict: # функция проверки токена
    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALG],
        )
        if not payload.get("sub"):
            raise ValueError("Токен отсутствует")
        return payload
    except ExpiredSignatureError:
        raise ValueError("Истек срок годности токена")
    except JWTError:
        raise ValueError("Ошибка токена")