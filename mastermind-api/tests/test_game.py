import pytest
from app.services.game import evaluate_player_number

class TestEvaluatePlayerNumber:
    """
        Tests for the evaluate_player_number function.
    """
   
    def test_all_correct_positions(self):
        """
            Test all digits in correct positions.
        """
        player_number = ['2','5','3','1']
        secret_number = ['2','5','3','1']

        correct_numbers, correct_positions = evaluate_player_number(player_number,secret_number)

        assert correct_numbers == 4
        assert correct_positions == 4

    def test_no_correct_numbers(self):
        """
            Test no digits match at all.
        """
        player_number = ['3','5','1','3']
        secret_number = ['2','2','2','2']

        correct_numbers, correct_positions = evaluate_player_number(player_number,secret_number)
        
        assert correct_numbers == 0
        assert correct_positions == 0

    def test_all_correct_numbers_wrong_positions(self):
        """
            Test all digits correct but in wrong positions.
        """
        player_number = ['2', '4', '5', '7']
        secret_number = ['7', '5', '4', '2']

        correct_numbers, correct_positions = evaluate_player_number(player_number, secret_number)

        assert correct_numbers == 4
        assert correct_positions == 0


    def test_correct_and_wrong_positions(self):
        """
            Test some digits in correct positions, some in wrong positions
        """
        player_number = ['2','3','4','6']
        secret_number = ['5','2','3','6']

        correct_numbers, correct_positions = evaluate_player_number(player_number,secret_number)

        assert correct_numbers == 3
        assert correct_positions == 1
        

    def test_duplicates_in_secret_number(self):
        """
            Test handle duplicates in secret number correctly.
        """
        player_number = ['1','4','3','5']
        secret_number = ['1','3','3','5']

        correct_numbers, correct_positions = evaluate_player_number(player_number, secret_number)

        assert correct_numbers == 3
        assert correct_positions == 3


    def test_duplicates_in_player_number(self):
        """
            Test handle duplicates in player number correctly.
        """
        player_number = ['2','2','1','3']
        secret_number = ['1','4','2','3']

        correct_numbers, correct_positions = evaluate_player_number(player_number, secret_number)

        assert correct_numbers == 3
        assert correct_positions == 1

    def test_duplicates_both_numbers(self):
        """
            Test handle duplicates in both numbers correctly.
        """
        player_number = ['2','2','3','3']
        secret_number = ['3','3','3','2']

        correct_numbers, correct_position = evaluate_player_number(player_number, secret_number)

        assert correct_numbers == 3
        assert correct_position == 1

        