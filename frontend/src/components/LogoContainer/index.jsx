import Logo from "../../assets/logo.png";
import "./styles.css";

function LogoContainer() {
  return (
    <div className="logo-container">
      <img id="logo" src={Logo} alt="logo" />
    </div>
  );
}

export default LogoContainer;
