import "../../styles/base.css";
import "./Navbar.css";
import logo from "../../assets/images/logo.png";
import { Link } from "react-router-dom";
import { useCart } from "../../context/CartContext";

export default function Navbar() {
  const { items } = useCart();

  return (
    <>
      <div className="nav-container">
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
            <Link to="/cart" className="nav-link link cart-icon-container">
              <i className="fa-solid fa-cart-shopping"></i>
              {items.length > 0 && (
                <span className="cart-count">{items.length}</span>
              )}
            </Link>
          </div>
        </div>
      </div>
    </>
  );
}
