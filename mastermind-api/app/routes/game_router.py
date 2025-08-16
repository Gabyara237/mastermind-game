from fastapi import APIRouter, Depends, HTTPException, Body
from sqlmodel import Session
from app.database.connection import get_session
from app.services.game import evaluate_player_number
from app.services.score import update_player_score
from app.database.crud import(
    get_player_by_name,
    create_game_session,
    create_game_attempt,
    update_game_session,
    get_top_players
)
from app.models import GameSession
from app.client.random_number import get_secret_number

router = APIRouter()

@router.post("/start_game/")
def start_game(player_name: str, difficulty_level: int, session: Session=Depends(get_session)):
    """
        Endpoint to start a new game
    """

    if difficulty_level not in [1,2,3]:
        raise HTTPException(status_code = 400, detail="Invalid difficulty level. Use 1, 2 or 3.")
    
    player = get_player_by_name(session,player_name)

    secret_number_list, attempts_left = get_secret_number(difficulty_level)
    secret_number_str = "".join(secret_number_list)

    game_session = create_game_session(
        session,
        player_id=player.id,
        secret_number= secret_number_str,
        difficulty_level= difficulty_level,
        attempts_left=attempts_left
    )

    return {
        "message": "Game started!",
        "session_id": game_session.id,
        "attempts_left": game_session.attempts_left
    }

@router.post("/guess/")
def make_a_guess(
    session_id: int = Body(...), 
    guessed_number: str = Body(..., max_length=4, min_length=4), 
    session: Session = Depends(get_session)
):
    """
        Endpoint to register an attempt to guess the number
    """

    game_session = session.get(GameSession, session_id)
    
    if not game_session:
        raise HTTPException(status_code=404, detail="Game session not found")
    if not game_session.is_active:
        raise HTTPException(status_code=400, detail="Game session already ended")

    if not guessed_number.isdigit():
        raise HTTPException(status_code=400, detail="The guessed number must be of 4 numeric digits ")
    
    guessed_number_list = list(guessed_number)
    secret_number_list = list(game_session.secret_number)

    correct_numbers, correct_positions = evaluate_player_number( guessed_number_list, secret_number_list)

    player = game_session.player

    score_this_attempt = update_player_score(
        player,
        game_session,
        correct_numbers,
        correct_positions
    )

    session.add(player)
    session.commit()
    session.refresh(player)

    create_game_attempt(
        session,
        game_session_id= game_session.id,
        guessed_number= guessed_number,
        correct_numbers= correct_numbers,
        correct_positions= correct_positions
    )

    game_session.attempts_left -= 1
    update_game_session(session, game_session)

    session.refresh(game_session)

    history = [
        {"guessed_number": attempt.guessed_number,
         "correct_numbers": attempt.correct_numbers,
         "correct_positions": attempt.correct_positions 
        }
        for attempt in game_session.attempts
    ]

    if game_session.attempts_left == 0:
        game_session.is_active = False
        update_game_session(session, game_session)
        return {"message": "Game Over", "result": "LOSE", "total_score": player.score}

    if correct_positions == 4:
        game_session.is_active = False
        update_game_session(session, game_session)
        return {"message": "Congratulations, you won", "result": "WIN", "total_score": player.score}

    return {
        "message":"Attempt registered.",
        "score_this_attempt": score_this_attempt,
        "total_score": player.score,
        "result":{
            "correct_numbers": correct_numbers,
            "correct_positions": correct_positions
        },
        "attempts_left": game_session.attempts_left,
        "history": history
    }


@router.get("/top_players/")
def get_top_three_players(session: Session = Depends(get_session)):
    """
        Endpoint to obtain the 3 best players
    """
    players = get_top_players(session)
    return {"top_players": players}