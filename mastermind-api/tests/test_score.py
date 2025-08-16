import pytest
from app.services.score import (
    calculate_score_for_attempt,
    penalize_score,
    update_player_score
)
from app.models import Player, GameSession

class TestCalculateScoreForAttempt:
    """
        Tests for the calculate_score_for_attempt function.
    """

    def test_easy_level_scoring(self):
        """
            Test scoring calculation for difficulty level 1 (Easy)
        """
        difficulty_level = 1
        correct_numbers = 2
        correct_positions =1

        score = calculate_score_for_attempt(difficulty_level, correct_numbers, correct_positions)

        # Easy: numbers*600 + positions*12000
        expected_score = (2*600) + (1*1200)
        assert score == expected_score

    
    def test_medium_level_scoring(self):
        """
            Test Scoring calculation for difficulty level 2 (Medium)
        """
        
        difficulty_level = 2
        correct_numbers = 3
        correct_positions = 1

        score = calculate_score_for_attempt(difficulty_level,correct_numbers,correct_positions)

        # Medium: numbers*800 + positions*1600
        expected_score = (3*800) + (1*1600)
        assert score == expected_score

    def test_hard_level_scoring(self):
        """
            Test scoring calculation for difficulty level 3 (Hard)
        """

        difficulty_level = 3
        correct_numbers = 1
        correct_positions = 2

        score = calculate_score_for_attempt(difficulty_level, correct_numbers, correct_positions)

        # Hard: numbers*1200 + positions*2400
        expected_score = (1*1200) + (2*2400)
        assert score == expected_score


class TestPenalizeScore:
    """
        Test for the penalize_score function
    """
    def test_easy_level_penalty(self):
        
        original_score = 1000
        difficulty_level = 1

        penalized_score = penalize_score(difficulty_level,original_score)

        assert penalized_score == original_score - 50 #950

    def test_medium_level_penalty(self):
        """
            Test penalty application for medium level
        """

        original_score = 2000
        difficulty_level = 2

        penalized_score = penalize_score(difficulty_level,original_score)

        assert penalized_score == original_score - 100 #1900

    def test_hard_level_penalty(self):
        """
            Test penalty application for hard level.
        """ 
        original_score = 3000
        difficulty_level = 3

        penalized_score = penalize_score(difficulty_level,original_score)

        assert penalized_score == original_score - 150 


class TestUpdatePlayerScore:
    """
        Tests for the update_player_score function
    """

    def create_test_player(self, initial_score = 0, last_attempt_score = None):

        return Player(
            name = "TestPlayer",
            score=initial_score,
            last_attempt_score= last_attempt_score
        )

    def create_test_game_session(self, difficulty_level =1):
        return GameSession(
            player_id =1,
            secret_number= "1242",
            difficulty_level=difficulty_level,
            attempts_left=10
        )
    
    def test_first_attempt_no_penalty(self):
        """
            Test first attempt should not be penalizad.
        """

        player = self.create_test_player(initial_score=0,last_attempt_score=None)
        session = self.create_test_game_session(difficulty_level=1)

        attempt_score = update_player_score(player, session, 2,1)

        expected_score = (2*600) + (1*1200)
        assert attempt_score == expected_score
        assert player.score == expected_score
        assert player.last_attempt_score == expected_score


    def test_improved_performance_no_penalty(self):
        """
            Test better performance than last attempt should not be penalized.
        """

        player = self.create_test_player(initial_score=1000, last_attempt_score=1500)
        session = self.create_test_game_session(difficulty_level=1)
        
        attempt_score = update_player_score(player, session, 3, 1)
        
        expected_attempt_score = (3 * 600) + (1 * 1200) 
        assert attempt_score == expected_attempt_score 
        assert player.score == 1000 + expected_attempt_score  
        assert player.last_attempt_score == expected_attempt_score



    def test_worse_performance_with_penalty(self):
        """
            Test worse performance than last attempt should be penalized.
        """
     
        player = self.create_test_player(initial_score=5000, last_attempt_score=3000)
        session = self.create_test_game_session(difficulty_level=1)
        
        attempt_score = update_player_score(player, session, 1, 1)
        
        base_score = (1 * 600) + (1 * 1200)  
        expected_penalized_score = base_score - 50  
        
        assert attempt_score == expected_penalized_score
        assert player.score == 5000 + expected_penalized_score  
        assert player.last_attempt_score == expected_penalized_score


    def test_equal_performance_no_penalty(self):
        """
            Test same performance as last attempt should not be penalized.
        """
        
        player = self.create_test_player(initial_score=2000, last_attempt_score=2400)
        session = self.create_test_game_session(difficulty_level=1)
        
        attempt_score = update_player_score(player, session, 2, 1)
        
        expected_score = (2 * 600) + (1 * 1200)  
        assert attempt_score == expected_score  
        assert player.score == 2000 + expected_score 
        assert player.last_attempt_score == expected_score