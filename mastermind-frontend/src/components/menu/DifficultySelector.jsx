import { useState } from "react"
import DifficultyOption from "./DifficultyOption"

const DifficultySelector = ({onStartGame,onBack}) =>{
    
    const [selectedDifficulty, setSelectedDificulty] = useState(null);
    
    const handleDifficultySelect= (level) =>{
        setSelectedDificulty(level);
        console.log('Selected difficulty level:', level)
    }

    const handlePlayNow = () =>{
        if(selectedDifficulty){
            onStartGame(selectedDifficulty)
        }else{
            alert('Please select a difficulty level first!')
        }
    }

    return(
        <div className="difficulty-selector-container">
            <h2 className="title-dificulty-option">Select your difficulty level</h2>
            <div className="difficulty-options">
                <DifficultyOption 
                    title = "Easy" 
                    level={1} 
                    description=" Digits from 0 - 5, 12 attempts"
                    onClick={()=> handleDifficultySelect(1)}
                    isSelected = {selectedDifficulty === 1}
                />
                <DifficultyOption 
                    title = "Medium" 
                    level={2} 
                    description="Digits from 0 - 7, 10 attempts"
                    onClick={() => handleDifficultySelect(2)}
                    isSelected = {selectedDifficulty === 2}
                />
                <DifficultyOption 
                    title = "Hard" 
                    level={3} 
                    description="Digits from 0 - 9, 8 attempts"
                    onClick={() => handleDifficultySelect(3)}
                    isSelected = {selectedDifficulty === 3}

                />
            </div>
            <p>Note: for each level the number to guess is of 4 digits</p>
            <div className="difficulty-actions">
                
                <button
                    className="play-button"
                    onClick={handlePlayNow}
                    disabled = {!selectedDifficulty}
                >
                    Play now
                </button>

                <button 
                    className="back-button"
                    onClick={onBack}
                >
                    Back to Menu
                </button>

            </div>
            
        </div>
    )
}

export default DifficultySelector