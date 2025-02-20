import "./Video.css";
import { Link } from "react-router-dom";

export default function Video() {
  return (
    <>
      <div className="banner">
        <video className="banner-video" autoPlay muted loop playsInline>
          <source
            src="https://my-app-images44.s3.us-east-2.amazonaws.com/test/videobanner.mp4"
            type="video/mp4"
          />
          Your browser does not support the video tag.
        </video>
        <div className="banner-content">
          <h1>WHERE STYLE TELLS YOUR STORY</h1>

          <p>
            Curate, trade, and celebrate one-of-a-kind finds
            <br />
            from the world’s most coveted designers.
          </p>

          <div className="cta-buttons">
            <Link to="/shop" className="video-banner-button">
              DISCOVER NOW
            </Link>
          </div>
        </div>
      </div>
    </>
  );
}
