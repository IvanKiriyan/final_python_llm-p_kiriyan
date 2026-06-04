from pydantic import BaseModel, EmailStr

class RegisterRequest(BaseModel): #pydantic-схемы для регистрации
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"