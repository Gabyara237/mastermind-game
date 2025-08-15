import requests
import random
from typing import List, Tuple
import  logging

# Config logging for debugging
logger = logging.getLogger(__name__)

def get_secret_number(difficulty_level: int) -> Tuple[List[str], int]:
    """
        Gets a 4 digit secret number from random.org API
        based on the difficulty level.
        If random.org API fails, uses local random generation 
    """

    if difficulty_level == 1: 
        max_digit = 5
        attempts = 12
    elif difficulty_level == 2:
        max_digit = 7
        attempts = 10
    else:
        max_digit = 9
        attempts = 8

    try:
        response = requests.get(f'https://www.random.org/integers/?num=4&min=0&max={max_digit}&col=4&base=10&format=plain&rnd=new')
        response.raise_for_status()

        # Process response
        number= ''.join(response.text.split())

        logger.info(f"Generated secret number from random.org for difficulty {difficulty_level}")
        return list(number), attempts
    except (requests.RequestException, ValueError) as e:
        logger.warning(f"Failed to get number from random.org: {e}. Using local fallback...")
        # Fallback: generate random number locally 
        return [str(random.randint(0,max_digit)) for _ in range(4)], attempts