from datetime import datetime, timezone
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship


class User(SQLModel, table = True):
    """
        System User- Authentication only
    """
    __tablename__="users"

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str
    created_at: datetime = Field(default_factory= lambda:datetime.now(timezone.utc))

    player: Optional["Player"] = Relationship(
        back_populates = "user",
        sa_relationship_kwargs={"uselist": False}
    )

class Player(SQLModel, table= True):
    """
        Game profile. Model for players.
    """
    __tablename__="player"

    id: Optional[int]= Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique= True)


    score: int = Field(default=0)
    last_attempt_score: Optional[int] = Field(default=None)

    #Relationships
    user: User = Relationship(back_populates="player")
    # One to many relationship with GameSession
    game_sessions: List["GameSession"]= Relationship(back_populates="player")

    @property
    def display_name(self) -> str:
        return self.user.username


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