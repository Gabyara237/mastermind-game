const API_BASE_URL = "http://localhost:8000/api/v1";

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

export const authService = {
  // Get current user
  getCurrentUser: async () => {
    return apiRequest("/auth/me");
  },

  // Logout
  logout: () => {
    localStorage.removeItem("token");
  },
};
