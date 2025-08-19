import { useState, useEffect } from 'react';
import GameDashboard from "./pages/GameDashboard"
import Welcome from "./pages/welcome"
import { authService } from './services/authService'; // Ajusta la ruta según tu estructura

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const user = await authService.getCurrentUser();
      setIsAuthenticated(!!user);
    } catch (error) {
      setIsAuthenticated(false);
      console.log("error",error)
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = () => {
    setIsAuthenticated(true);
  };


  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <>
      {isAuthenticated ? (
        <GameDashboard />
      ) : (
        <Welcome onLogin={handleLogin} />
      )}
    </>
  );
}

export default App;