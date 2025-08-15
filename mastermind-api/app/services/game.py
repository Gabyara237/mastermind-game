from collections import defaultdict

def evaluate_player_number(player_number, secret_number):
    """
       Evaluates the player_number against the secret_number and
       retunns the count of correct numbers an correct positions 
    """
    correct_numbers_count = 0
    correct_positions_count = 0

    # Count frequency of each digit in secret number for efficient lookups
    digit_secret_count = defaultdict(int)

    # Track which positions have been matched to avoid double counting
    matched_positions = [False]*len(secret_number)

    # Store the frequency of each digit in the secret number
    for digit in secret_number:
        digit_secret_count[digit] +=1

    # Count digits in correct positions
    for i in range(len(player_number)):
        if player_number[i] == secret_number[i]:
            correct_positions_count +=1
            correct_numbers_count +=1
            digit_secret_count[player_number[i]] -= 1
            matched_positions[i] = True
    
    #  Count correct digits in wrong positions (not yet matched)
    for i in range(len(player_number)):
        if not matched_positions[i]:
            digit = player_number[i]
            if digit_secret_count[digit]> 0:
                correct_numbers_count +=1
                digit_secret_count[digit] -= 1

    return correct_numbers_count, correct_positions_count