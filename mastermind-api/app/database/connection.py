from sqlmodel import create_engine, Session, SQLModel
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    
    database_url: str ="sqlite: ///./mastermind.db"

    class Config:
        env_file = ".env"


settings = Settings()

engine= create_engine(settings.database_url, echo=True, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session