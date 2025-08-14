from sqlmodel import create_engine, Session, SQLModel
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """
     Database configuration
    """
    database_url: str ="sqlite: ///./mastermind.db"

    class Config:
        env_file = ".env"


settings = Settings()

engine= create_engine(settings.database_url, echo=True, connect_args={"check_same_thread": False})

def create_db_and_tables():
    """
     Create the database tables if they do not exist
    """
    SQLModel.metadata.create_all(engine)

def get_session():
    """
     Dependency function to obtain a database session.
    """
    with Session(engine) as session:
        yield session