import random
import logging
from app.client.ai_client import generate_from_ai
from typing import List

# Dictionay with static hints to be used in case the call to gemini api fails
RINDDLE_HINTS = {
    '0': "The number of planets in our solar system that have no natural satellites. what number is it?",
    '1': "The only number that is neither prime nor composite. what number is it?", 
    '3': "The number of primary colors. What number is it?", 
    '4': "The number of chemical elements in the air. What number is it?",
    '5': "The number of major oceans on planet Earth. What number is it?", 
    '6': "The number of faces of a cube. What number is it? ", 
    '7': "The number of continents. What number is it?", 
    '8': "The figure of eternity lying down. What number is it?", 
    '9': "The number of the jersey worn by Michael Jordan. What number is it?" 
}

logger = logging.getLogger(__name__)

def get_unguessed_digits(guessed_number: str, secret_number: List[str]) -> List[str]:
    """
        Identifies the digits in the secret number that the player has not yet guessed.
    """
    unguessed = []
    secret_counts = {d:secret_number.count(d) for d in set(secret_number)}

    for digit in guessed_number:
        if digit in secret_number and secret_counts[digit]>0:
            secret_counts[digit] -=1
    
    for digit, count in secret_counts.items():
        if count >0:
            unguessed.append(digit)

    return unguessed

def generate_hint(guessed_number: str, secret_number: List[str]) ->str:
    """
    Generates a hint. It can be a custom AI riddle or a fallback riddle.
    """
    unguessed_digits = get_unguessed_digits(guessed_number,secret_number)

    if unguessed_digits:
        unguessed_str = ", ".join(unguessed_digits)
        prompt = f""" You are a clue generator for a Mastermind game. The secret number contains the following 
        digits that the player has not yet guessed: {unguessed_str}. Your task is to generate a general culture 
        clue related to one of these numbers. The clue must be a riddle or a question whose answer is one of these 
        numbers. Do not mention the number directly in the question. The answer should be just the riddle, 
        without explanation. Example: If the number is '7', the hint could be: 'The number of continents. 
        What number is it?' or if the number is '5', the hint could be: 'The number of major oceans on planet Earth. What number is it?'  """

        ai_riddle = generate_from_ai(prompt)

        if ai_riddle:
            logger.info("AI hint generated successfully")
            return ai_riddle
        else:
            logger.warning("AI failed, using fallback riddle")
            riddle_digit = random.choice(unguessed_digits)
            return RINDDLE_HINTS.get(riddle_digit)
    
    return "Don't give up, you're doing great!"