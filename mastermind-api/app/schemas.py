from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    """
        Model to create a user
    """
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    """
        Model for user login
    """
    username: str
    password: str

class UserRegisterResponse(BaseModel):
    """
        User registration response model
    """
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    """
        User response model 
    """
    id: int
    username: str
    email: str
    created_at: datetime
    score: int

    class Config:
        from_attributes = True
class Token(BaseModel):
    """
        Model for JWT token
    """
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
        Model for data contained in the token
    """
    username: Optional[str] = None
    
class PlayerResponse(BaseModel):
    """
        Player response model
    """
    id: int
    user_id: int 
    score: int
    last_attempt_score: Optional[int]
    display_name: str

    class Config:
        from_attributes = True


class GameSessionResponse(BaseModel):
    """
        Game session response model
    """
    id: int
    difficulty_level: int
    attempts_left: int
    is_active: bool
    player_id: int

    class Config:
        from_attributes = True