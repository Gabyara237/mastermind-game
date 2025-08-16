from app.models import Player, GameSession


def calculate_score_for_attempt(difficulty_level: int, correct_numbers: int, correct_positions: int) -> int:
    """
        Calculates the base score for a attempt based on the difficulty level.
    """
    if difficulty_level == 1: # Easy level
        return(correct_numbers*600) + (correct_positions*1200)
    elif difficulty_level ==2: # Medium level
        return (correct_numbers*800) + (correct_positions*1600)     
    else: # Hard level
        return (correct_numbers*1200) + (correct_positions*2400)


def penalize_score(difficulty_level: int, new_score: int) -> int:
    """
        Applies a penalty to the score based on the difficulty level
    """

    if difficulty_level == 1:
        return new_score - 50
    elif difficulty_level == 2:
        return new_score - 100
    else:
        return new_score - 150
    
def update_player_score(player: Player, session_data: GameSession, correct_numbers: int, correct_positions: int) -> int:
    
    """
        Calculates the score for the current attempt, applies a penalty if the score is lower
        than to the last attempt's score, and updates the player's total score.
    """

    #Calculate the base score for the current attempt
    score_this_attempt = calculate_score_for_attempt(
        session_data.difficulty_level,
        correct_numbers,
        correct_positions
    )

    # Apply penalty logic
    if player.last_attempt_score is not None and player.last_attempt_score > 0 and score_this_attempt < player.last_attempt_score:
        score_this_attempt = penalize_score(session_data.difficulty_level,score_this_attempt)

    # Update the total score and the last attempt's score for the player
    player.score += score_this_attempt
    player.last_attempt_score = score_this_attempt

    return score_this_attempt
