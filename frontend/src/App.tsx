// import "./App.css";
// import "./base.css";
// import Navbar from "./Navbar";
// import Bottom from "./Bottom";
// import Cart from "./pages/Cart";
// import Shop from "./pages/Shop";
// import Brands from "./pages/Brands";

// export default function App() {
//   let component;
//   switch (window.location.pathname) {
//     case "/":
//       break;
//     case "/brands":
//       component = <Brands />;
//       break;
//     case "/shop":
//       component = <Shop />;
//       break;
//     case "/cart":
//       component = <Cart />;
//   }

//   return (
//     <>
//       <Navbar />
//       {component}
//       <Bottom />
//     </>
//   );
// }
import React, { useEffect, useState } from "react";
import axios from "axios";

import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import "./App.css";
import "./base.css";
import Navbar from "./components/Navbar/Navbar";
import Bottom from "./components/Bottom/Bottom";
import Cart from "./pages/Cart";
import Shop from "./pages/Shop";
import Brands from "./pages/Brands";
import Products from "./components/Products/Products";
import Posts from "./components/Posts/Posts";

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

      {/* Homepage */}
      <Routes>
        <Route path="/brands" element={<Brands />} />
        <Route path="/shop" element={<Shop />} />
        <Route path="/cart" element={<Cart />} />
        {/*<Route path="/products" element={<Products />} />*/}
      </Routes>
      <Posts />
      <Bottom />
    </Router>
  );
}
