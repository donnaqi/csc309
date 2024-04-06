import Image from "../../assets/hero_image.png";
import "./styles.css";

function HeroImage() {
  return (
    <div className="hero-image-container">
      <img id="hero-image" src={Image} alt="hero-image" />
    </div>
  );
}

export default HeroImage;
