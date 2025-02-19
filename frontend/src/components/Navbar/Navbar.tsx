import "../../styles/base.css";
import "./Navbar.css";
import logo from "../../assets/images/logo.png";
import { Link } from "react-router-dom";
import { useCart } from "../../context/CartContext";
import { useAuth } from "../../context/AuthContext";

export default function Navbar() {
  const { items } = useCart();
  const { isAuthenticated, isAdmin, logout } = useAuth();
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
            <Link to="/shop" className="nav-link link shop-link">
              SHOP
            </Link>
            <Link to="/cart" className="nav-link link cart-icon-container">
              <i className="fa-solid fa-cart-shopping"></i>
              {items.length > 0 && (
                <span className="cart-count">{items.length}</span>
              )}
            </Link>
            <div className="nav-auth">
              {isAuthenticated ? (
                <>
                  {isAdmin && (
                    <Link to="/admin" className="nav-link">
                      Admin Panel
                    </Link>
                  )}
                  <button onClick={logout} className="nav-link">
                    Logout
                  </button>
                </>
              ) : (
                <Link to="/login" className="nav-link">
                  Login
                </Link>
              )}
            </div>
            {/* <Link to="/login" className="nav-link link login-link">
              Login
            </Link> */}
          </div>
        </div>
      </div>
    </>
  );
}
