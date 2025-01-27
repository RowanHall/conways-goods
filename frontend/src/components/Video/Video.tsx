import "./Video.css";
import { Link } from "react-router-dom";

export default function Video() {
  return (
    <>
      <div className="banner">
        <video className="banner-video">
          {/* autoplay muted loop playsinline */}
          <source
            src="https://my-app-images44.s3.us-east-2.amazonaws.com/test/videobanner.mp4"
            type="video/mp4"
          />
          Your browser does not support the video tag.
        </video>
        <div className="banner-content">
          <h1>THE PLATFORM FOR PERSONAL STYLE</h1>
          <p>
            Buy, sell, discover authenticated pieces from the world's top
            brands.
          </p>
          <div className="cta-buttons">
            <button>Shop Menswear</button>
            <button>Shop Womenswear</button>
          </div>
        </div>
      </div>
    </>
  );
}
