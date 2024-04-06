import { useNavigate } from "react-router-dom";
import HeroImage from "../../components/HeroImage";
import LogoContainer from "../../components/LogoContainer";
import "./styles.css";

function LoginPage() {
  const navigate = useNavigate();

  const handleLogin = () => {
    fetch("http://localhost:8000/accounts/api/login/", {
      method: "POST",
      body: JSON.stringify({
        username: document.querySelector('input[name="username"]').value,
        password: document.querySelector('input[name="password"]').value,
      }),
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        if (data.error) {
          throw new Error(data.error);
        }
        localStorage.setItem("token", data.access);
        localStorage.setItem("username", data.username);
        navigate("/event");
      })
      .catch((error) => {
        alert(
          error.message ||
            "Your usernmae or password is incorrect. Please try again."
        );
      });
  };

  return (
    <div className="outer-container">
      <LogoContainer />
      <div className="main-content">
        <HeroImage />
        <div className="auth-card-container">
          <div className="auth-card">
            <div id="title" className="tile">
              <h1>Login</h1>
            </div>
            <div id="description" className="tile">
              <p>Welcome back! Please enter your details</p>
            </div>
            <input
              type="username"
              name="username"
              placeholder="Username"
              className="auth-input"
              required
            />
            <input
              type="password"
              name="password"
              placeholder="Password"
              className="auth-input"
              required
            />
            <button id="primary-button" onClick={handleLogin}>
              Login
            </button>
            <div id="bottom-tile" className="tile">
              <p>
                {"Don't have an account?" + " "}
                <span onClick={() => navigate("/signup")}>
                  Sign up for free
                </span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default LoginPage;
