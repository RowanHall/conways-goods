import "../../styles/base.css";
import "./Navbar.css";
import logo from "../../assets/images/logo.png";
import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <>
      <header className="header">
        <div className="logo-container">
          <Link to="/" className="site-name">
            <img src={logo} alt="Conway's Goods" className="logo"></img>
          </Link>
        </div>
      </header>
      <div className="navbar-div">
        <div className="nav-link-container">
          <Link to="/brands" className="nav-link link">
            BRANDS
          </Link>
          <Link to="/shop" className="nav-link link">
            SHOP
          </Link>
          <Link to="/cart" className="nav-link link">
            <i className="fa-solid fa-cart-shopping"></i>
          </Link>
        </div>
      </div>
    </>
  );
}
