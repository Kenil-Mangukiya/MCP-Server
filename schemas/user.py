from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class CreateUserSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=30)
    email: EmailStr
    password: str = Field(..., min_length=5)

class UpdateUserSchema(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=30)
    email: EmailStr
    password: Optional[str] = Field(None, min_length=5)

class DeleteUserSchema(BaseModel):
    email: EmailStr
    
class GetUserSchema(BaseModel):
    email: EmailStr