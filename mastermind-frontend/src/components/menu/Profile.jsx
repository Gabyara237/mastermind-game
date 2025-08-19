import { useState, useEffect } from 'react';
import { authService } from '../../services/authService';

const Profile = ({ onBack }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchUserProfile();
  }, []);

  const fetchUserProfile = async () => {
    try {
      setLoading(true);
      setError('');
      
      const userData = await authService.getCurrentUser();
      console.log('User profile data:', userData);
      setUser(userData);
      
    } catch (err) {
      console.error('Error fetching profile:', err);
      setError('Failed to load profile');
    } finally {
      setLoading(false);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    });
  };

  if (loading) {
    return (
      <div className="profile-container">
        <div className="loading-state">
          <h2>👤 Loading Profile...</h2>
          <div className="loading-spinner">⏳</div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="profile-container">
        <div className="error-state">
          <h2>👤 Profile</h2>
          <p className="error-message">{error}</p>
          <button className="retry-button" onClick={fetchUserProfile}>
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
    <div className="profile-container">
      <div className="profile-header">
        <h2>👤 My Profile</h2>
        <p>Your Mastermind account information</p>
      </div>

      <div className="profile-content">
        {/* User Information Card */}
        <div className="profile-card user-info-card">
          <h3>Account Information</h3>
          <div className="info-grid">
            <div className="info-item">
              <span className="info-label">Username: </span>
              <span className="info-value">{user.username}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Email: </span>
              <span className="info-value">{user.email}</span>
            </div>
            <div className="info-item">
              <span className="info-label">Member since: </span>
              <span className="info-value">{formatDate(user.created_at)}</span>
            </div>
          </div>
        </div>

        <div className="profile-card stats-card">
          <h3>Game Statistics</h3>
          <div className="stats-grid">
            <div className="stat-item">
              <div className="stat-info">
                <span className="stat-label">Total Score</span>
                <span className="stat-value">Coming Soon</span>
              </div>
            </div>
            <div className="stat-item">
              <div className="stat-info">
                <span className="stat-label">Games Played</span>
                <span className="stat-value">Coming Soon</span>
              </div>
            </div>
            <div className="stat-item">
              <div className="stat-info">
                <span className="stat-label">Games Won</span>
                <span className="stat-value">Coming Soon</span>
              </div>
            </div>
            <div className="stat-item">
              <div className="stat-info">
                <span className="stat-label">Win Rate</span>
                <span className="stat-value">Coming Soon</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="profile-actions">
        <button className="back-button" onClick={onBack}>
          ← Back to Menu
        </button>
        <button className="refresh-button" onClick={fetchUserProfile}>
          🔄 Refresh
        </button>
      </div>
    </div>
  );
};

export default Profile;