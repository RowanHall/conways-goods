import React, { useEffect, useState } from "react";
import axios from "axios";
import "./Posts.css";

interface Post {
  title: string;
  first_image_url: string;
}

const PostsWithImages: React.FC = () => {
  const [posts, setPosts] = useState<Post[]>([]); // State to store fetched posts

  useEffect(() => {
    // Fetch data from the backend
    axios
      .get("http://127.0.0.1:5000/posts/first-image") // Update with your backend endpoint
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
      <h2 className="sub-title">Featured</h2>

      <div className="carousel-items-container">
        <div className="button-container">
          <button className="prev">Prev</button>
        </div>
        <div className="carousel-items-padding">
          <ul className="carousel-track">
            {posts.map((post, index) => (
              <li key={index} className="carousel-item">
                <img
                  src={post.first_image_url}
                  alt={post.title}
                  className="carousel-image"
                  style={{}}
                />{" "}
                <h2 className="post-title">{post.title}</h2>
                <h2 className="post-price">${post.price}</h2>
              </li>
            ))}
            <div className="item-heart-price"></div>
          </ul>
        </div>
        <div className="button-container">
          <button className="next">Next</button>
        </div>
      </div>
    </div>
  );
};

export default PostsWithImages;

{
  /* <div>
  <h1>Shop</h1>
  <div className="carousel">
    <button className="prev">←</button>
    <div className="carousel-track-container">
      <ul className="carousel-track">
        {posts.map((post, index) => (
          <li key={index} className="carousel-item">
            <h2>{post.title}</h2>
            <img
              src={post.first_image_url}
              alt={post.title}
              style={{
                maxWidth: "300px",
                border: "1px solid #ccc",
                borderRadius: "5px",
                padding: "5px",
              }}
            />
          </li>
        ))}
      </ul>
    </div>
    <button className="next">→</button>
  </div>
</div>  */
}
