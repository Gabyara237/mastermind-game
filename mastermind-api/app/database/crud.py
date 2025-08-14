from typing import List
from sqlmodel import Session, select
from app.models import Player, GameSession, GameAttempt

def get_player_by_name(session: Session, player_name: str) -> Player:
    """
        Search for a player by name. If it does not exist, create it.
    """
    player = session.exec(select(Player).where(Player.name== player_name)).first()

    if not player:
        player= Player(name=player_name)
        session.add(player)
        session.commit()
        session.refresh(player)

    return player


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
