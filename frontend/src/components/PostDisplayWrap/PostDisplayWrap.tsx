import React, { useEffect, useState } from "react";
import axios from "axios";
import "./PostDisplayWrap.css";
import { Link } from "react-router-dom";

interface Post {
  title: string;
  first_image_url: string;
  id: number;
  price: number;
}

interface PostDisplayWrapProps {
  filters?: {
    minPrice: string;
    maxPrice: string;
    category: string;
    designer: string;
  };
}

const PostDisplayWrap: React.FC<PostDisplayWrapProps> = ({ filters }) => {
  const [posts, setPosts] = useState<Post[]>([]);

  useEffect(() => {
    // Create query parameters based on filters
    const params = new URLSearchParams();
    if (filters) {
      if (filters.minPrice) params.append("minPrice", filters.minPrice);
      if (filters.maxPrice) params.append("maxPrice", filters.maxPrice);
      if (filters.category !== "all")
        params.append("category", filters.category);
      if (filters.designer !== "all")
        params.append("designer", filters.designer);
    }

    // Fetch filtered data from the backend
    axios
      .get(`http://127.0.0.1:5005/posts/first-image?${params.toString()}`)
      .then((response) => {
        console.log("Fetched filtered posts:", response.data);
        setPosts(response.data);
      })
      .catch((error) => {
        console.error("Error fetching posts:", error);
      });
  }, [filters]); // Re-fetch when filters change

  return (
    <div className="wrap-container">
      <ul className="wrap-track">
        {posts.map((post, index) => (
          <Link to={`/post/${post.id}`} key={index} className="wrap-item">
            <img
              src={post.first_image_url}
              alt={post.title}
              className="wrap-image"
            />{" "}
            <h2 className="itm-title">{post.title}</h2>
            <h2 className="itm-price">${post.price}</h2>
          </Link>
        ))}
        <div className="item-heart-price"></div>
      </ul>
    </div>
  );
};

export default PostDisplayWrap;
