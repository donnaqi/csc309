import "./styles.css";
import Logo from "../../assets/logo.png";
import { useNavigate } from "react-router-dom";

function Menu({ activeIndex }) {
  const navigate = useNavigate();
  const username = localStorage.getItem("username");

  return (
    <header>
      <div className="menu-wrapper">
        <img className="logo" src={Logo} alt="logo" />

        <div className="menu-items">
          <div
            onClick={() => {
              navigate("/event");
            }}
            className={`menu-item ${activeIndex === 0 ? "active-menu" : ""}`}
          >
            Events
          </div>
          <div
            onClick={() => {
              navigate("/calendar");
            }}
            className={`menu-item ${activeIndex === 1 ? "active-menu" : ""}`}
          >
            Scheduling
          </div>
          <div
            onClick={() => {
              navigate("/contact");
            }}
            className={`menu-item ${activeIndex === 2 ? "active-menu" : ""}`}
          >
            Contacts
          </div>
        </div>

        <div className="profile-picture">
          <div className="background">
            <p>{(username?.toUpperCase() || 'Default')[0]}</p>
          </div>
        </div>
      </div>
    </header>
  );
}

export default Menu;
