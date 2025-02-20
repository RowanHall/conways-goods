import "../../styles/base.css";
import "./Bottom.css";
import { Link } from "react-router-dom";

export default function Bottom() {
  // add funtionality to site-links
  return (
    <div className="bottom-banner">
      <div className="bottom-banner-socials">
        <Link
          to="https://www.grailed.com/JapaneseThreads/feedback"
          className="bottom-banner-site-links link-font link"
        >
          REVIEWS
        </Link>
        <Link
          to="https://www.instagram.com/conwaysgoods/"
          className="link-font link"
        >
          INSTAGRAM
        </Link>
        <Link
          to="https://www.grailed.com/JapaneseThreads"
          className="link-font link"
        >
          GRAILED
        </Link>
        <p className="link-font">Conway's Goods © 2024</p>
      </div>
    </div>
  );
}
