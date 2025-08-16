from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class Player(SQLModel, table= True):
    """
     Model for players.
     Id is the primary key
    """
    __tablename__="player"

    id: Optional[int]= Field(default=None, primary_key=True)
    name: str = Field(index=True)
    score: int = Field(default=0)
    last_attempt_score: Optional[int] = Field(default=None)

    # One to many relationship with GameSession
    game_sessions: List["GameSession"]= Relationship(back_populates="player")

class GameSession(SQLModel, table= True):
    """
     Model for game sessions.
     Represents a Mastermind game
    """
    __tablename__= "game_session"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    secret_number: str
    difficulty_level: int
    attempts_left: int
    is_active: bool = Field(default=True)

    # Foreign key to relate to Player
    player_id: Optional[int]= Field(default=None, foreign_key="player.id")

    # Many to one relationship with Player
    player: Optional[Player] = Relationship(back_populates="game_sessions") 
    
    # One to many relationship with GameAttempt
    attempts: List["GameAttempt"] = Relationship(back_populates="game_session")

class GameAttempt(SQLModel, table= True):
    """
     Model for a player's attempts in a game session.
    """
    __tablename__="game_attempt"

    id: Optional[int] = Field(default=None, primary_key=True)
    guessed_number: str
    correct_numbers: int
    correct_positions: int

    # Foreign key to relate GameSession
    game_session_id: Optional[int] = Field(default=None,foreign_key="game_session.id")
    
    # Many to one relationship with GameSession
    game_session: Optional["GameSession"] = Relationship(back_populates="attempts")