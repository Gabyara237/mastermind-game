
const GameDisplay = ({ currentGuess, attempts, hint, gameStatus, onGameEnd, gameData, user,attemptsLeft,
  totalScore  }) => {

  // Render attempt feedback
  const renderAttemptFeedback = (attempt) => {
    return (
      <div className="attempt-feedback-text">
        <span className="feedback-positions">
            CP:  {attempt.correct_positions}
        </span>
        <span className="feedback-separator"> | </span>
        <span className="feedback-numbers">
            CN: {attempt.correct_numbers}
        </span>
        {attempt.score_this_attempt && (
                <>
                    <span className="feedback-separator"> | </span>
                    <span className="feedback-score">
                        +{attempt.score_this_attempt} pts
                    </span>
                </>
            )}
      </div>
    );
  };

  return (
    <div className="game-display">
        <div>
            <div className='margin: 40px 0 30px 0;'>
                <h2>🎮 Game Started!</h2>
                <div className='game-data-container'>
                    <p>
                      <strong>Attempts left: </strong> 
                      <span className={attemptsLeft <= 3 ? 'low-attempts' : ''}>
                         {attemptsLeft || 0} 
                      </span>
                    </p>
                    <p><strong>Difficulty level:</strong> {
                        gameData.difficulty_level === 1 ? 'Easy' :
                        gameData.difficulty_level === 2 ? 'Medium' :
                        gameData.difficulty_level === 3 ? 'Hard' :'Unknown'
                    }</p>
                    <p><strong>Total Score:</strong> {totalScore || user?.score || 0}</p>
                </div>         
            </div>
        </div>
        
        {/* Current number */}
        <div className="current-guess">
            <h3>Current guess:</h3>
            <div className="guess-display">
            {currentGuess.map((digit, index) => (
                <div key={index} className="digit-box">
                {digit || '_'}
                </div>
            ))}
            </div>
        </div>

        {/* Hint area - Only appears if there is a hint. */}
        {hint && (
            <div className="hint-area">
            <h4>💡 Hint:</h4>
            <p>{hint}</p>
            </div>
        )}

        {/* History of attempts */}
        <div className="attempts-history">
            <h3>📝 Previous attempts:<br/><span className="definition">(Correct Position= CP, Correct Numbers= CN)</span></h3>
            {attempts.length === 0 ? (
            <p className="no-attempts">No attempts yet. Make your first guess!</p>
            ) : (
            <div className="attempts-list">
                {attempts.map((attempt, index) => (
                <div key={index} className="attempt-item">
                    <span className="attempt-guess">{attempt.guess}</span>
                    <span className="attempt-arrow">→</span>
                    {renderAttemptFeedback(attempt)}
                </div>
                ))}
            </div>
            )}
        </div>

        {/* Game Status */}
        {gameStatus === 'won' && (
            <div className="game-status win">
            <h2>🎉 Congratulations! You won!</h2>
            <button onClick={onGameEnd}>Play Again</button>
            </div>
        )}

        {gameStatus === 'lost' && (
            <div className="game-status lose">
            <h2>😞 Game Over! Better luck next time!</h2>
            <button onClick={onGameEnd}>Try Again</button>
            </div>
        )}
    </div>
  );
};

export default GameDisplay;