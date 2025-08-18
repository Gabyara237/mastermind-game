from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from app.auth.auth_utils import create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from app.auth.auth_middleware import get_current_user
from app.database.crud import create_user, authenticate_user, get_user_by_username, get_user_by_email
from app.schemas import UserCreate, UserLogin, Token, UserResponse
from app.database.connection import get_session

router = APIRouter(prefix="/auth",tags=["Authentication"])

@router.post("/register",response_model= UserResponse)
async def register_user( user_data: UserCreate, session:Session=Depends(get_session)):
    """
        Register a new user
    """

    if get_user_by_username(session, user_data.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is alredy registered"
        )
    
    if get_user_by_email(session, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is alredy registered"
        )
    
    try:
        user = create_user(
            session= session,
            username = user_data.username,
            email= user_data.email,
            password = user_data.password
        )
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail= "Error creating user"
        )
    

@router.post("/login", response_model= Token)
async def login(login_data: UserLogin, session: Session = Depends(get_session)):
    """
        Authenticates a user and returns a JWT token
    """
    user = authenticate_user(session,login_data.username, login_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect credentials ",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, 
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token, 
        "token_type": "bearer"
    }

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user = Depends(get_current_user)):
    """
        Gets current user information
    """
    return current_user
