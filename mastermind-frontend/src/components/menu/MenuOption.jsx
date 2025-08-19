const MenuOption = ({ title, description, icon, onClick }) => {
  return (
    <div className="menu-option" onClick={onClick}>
      <div className="menu-option-icon">
        {icon}
      </div>
      <div className="menu-option-content">
        <h3 className="menu-option-title">{title}</h3>
        <p className="menu-option-description">{description}</p>
      </div>
    </div>
  );
};

export default MenuOption;