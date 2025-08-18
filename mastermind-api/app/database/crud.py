from typing import List, Optional
from app.auth.auth_utils import hash_password,verify_password
from sqlmodel import Session, select
from app.models import User, Player, GameSession, GameAttempt


def create_user(session: Session, username: str, email: str, password: str) -> User:
    """
        Create user and player automatically
    """
    # Create user
    hashed_password = hash_password(password)
    user = User(
        username = username,
        email = email,
        hashed_password= hashed_password
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Create player automatically profile
    player= Player(user_id =user.id)
    session.add(player)
    session.commit()
    session.refresh(player)
    
    return user


def get_user_by_username(session: Session, username: str) -> Optional[User]:
    """
        Search for a player by username.
    """
    return session.exec(select(User).where(User.username== username)).first()
    

def get_player_by_user_id(session: Session, user_id: int) -> Optional[Player]:
    """
        Gets player profile by user id
    """
    return session.exec(select(Player).where(Player.user_id == user_id)).first()


def get_user_by_email(session: Session, email: str) -> Optional[User]:
    """
        Gets user by email
    """
    return session.exec(select(User).where(User.email == email)).first()
    

def authenticate_user(session: Session, username:str,password:str) -> Optional[User]:
    """
        Authenticates a user by verifying username and password
    """

    user = get_user_by_username(session, username)
    if not user:
        return None
    if not verify_password(password,user.hashed_password):
        return None
    
    return user


def create_game_session(session: Session, player_id: int, secret_number:str, difficulty_level: int, attempts_left:int) -> GameSession:
    """ 
        Crates a new game session in the database
    """
    game_session = GameSession(
        player_id = player_id,
        secret_number = secret_number,
        difficulty_level = difficulty_level,
        attempts_left = attempts_left
    )

    session.add(game_session)
    session.commit()
    session.refresh(game_session)
    return game_session

def create_game_attempt(session: Session, game_session_id: int, guessed_number: str, correct_numbers: int, correct_positions: int) -> GameAttempt:
    """
        Register a game attempt in the database
    """
    game_attempt = GameAttempt(
        game_session_id = game_session_id,
        guessed_number = guessed_number,
        correct_numbers = correct_numbers,
        correct_positions = correct_positions
    )

    session.add(game_attempt)
    session.commit()
    session.refresh(game_attempt)

    return game_attempt

def update_game_session(session: Session, game_session: GameSession):
    """
        Update a game session
    """
    session.add(game_session)
    session.commit()
    session.refresh(game_session)

    return game_session

def get_top_players(session:Session) -> List[Player]:
    """Gets the 3 best players by score"""
    return session.exec(select(Player).order_by(Player.score.desc()).limit(3)).all()
