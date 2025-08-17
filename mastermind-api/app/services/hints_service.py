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
        prompt = f"""You are a clue generator for a Mastermind game. The secret number contains the following 
        digits that the player has not yet guessed: {unguessed_str}. 

        Your task is to generate a riddle whose answer is EXACTLY ONE of these single digits: {unguessed_str}.

        REQUIREMENTS:
        - The answer must be a single digit (0, 1, 2, 3, 4, 5, 6, 7, 8, or 9)
        - The riddle should reference something that naturally counts or measures to that digit
        - Use intermediate difficulty - avoid obvious questions like 'How many legs does a dog have?'
        - Do not mention the digit directly in the question
        - Do not use self-referential phrases like 'I am the number of...'
        - Phrase as a neutral question or statement

        EXAMPLES:
        - If the digit is 7: "How many continents are there on Earth?"
        - If the digit is 5: "How many major oceans cover our planet?"
        - If the digit is 3: "How many primary colors exist in traditional color theory?"
        BAD EXAMPLES (avoid these):
`       - "How many sides does a quadrilateral have?" (word contains answer)

        ADDITIONAL REQUIREMENTS:
        - Ensure the question has ONE clear, unambiguous answer
        - Avoid questions that could be interpreted in multiple ways
        - The riddle should have universal consensus on the answer

        Generate ONE riddle whose answer is one of these digits: {unguessed_str}
                
        """

        ai_riddle = generate_from_ai(prompt)

        if ai_riddle:
            logger.info("AI hint generated successfully")
            return ai_riddle
        else:
            logger.warning("AI failed, using fallback riddle")
            riddle_digit = random.choice(unguessed_digits)
            return RINDDLE_HINTS.get(riddle_digit)
    
    return "Don't give up, you're doing great!"