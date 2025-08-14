"""
 Tests for CRUD functions
 Each test checks a specific function of the crud.py file
"""
import pytest
from sqlmodel import Session, SQLModel, create_engine, select
from sqlalchemy.pool import StaticPool
from app.database.crud import(
    get_player_by_name,
    create_game_attempt,
    create_game_session,
    update_game_session,
    get_top_players
)
from app.models import Player, GameAttempt, GameSession

#=======================================
# Functions that prepare data for test
#=======================================

@pytest.fixture(scope="function")
def test_session():
    """
        Fixture that creates an in memory database for each test.
        It is exacuted before each test and cleaned up afterwards.  
    """

    # Create engine in memory
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass= StaticPool,
    )

    # Create all the tables
    SQLModel.metadata.create_all(engine)

    # Create session
    with Session(engine) as session:
        yield session


@pytest.fixture
def sample_player(test_session):
    """ 
        Fixture that creates a test player 
    """

    player = Player(name="TestPlayer", score=100)
    test_session.add(player)
    test_session.commit()
    test_session.refresh(player)
    return player

@pytest.fixture
def sample_game_session(test_session, sample_player):
    """
        Fixture that creates a sample game session 
    """
    game_session = GameSession(
        player_id= sample_player.id,
        secret_number="1234",
        difficulty_level=1,
        attempts_left=10
    )
    test_session.add(game_session)
    test_session.commit()
    test_session.refresh(game_session)
    return game_session


#=======================================
# TESTS FOR get_player_by_name()
#=======================================

class TestGetPlayerByName:
    """
        Test class grouping all tests related to
        get_player_by_name()
    """

    def test_create_new_player(self, test_session):
        """
            Test that verifies that a new player is created when
            it does not exist
        """
        player_name = "Gabriela"

        player= get_player_by_name(test_session, player_name)

        # Verify that the result is correct
        assert player.name == player_name
        assert player.score == 0
        assert player.id is not None

        # Verify that it was actually saved in the database
        saved_player = test_session.get(Player,player.id)
        assert saved_player is not None
        assert saved_player.name == player_name


    def test_get_existing_player(self, test_session):
        """
            Test that verifies that the function does NOT CREATE DUPLICATES
        """

        player_name = "RegisteredPlayer"
        player = get_player_by_name(test_session,player_name)

        retrieved_player = get_player_by_name(test_session,player_name)
        
        # Verify that they are the same object
        assert retrieved_player is player
        
        count = len(test_session.exec(select(Player).where(Player.name==player_name)).all())
        assert count == 1
  

#=======================================
# TESTS FOR create_game_session()
#=======================================

class TestCreateGameSession:
    """
        Test class grouping all tests related to
        create_game_session()
    """
    def test_create_valid_game_session(self, test_session,sample_player):
        """
            Test that verifis if create a game session with valid data
        """

        secret_number ="5678"
        dificulty_level = 2
        attempts_left =8

        game_session = create_game_session(
            test_session,
            sample_player.id,
            secret_number,
            dificulty_level,
            attempts_left
        )

        assert game_session.id is not None
        assert game_session.player_id == sample_player.id
        assert game_session.secret_number == secret_number
        assert game_session.difficulty_level == dificulty_level
        assert game_session.attempts_left == attempts_left

        assert game_session.is_active is True


#=======================================
# TESTS FOR create_game_attempt()
#=======================================

class TestCreateGameAttempt:
    """
        Test class grouping all tests related to
        create_game_attempt()
    """
    def test_create_valid_attempt(self, test_session, sample_game_session):
        """
            Test that verifies if create a valid attempt
        """
        # Data of the attempt 
        guessed_number = "4323"
        correct_numbers = 2
        correct_positions = 1

        # Create attempt
        attempt = create_game_attempt(
            test_session,
            sample_game_session.id,
            guessed_number,
            correct_numbers,
            correct_positions
        )

        # Verify all the fields
        assert attempt.id is not None
        assert attempt.game_session_id == sample_game_session.id
        assert attempt.guessed_number == guessed_number
        assert attempt.correct_numbers == correct_numbers
        assert attempt.correct_positions == correct_positions

#=======================================
# TESTS FOR update_game_session()
#=======================================

class TestUpdateGameSession:
    """
        Test class grouping all tests related to
        update_game_session()
    """

    def test_update_attempts_left(self, test_session, sample_game_session):
        """
            Test that verifies that the changes are persisted in the DB
        """
        # Modify the session
        original_attempts = sample_game_session.attempts_left
        sample_game_session.attempts_left = original_attempts -1

        # Update in the DB
        updated_session = update_game_session(test_session,sample_game_session)

        assert updated_session.attempts_left == original_attempts - 1


    def test_update_is_active_status(self, test_session,sample_game_session):
        """
            Test that verifies changes in is_active status
        """

        # Change status
        sample_game_session.is_active = False

        updated_session = update_game_session(test_session, sample_game_session)

        assert updated_session.is_active is False


#=======================================
# TESTS FOR get_top_players()
#=======================================

class TestGetTopPlayers:
    """
        Test class grouping all tests related to
        get_top_players()
    """

    def test_get_top_players_empty_db(self, test_session):
        """
            Test that verifies that it works correctly with empty BD
        """

        top_players = get_top_players(test_session)

        assert len(top_players)==0
        assert isinstance(top_players, list)

    def test_get_top_players_les_that_three(self, test_session):
        """
            Test that verifies tha it works correctly with little data
        """
        player1 = Player(name="Player1", score = 130)
        player2 = Player(name="Player2", score = 240)
    
        test_session.add_all([player1,player2])
        test_session.commit()

        top_player= get_top_players(test_session)

        assert len(top_player)==2
        assert top_player[0].name == "Player2"
        assert top_player[0].score == 240
        assert top_player[1].name == "Player1"
        assert top_player[1].score == 130

    def test_get_top_players_exactly_three(self, test_session):
        """
            Test that verifies that it works correctly with exactly 3 top players
        """

        player1 = Player(name="Player1", score = 130)
        player2 = Player(name="Player2", score = 240)
        player3 = Player(name="Player3", score = 90)
        
        test_session.add_all([player1,player2,player3])
        test_session.commit()

        top_players= get_top_players(test_session)

        assert len(top_players)==3
        assert top_players[0].name == "Player2"
        assert top_players[0].score == 240
        assert top_players[1].name == "Player1"
        assert top_players[1].score == 130
        assert top_players[2].name == "Player3"
        assert top_players[2].score == 90

    def test_get_top_players_more_than_three(self, test_session):
        """
            Test that verifies that only the best 3 are obtained when there are 
            more players
        """
        player1 = Player(name="Player1", score = 130)
        player2 = Player(name="Player2", score = 240)
        player3 = Player(name="Player3", score = 90)
        player4 = Player(name="Player4", score = 540)
        player5 = Player(name="Player5", score = 149)

        test_session.add_all([player1,player2,player3,player4,player5])
        test_session.commit()

        top_player= get_top_players(test_session)

        assert len(top_player)==3
        assert top_player[0].name == "Player4"
        assert top_player[0].score == 540
        assert top_player[1].name == "Player2"
        assert top_player[1].score == 240
        assert top_player[2].name == "Player5"
        assert top_player[2].score == 149
