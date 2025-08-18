from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from app.database.connection import create_db_and_tables

from app.routes.game_router import router as game_router
from app.routes.auth_routes import router as auth_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    print("Database and tables created successfully")
    yield



app = FastAPI(
    title ="Mastermind API",
    lifespan= lifespan    
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)

# Routers
app.include_router(auth_router,prefix="/api/v1")
app.include_router(game_router, prefix="/api/v1")


@app.get("/")
def read_root():
    return{"message": "Welcome!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)