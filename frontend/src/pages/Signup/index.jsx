import { useNavigate } from "react-router-dom";
import "./styles.css";
import LogoContainer from "../../components/LogoContainer";
import HeroImage from "../../components/HeroImage";

function SignupPage() {
  const navigate = useNavigate();

  const handleSignup = () => {
    fetch("http://localhost:8000/accounts/register/", {
      method: "POST",
      body: JSON.stringify({
        username: document.querySelector('input[name="username"]').value,
        email: document.querySelector('input[name="email"]').value,
        password: document.querySelector('input[name="password"]').value,
        password2: document.querySelector('input[name="confirm-password"]')
          .value,
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
        } else if (data.username) {
          throw new Error(data.username[0]);
        }
        navigate("/");
      })
      .catch((error) => {
        alert(error.message || "An error occurred. Please try again.");
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
              <h1>Sign Up</h1>
            </div>
            <div id="description" className="tile">
              <p>Let's get started</p>
            </div>
            <input
              type="text"
              name="username"
              placeholder="Username"
              className="auth-input"
              required
            />
            <input
              type="email"
              name="email"
              placeholder="Email"
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
            <input
              type="password"
              name="confirm-password"
              placeholder="Confirm Password"
              className="auth-input"
              required
            />
            <button id="primary-button" onClick={handleSignup}>
              Register
            </button>
            <div id="bottom-tile" className="tile">
              <p>
                {"Already have an account?" + " "}
                <span onClick={() => navigate("/")}>Login here</span>
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default SignupPage;
