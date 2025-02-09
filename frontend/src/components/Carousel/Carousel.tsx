import React, { useEffect, useState } from "react";
import axios from "axios";
import "./Carousel.css";
import { Link } from "react-router-dom";

interface Post {
  title: string;
  first_image_url: string;
  id: number;
  price: number;
}

const PostsWithImages: React.FC = () => {
  const [posts, setPosts] = useState<Post[]>([]); // State to store fetched posts

  useEffect(() => {
    // Fetch data from the backend
    axios
      .get("http://127.0.0.1:5005/posts/first-image") // Update with your backend endpoint
      .then((response) => {
        console.log("Fetched posts:", response.data);
        setPosts(response.data); // Set the fetched data in state
      })
      .catch((error) => {
        console.error("Error fetching posts:", error);
      });
  }, []);

  return (
    <div className="carousel-container">
      <ul className="carousel-track">
        {posts.map((post, index) => (
          <Link to={`/post/${post.id}`} key={index} className="carousel-item">
            <img
              src={post.first_image_url}
              alt={post.title}
              className="carousel-image"
            />{" "}
            <h2 className="post-title">{post.title}</h2>
            <h2 className="post-price">${post.price}</h2>
          </Link>
        ))}
        <div className="item-heart-price"></div>
      </ul>
    </div>
  );
};

export default PostsWithImages;
