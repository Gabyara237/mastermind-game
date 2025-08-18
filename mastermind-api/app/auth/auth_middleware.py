from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session
from app.auth.auth_utils import verify_token
from app.database.crud import get_user_by_username, get_player_by_user_id
from app.models import User
from app.database.connection import get_session

security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), session: Session = Depends(get_session)) -> User:
    """
        Obtains the current user based on the JWT token
    """

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credentials could not be validated",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try: 
        token = credentials.credentials
        username = verify_token(token)

        if username is None:
            raise credentials_exception
        
    except Exception:
        raise credentials_exception
    
    user = get_user_by_username(session, username=username)
    if user is None:
        raise credentials_exception
    
    return user

def get_current_player(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """
        Gets the player profile of the current user
    """
    
    player = get_player_by_user_id(session, current_user.id)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Player profile not found"
        )
    return player