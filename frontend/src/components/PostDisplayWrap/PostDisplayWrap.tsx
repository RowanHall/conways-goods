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
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const params = new URLSearchParams();

    // Add null check for filters
    if (filters) {
      if (filters.minPrice.trim()) params.append("minPrice", filters.minPrice);
      if (filters.maxPrice.trim()) params.append("maxPrice", filters.maxPrice);
      if (filters.category !== "all")
        params.append("category", filters.category);
      if (filters.designer !== "all")
        params.append("designer", filters.designer);
    }

    axios
      .get(`http://127.0.0.1:5005/posts/first-image?${params.toString()}`)
      .then((response) => {
        if (response.data.error) {
          setError(response.data.error);
          setPosts([]);
        } else {
          setError(null);
          setPosts(response.data);
        }
      })
      .catch((error) => {
        console.error("Error fetching posts:", error);
        setError("Error loading posts. Please try again.");
        setPosts([]);
      });
  }, [filters]);

  if (error) {
    return <div className="error-message">{error}</div>;
  }

  return (
    <div className="wrap-container">
      <ul className="wrap-track">
        {posts.length > 0 ? (
          posts.map((post, index) => (
            <Link to={`/post/${post.id}`} key={index} className="wrap-item">
              <img
                src={post.first_image_url}
                alt={post.title}
                className="wrap-image"
              />
              <h2 className="itm-title">{post.title}</h2>
              <h2 className="itm-price">${post.price}</h2>
            </Link>
          ))
        ) : (
          <div className="no-results">No items found matching your filters</div>
        )}
      </ul>
    </div>
  );
};

export default PostDisplayWrap;
