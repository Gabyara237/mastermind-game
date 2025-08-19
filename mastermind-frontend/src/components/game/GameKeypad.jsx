import { useState } from 'react';
import { gameService } from '../../services/gameServices';

const GameKeypad = ({ 
  gameData, 
  onGuessUpdate, 
  onAttemptMade, 
  disabled,
  currentGuess,
  user
}) => {
  const [loading, setLoading] = useState(false);

  // Configuration according to difficulty
  const getDifficultyConfig = () => {
    switch(gameData.difficulty_level) {
      case 1: return { max: 5, name: 'Easy (0-5)' };
      case 2: return { max: 7, name: 'Medium (0-7)' };
      case 3: return { max: 9, name: 'Hard (0-9)' };
      default: return { max: 9, name: 'Unknown' };
    }
  };

  const config = getDifficultyConfig();

  // Generate keyboard buttons according to difficulty
  const generateKeypadNumbers = () => {
    const numbers = [];
    for (let i = 0; i <= config.max; i++) {
      numbers.push(i);
    }
    return numbers;
  };

  // Manage click on number
  const handleNumberClick = (number) => {
    if (disabled || loading) return;
    onGuessUpdate('add', number.toString());
  };

  // Handle delete
  const handleBackspace = () => {
    if (disabled || loading) return;
    onGuessUpdate('remove');
  };

  // Request hint
  const handleHint = async () => {
    if (disabled || loading) return;
    setLoading(true);
    try {
      const response = await gameService.getHint(gameData.session_id);
      onAttemptMade('hint', response.hint);
    } catch (error) {
      alert('Error getting hint: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  // Submit attempt
  const handleSubmit = async () => {
    if (disabled || loading) return;
    
    // Verify that the guess is complete
    if (!currentGuess || currentGuess.some(digit => digit === '')) {
      alert('Please enter 4 digits before submitting');
      return;
    }
    
    setLoading(true);
    try {
      const guessString = currentGuess.join('');
      const response = await gameService.makeGuess(gameData.session_id, guessString);
      
      // Handle different backend responses
      if (response.result === 'WIN') {
        onAttemptMade('submit', {
          guess: guessString,
          correct_numbers: 4,
          correct_positions: 4,
          game_won: true,
          game_over: false,
          total_score: response.total_score,
          attempts_left: 0,
          message: response.message
        });
      } else if (response.result === 'LOSE') {
        onAttemptMade('submit', {
          guess: guessString,
          correct_numbers: 0,
          correct_positions: 0,
          game_won: false,
          game_over: true,
          total_score: response.total_score,
          attempts_left: 0,
          message: response.message
        });
      } else {
        onAttemptMade('submit', {
          guess: guessString,
          correct_numbers: response.result.correct_numbers,
          correct_positions: response.result.correct_positions,
          game_won: false,
          game_over: false,
          attempts_left: response.attempts_left,
          score_this_attempt: response.score_this_attempt,
          total_score: response.total_score
        });
      }

    } catch (error) {
      console.error('Error making guess:', error);
      alert('Error making guess: ' + error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="game-keypad">
      <div className='good-luck'><p>Good luck {user.username}!</p></div>
      <div className="difficulty-info">
        <h2>Select your four numbers:</h2>
        <p>Difficulty level: {config.name}</p>
      </div>

      {/* Numeric keypad */}
      <div className="keypad">
        {generateKeypadNumbers().map(number => (
          <button
            key={number}
            className="keypad-button"
            onClick={() => handleNumberClick(number)}
            disabled={loading || disabled}
          >
            {number}
          </button>
        ))}
        <button
          className="keypad-button backspace"
          onClick={handleBackspace}
          disabled={loading || disabled}
        >
          ←
        </button>
      </div>

      {/* Action buttons */}
      <div className="action-buttons">
        <button
          className="hint-button"
          onClick={handleHint}
          disabled={loading || disabled}
        >
            {loading ? 'Loading...' : 'HINT'}
        </button>
        <button
          className="submit-button"
          onClick={handleSubmit}
          disabled={loading || disabled || currentGuess.some(digit => digit === '')}
        >
            {loading ? 'Submitting...' : 'SUBMIT'}
        </button>
      </div>
    </div>
  );
};

export default GameKeypad;