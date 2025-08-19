import MenuOption from "../menu/MenuOption";

const GameMenu = ({onMenuSelect}) => {

    const handlePlayGame = () => {
        onMenuSelect('difficulty'); 
    };

    const handleInstructions = () => {
        onMenuSelect('instructions');
    };

    const handleLeaderboard = () => {
        onMenuSelect('leaderboard');
    };

    const handleProfile = () => {
        onMenuSelect('profile');
    };

    return (
        <div className="game-menu-container">
        
            <div className="menu-options">
                <MenuOption
                title="Play Game"
                description="Start a new Mastermind challenge"
                icon="🎮"
                onClick={() => handlePlayGame()}
                />
                
                <MenuOption
                title="Instructions" 
                description="Learn how to play"
                icon="📖"
                onClick={() => handleInstructions()}
                />
                
                <MenuOption
                title="Leaderboard"
                description="View top 3 players"
                icon="🏆"
                onClick={() => handleLeaderboard()}
                />
                
                <MenuOption
                title="Profile"
                description="View your stats"
                icon="👤"
                onClick={() => handleProfile()}
                />
            </div>
        </div>
    );
};

export default GameMenu