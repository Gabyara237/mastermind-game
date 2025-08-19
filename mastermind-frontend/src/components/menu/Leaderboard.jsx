import { useState, useEffect } from 'react';
import { gameService } from '../../services/gameServices';

const Leaderboard = ({ onBack }) => {
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  const fetchLeaderboard = async () => {
    try {
      setLoading(true);
      setError('');
      
      const data = await gameService.getLeaderboard();
      console.log('Leaderboard data:', data);
      
      setPlayers(data.top_players || []);
      
    } catch (err) {
      console.error('Error fetching leaderboard:', err);
      setError('Failed to load leaderboard');
    } finally {
      setLoading(false);
    }
  };

  const getRankClass = (index) => {
    const classes = ['first-place', 'second-place', 'third-place'];
    return classes[index] || 'other-place';
  };

  if (loading) {
    return (
      <div className="leaderboard-container">
        <div className="loading-state">
          <h2>🏆 Loading Top Players...</h2>
          <div className="loading-spinner">⏳</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="leaderboard-container">
        <div className="error-state">
          <h2>🏆 Leaderboard</h2>
          <p className="error-message">{error}</p>
          <button className="retry-button" onClick={fetchLeaderboard}>
            🔄 Try Again
          </button>
          <button className="back-button" onClick={onBack}>
            ← Back to Menu
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="leaderboard-container">
      <div className="leaderboard-header">
        <h2>🏆 Top 3 Players</h2>
        <p>The best Mastermind players</p>
      </div>

      <div className="leaderboard-content">
        {players.length === 0 ? (
          <div className="empty-leaderboard">
            <p>🎮 No players yet!</p>
            <p>Be the first to play and claim the crown!</p>
          </div>
        ) : (
          <div className="players-list">
            {players.map((player, index) => (
              <div key={player.id} className={`player-card ${getRankClass(index)}`}>
                <div className="player-rank">
                    <div>
                    <span className="rank-number">#{index + 1}</span>
                    </div>

                    <div className="player-badge">
                        {index === 0 && <span className="champion-badge">Champion</span>}
                        {index === 1 && <span className="runner-up-badge">Runner-up</span>}
                        {index === 2 && <span className="third-badge">3rd Place</span>}
                </div>
                </div>
                
                <div className="player-info">
                    <h3 className="player-name">{player.user?.username || `Player ${player.user_id}`}</h3>
                    <div className="player-stats">
                        <span className="score">🎯 {player.score} points</span>
                    </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="leaderboard-actions">
        <button className="back-button" onClick={onBack}>
          ← Back to Menu
        </button>
      </div>
    </div>
  );
};

export default Leaderboard;