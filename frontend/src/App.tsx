import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import "./styles/base.css";
import Home from "./pages/Home/Home";
import Navbar from "./components/Navbar/Navbar";
import Bottom from "./components/Bottom/Bottom";
import Cart from "./pages/Cart/Cart";
import Shop from "./pages/Shop/Shop";
import Post from "./pages/Post/Post";
import { CartProvider } from "./context/CartContext";

export default function App() {
  return (
    <CartProvider>
      <Router>
        <Navbar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/shop" element={<Shop />} />
          <Route path="/cart" element={<Cart />} />
          <Route path={`/post/:postId`} element={<Post />} />
        </Routes>
        <Bottom />
      </Router>
    </CartProvider>
  );
}
