const DifficultyOption = ({title,level,description,onClick, isSelected}) =>{
    return(
        <div className={`difficulty-option ${isSelected ? 'selected' : ''}`} onClick={onClick}>            
            <div className="level">              
                <h3 className="dificulty-option-title">Level {level}: {title}</h3>
            </div>
            <div className="difficulty-option-content">
                <p className="difficulty-option-description">{description}</p>
            </div>
            {isSelected && <div className="selected-indicator">✓</div>}
        </div>
    )
}

export default DifficultyOption