import React, { useEffect, useState } from "react";
import axios from "axios";

interface Product {
  name: string;
  price: number;
}

const Products = () => {
  const [products, setProducts] = useState<Product[]>([]); // Define type for products

  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/api/products")
      .then((response) => {
        console.log("Fetched products:", response.data);
        setProducts(response.data); // Assume response.data is an array of Product
      })
      .catch((error) => {
        console.error("Error fetching products:", error);
      });
  }, []);

  return (
    <div>
      <h1>Product List</h1>
      <ul>
        {products.map((product, index) => (
          <li key={index}>
            <strong>{product.name}</strong>: ${Number(product.price).toFixed(2)}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Products;
