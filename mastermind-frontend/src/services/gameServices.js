const API_BASE_URL = "http://localhost:8000/api/v1";

// Helper function for authenticated requests
const apiRequest = async (endpoint, options = {}) => {
  const token = localStorage.getItem("token");

  if (!token) {
    throw new Error("No authentication token found");
  }

  const config = {
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
      ...options.headers,
    },
    ...options,
  };

  const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || "API Error");
  }

  return response.json();
};

export const gameService = {
  // Start game
  startGame: async (difficulty) => {
    return apiRequest(`/game/start_game/?difficulty_level=${difficulty}`, {
      method: "POST",
    });
  },

  // Make guess
  makeGuess: async (sessionId, guessedNumber) => {
    return apiRequest("/game/guess/", {
      method: "POST",
      body: JSON.stringify({
        session_id: sessionId,
        guessed_number: guessedNumber,
      }),
    });
  },

  // Get hint
  getHint: async (sessionId) => {
    return apiRequest("/game/get_ai_hint/", {
      method: "POST",
      body: sessionId,
    });
  },

  // Get leaderboard
  getLeaderboard: async () => {
    return apiRequest("/game/top_players/");
  },
};
