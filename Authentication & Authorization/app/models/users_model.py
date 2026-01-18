from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Annotated

class User(BaseModel):
    id: int
    name: Annotated[str, Field(description="Enter your name")]
    email: EmailStr
    password: Annotated[str, Field(description="Must be unique")]

class LoginRequest(BaseModel):
    email: EmailStr
    password: str