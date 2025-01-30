import { useEffect, useState } from "react";
import axios from "axios";

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
import "../styles/base.css";
import Home from "../pages/Home/Home";
import Navbar from "../components/Navbar/Navbar";
import Bottom from "../components/Bottom/Bottom";
import Cart from "../pages/Cart";
import Shop from "../pages/Shop";
import Brands from "../pages/Brands";
import Post from "../pages/Post/Post";

export default function App() {
  const [message, setMessage] = useState(""); // State to hold data from API

  useEffect(() => {
    // Fetch data from Flask API when the app loads
    axios
      .get("http://127.0.0.1:5000/api/test") // Replace with your Flask endpoint
      .then((response) => {
        console.log("API response:", response.data);
        setMessage(response.data.message); // Store API response in state
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  }, []); // Runs only once when the component mounts

  return (
    <Router>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/brands" element={<Brands />} />
        <Route path="/shop" element={<Shop />} />
        <Route path="/cart" element={<Cart />} />
        <Route path={`/post/:postId`} element={<Post />} />
        {/*<Route path="/products" element={<Products />} />*/}
      </Routes>
      <Bottom />
    </Router>
  );
}
