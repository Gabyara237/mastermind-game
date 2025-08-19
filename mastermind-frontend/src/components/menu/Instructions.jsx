const Instructions = ({ onBack }) => {
  return (
    <div className="instructions-container">
      <div className="instructions-header">
        <h2>📖 How to Play Mastermind</h2>
      </div>
      
      <div className="instructions-content">
        <div className="scroll-instructions">
          <div className="item">
            <p>
              <strong>Mastermind</strong> is a guessing game where you must decipher a 
              <span className="highlight"> 4-digit number</span> to achieve victory.
            </p>
            
            <p>
              With each attempt you make to guess the number, you will receive 
              <span className="highlight"> feedback</span> to help you perfect your next attempt.
            </p>
            
            <p>
              The game continues until you <span className="highlight">guess the correct code</span> or 
              <span className="highlight"> exhaust all your attempts</span>.
            </p>
          </div>

          <div className="game-example">
            <h4>Feedback Guide:</h4>
            <div className="feedback-examples">
              <div className="item">
                <span>Correct number in correct position</span>
              </div>
              <div className="item">

                <span>Correct number in wrong position</span>
              </div>
            </div>
          </div>
          <div className="difficulty-info">
              <h4>Difficulty Levels:</h4>
              <p className="item"><strong>Easy:</strong> Digits 0-5, 12 attempts<br/>
              <strong>Medium:</strong> Digits 0-7, 10 attempts<br/>
              <strong>Hard:</strong> Digits 0-9, 8 attempts</p>
      
          </div>
          
          <div className="scoring-system">
            <h4>Scoring System</h4>
            <p className="item">
              <strong>Points per Correct Number:</strong><br/>
              Easy: 600 pts | Medium: 800 pts | Hard: 1,200 pts<br/>
              <strong>Points per Correct Position:</strong><br/>
              Easy: 1,200 pts | Medium: 1,600 pts | Hard: 2,400 pts
            </p>

          </div>

          <div className="scoring-system">
            <h4>Penalty System:</h4>
            <p className="item">If your current attempt scores lower than your previous attempt, a penalty will be applied:<br/>
            Easy: -50 pts | Medium: -100 pts | Hard: -150 pts</p>
          </div>
          <div className="scoring-system">
            <h4>AI-Powered Hints:</h4>
            <p className="item">
              Get intelligent hints to help you crack the code! Our AI analyzes your previous attempts and provides strategic guidance to improve your next guess. Use hints wisely to avoid costly penalties and maximize your score.</p>
          </div>

        </div>
        <div className="instructions-footer">
          <p className="good-luck2">
            ✨ Now let's <strong>PLAY</strong> and <strong>GOOD LUCK</strong>! ✨
          </p>
        </div>
      </div>

      <div className="instructions-actions">
        <button className="back-button" onClick={onBack}>
          ← Back to Menu
        </button>
      </div>
    </div>
  );
};

export default Instructions;