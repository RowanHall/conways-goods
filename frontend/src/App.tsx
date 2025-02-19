import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import ProtectedRoute from "./components/ProtectedRoute/ProtectedRoute";
import AdminPanel from "./components/AdminPanel/AdminPanel";
import Login from "./components/Login/Login";

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
    <AuthProvider>
      <CartProvider>
        <Router>
          <Navbar />
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/shop" element={<Shop />} />
            <Route path="/cart" element={<Cart />} />
            <Route path={`/post/:postId`} element={<Post />} />
            <Route path="/login" element={<Login />} />
            <Route
              path="/admin"
              element={
                <ProtectedRoute requireAdmin={true}>
                  <AdminPanel />
                </ProtectedRoute>
              }
            />
          </Routes>
          <Bottom />
        </Router>
      </CartProvider>
    </AuthProvider>
  );
}
