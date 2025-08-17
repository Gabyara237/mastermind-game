import pytest
from unittest.mock import patch, Mock
from app.services.hints_service import(
    get_unguessed_digits,
    generate_hint,
    RINDDLE_HINTS
)

class TestGetUnguessedDigits:
    """
        Tests for the get_unguessed_digits function
    """

    def test_no_digits_guessed_correctly(self):
        """ 
            Test when noo digits from secret are in the guess
        """

        guessed_number = "1234"
        secret_number = ['5','6','7','8']

        unguessed = get_unguessed_digits(guessed_number,secret_number)

        assert set(unguessed) == {'5','6','7','8'}
        assert len(unguessed) == 4

    def test_all_digits_guessed_correctly(self):
        """
            Test when all digits from secret are in the guess.
        """

        guessed_number = "1234"
        secret_number = ['1','2','3','4']

        unguessed = get_unguessed_digits(guessed_number, secret_number)

        assert unguessed == []
    
    def test_some_digits_guessed_correctly(self):
        """
            Test when some digits from secret are in the guess
        """

        guessed_number = "1256"
        secret_number = ['1','2','3','4']

        unguessed = get_unguessed_digits(guessed_number,secret_number)

        assert set(unguessed) == {'3', '4'}
        assert len(unguessed) == 2

    def test_duplicates_in_secret_number(self):
        """
            Test handle duplicates in secret number correctly.
        """
        guessed_number = "1123"
        secret_number = ['1','1','2','4']

        unguessed = get_unguessed_digits(guessed_number, secret_number) 

        assert unguessed == ['4']

    def test_duplicates_in_gueseed_number(self):
        """ 
            Test handle duplicates in guessed number correctly
        """

        guessed_number = "1111"
        secret_number = ['1','2','3','4']

        unguessed = get_unguessed_digits(guessed_number, secret_number)

        assert set(unguessed) == {'2','3', '4'}
        assert len(unguessed) == 3


    def test_complex_duplicate_scenario(self):
        """
            Test complex scenario with duplicates in both
        """

        guessed_number = "1122"
        secret_number = ['1','1','3','3']

        unguessed = get_unguessed_digits(guessed_number, secret_number)

        assert set(unguessed) == {'3'}
        assert len(unguessed) == 1

    
    def test_more_guesses_than_secret_digits(self):
        """ 
            Test when player guesses more of a digit than secret contains
        """

        guessed_number = "1111"
        secret_number = ['1','2','3','4']

        unguessed = get_unguessed_digits(guessed_number, secret_number)

        assert set(unguessed) == {'2','3','4'}


class TestGenerateHint:
    """
        Tests for the generate_hint function
    """

    @patch('app.services.hints_service.generate_from_ai')
    def test_generate_hint_ai_success(self, mock_ai):
        """
            Test AI successfully generates hint.
        """
        mock_ai.return_value = "The number of continents on Earth. What number is it?"
        guessed_number = "1234"
        secret_number = ['5','6','7','8']

        hint = generate_hint(guessed_number, secret_number)

        assert hint == "The number of continents on Earth. What number is it?"
        mock_ai.assert_called_once()

        #Verify the prompt contains unguessed digits
        call_args = mock_ai.call_args[0][0]
        for digit in ['5','6','7','8']:
            assert digit in call_args 

    @patch('app.services.hints_service.generate_from_ai')
    def test_generate_hint_ai_failure_fallback_to_dictionary(self, mock_ai):
        """
            Test when ai fails, fallback to dictionary riddles.
        """

        mock_ai.return_value= None
        guessed_number = "1234"
        secret_number = ['7','8','9','0']

        hint = generate_hint(guessed_number,secret_number)

        mock_ai.assert_called_once()

        # Should fallback to dictionary riddle for one of unguessed digits
        assert hint in [
            RINDDLE_HINTS['7'],
            RINDDLE_HINTS['8'],
            RINDDLE_HINTS['9'],
            RINDDLE_HINTS['0']
        ]

    @patch('app.services.hints_service.random.choice')
    @patch('app.services.hints_service.generate_from_ai')
    def test_generate_hint_random_selection_fallback(self, mock_ai, mock_choice):
        """
            Test Fallback randomly selects from unguessed digits
        """
        mock_ai.return_value = None
        mock_choice.return_value = '5'
        guessed_number = "1234"
        secret_number = ['5','6','7','8']

        hint = generate_hint(guessed_number,secret_number)

        assert hint == RINDDLE_HINTS['5']
        mock_choice.assert_called_once()
        call_args = mock_choice.call_args[0][0]
        assert set(call_args) == {'5','6','7','8'}