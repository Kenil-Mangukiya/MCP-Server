from pydantic import BaseModel, EmailStr, Field

class CreateUserSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=5)
