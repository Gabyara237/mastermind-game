import { useEffect, useState } from 'react';
import GameMenu from '../components/game/GameMenu';
import DifficultySelector from '../components/menu/DifficultySelector';
import { authService } from '../services/authService';
import { gameService } from '../services/gameServices'; 
import Instructions from '../components/menu/Instructions';
import Leaderboard from '../components/menu/Leaderboard';
import Profile from '../components/menu/Profile';
import GameDisplay from '../components/game/GameDisplay';
import GameKeypad from '../components/game/GameKeypad';

const GameDashboard = () => {
    const [currentView, setCurrentView] = useState('menu');
    const [gameData, setGameData] = useState(null);
    const [user, setUser] = useState(null); 

     // Game states
    const [currentGuess, setCurrentGuess] = useState(['', '', '', '']);
    const [attempts, setAttempts] = useState([]);
    const [hint, setHint] = useState('');
    const [gameStatus, setGameStatus] = useState('playing'); // 'playing', 'won', 'lost'

    const [attemptsLeft, setAttemptsLeft] = useState(null);
    const [totalScore, setTotalScore] = useState(0);

    useEffect(() => {
        fetchUser();
    }, []);

    const fetchUser = async () => {
        try {
            const userData = await authService.getCurrentUser();
            setUser(userData);
        } catch (error) {
            console.error('Error fetching user:', error);
        }
    };
    // Function to change views
    const handleMenuSelect = (view) => {
        setCurrentView(view);
        console.log('Cambiando a vista:', view); 
    };

    const handleStartGame = async (difficulty) => {
        try {
            console.log('Starting game with difficulty:', difficulty);
            console.log('Current user score:', user?.score); 
            
            const response = await gameService.startGame(difficulty);
            console.log('Game started successfully:', response);
            
            const gameData = {
                ...response,
                difficulty_level: difficulty 
            };
            
            setGameData(gameData);
            setAttemptsLeft(gameData.attempts_left);
            
            setTotalScore(user?.score || 0);
            console.log('Setting totalScore to:', user?.score || 0); 
            
            setCurrentView('game');
        
        } catch (error) {
            console.error('Error starting game:', error);
            alert('Error starting game: ' + error.message);
        }
    };

    
    //  Manage guess updates from the keypad
    const handleGuessUpdate = (action, value) => {
        if (action === 'add') {
            const nextEmptyIndex = currentGuess.findIndex(digit => digit === '');
            if (nextEmptyIndex !== -1) {
                const newGuess = [...currentGuess];
                newGuess[nextEmptyIndex] = value;
                setCurrentGuess(newGuess);
            }
        } else if (action === 'remove') {
            const lastFilledIndex = currentGuess.map(digit => digit !== '').lastIndexOf(true);
            if (lastFilledIndex !== -1) {
                const newGuess = [...currentGuess];
                newGuess[lastFilledIndex] = '';
                setCurrentGuess(newGuess);
            }
        }
    };

    // Handling keypad actions (hint, submit)
    const handleAttemptMade = (action, data) => {
        if (action === 'hint') {
            setHint(data);
        } else if (action === 'submit') {
            // Add attempt to history
            const newAttempt = {
                guess: data.guess,
                correct_numbers: data.correct_numbers,
                correct_positions: data.correct_positions,
                score_this_attempt: data.score_this_attempt 
            };
            setAttempts(prev => [...prev, newAttempt]);

            // Update attempts and score
            if (data.attempts_left !== undefined) {
                setAttemptsLeft(data.attempts_left);
            }
            if (data.total_score !== undefined) {
                setTotalScore(data.total_score);
            }

            // Check game status
            if (data.game_won) {
                setGameStatus('won');
            } else if (data.game_over) {
                setGameStatus('lost');
            }

            // Clear current attempt and hint
            setCurrentGuess(['', '', '', '']);
            setHint('');
        } else if (action === 'requestSubmit') {
            // Check if you can submit
            const canSubmit = currentGuess.every(digit => digit !== '');
            if (canSubmit) {
                return true;
            }
            return false;
        }
    };

    // Function to end game and return to menu
    const handleGameEnd = async () => {
        const freshUserData = await authService.getCurrentUser();
        
        setCurrentView('menu');
        setGameData(null);
        setCurrentGuess(['', '', '', '']);
        setAttempts([]);
        setHint('');
        setGameStatus('playing');
        setAttemptsLeft(null);
        
        setTotalScore(freshUserData?.score || 0);
        setUser(freshUserData);
    };

        // Function to render the LEFT side content
    const renderLeftContent = () => {
        if (currentView === 'game' && gameData) {
            return (
                <GameKeypad
                    gameData={gameData}
                    onGuessUpdate={handleGuessUpdate}
                    onAttemptMade={handleAttemptMade}
                    disabled={gameStatus !== 'playing'}
                    currentGuess= {currentGuess}
                    user={user}
                    
                />
            );
        }
        return <GameMenu onMenuSelect={handleMenuSelect} />;
    };
  
    // Function to render the content of the right side
    const renderRightContent = () => {
        switch(currentView) {
            case 'difficulty':
                return (
                    <DifficultySelector
                        onStartGame={handleStartGame}
                        onBack={() => setCurrentView('menu')}
                    />
                )
            case 'game':
                return  gameData ? (
                    <GameDisplay
                        currentGuess={currentGuess}
                        attempts={attempts}
                        hint={hint}
                        gameStatus={gameStatus}
                        onGameEnd={handleGameEnd}
                        gameData={gameData}
                        user={user}
                        attemptsLeft={attemptsLeft}  
                        totalScore={totalScore}  
                    />
                ) : (
                    <div>Loading game...</div>
                );
                
            case 'instructions':
                return <Instructions onBack={() => setCurrentView('menu') }/>;
            
            case 'leaderboard':
                return <Leaderboard onBack={() => setCurrentView('menu') }/>;
            
            case 'profile':
                return <Profile onBack={() => setCurrentView('menu') }/>;
            
            default:
                return (
                <div className="welcome-content">
                    {user && (
                    <h3 className="welcome-user">Hello, {user.username}! 👋</h3>
                    )}        
                    <h2>🎯 Welcome to Mastermind!</h2>
                    <p>Select an option from the menu to get started.</p>
                </div>
                );
        }
    };

    return (
        <div className="game-dashboard">
            <div className='dashboard-card'>
                <div className="dashboard-left">
                     {renderLeftContent()}
                </div>
                
                <div className="dashboard-right">
                    {renderRightContent()}
                </div>
            </div>
        </div>
    );
};

export default GameDashboard;