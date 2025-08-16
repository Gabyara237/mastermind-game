from fastapi import FastAPI
from app.database.connection import create_db_and_tables
from app.routes.game_router import router as game_router

app = FastAPI(title ="Mastermind API")

app.include_router(game_router, prefix="/api/v1")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    print("Database and tables created successfully")

@app.get("/")
def read_root():
    return{"message": "Welcome!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)