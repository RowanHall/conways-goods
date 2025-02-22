import React, { useEffect, useState, useRef } from "react";
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
  const [posts, setPosts] = useState<Post[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [visibleItems, setVisibleItems] = useState(4);
  const carouselRef = useRef<HTMLDivElement>(null);

  // Calculate visible items based on container width
  const calculateVisibleItems = () => {
    if (carouselRef.current) {
      const containerWidth = carouselRef.current.offsetWidth;
      // Assuming each item is ~275px (including padding)
      const itemsVisible = Math.floor(containerWidth / 275);
      setVisibleItems(Math.max(1, itemsVisible));
    }
  };

  useEffect(() => {
    calculateVisibleItems();

    const handleResize = () => {
      calculateVisibleItems();
      setCurrentIndex((prev) => {
        const maxIndex = Math.max(0, posts.length - visibleItems);
        return Math.min(prev, maxIndex);
      });
    };

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, [posts.length, visibleItems]);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:5005/posts/first-image")
      .then((response) => {
        console.log("Fetched posts:", response.data);
        setPosts(response.data);
      })
      .catch((error) => {
        console.error("Error fetching posts:", error);
      });
  }, []);

  const handleNext = () => {
    setCurrentIndex((prev) => {
      const nextIndex = prev + visibleItems;
      const maxIndex = Math.max(0, posts.length - visibleItems);
      return Math.min(nextIndex, maxIndex);
    });
  };

  const handlePrev = () => {
    setCurrentIndex((prev) => {
      const nextIndex = prev - visibleItems;
      return Math.max(0, nextIndex);
    });
  };

  return (
    <div className="carousel-container">
      <h2 className="carousel-title">Related Products</h2>
      <div className="carousel-container" ref={carouselRef}>
        <div className="carousel-items-container">
          {currentIndex > 0 && (
            <button className="carousel-nav-button prev" onClick={handlePrev}>
              &lt;
            </button>
          )}
          <ul
            className="carousel-track"
            style={{
              transform: `translateX(-${currentIndex * (100 / visibleItems)}%)`,
            }}
          >
            {posts.map((post, index) => (
              <Link
                to={`/post/${post.id}`}
                key={index}
                className="carousel-item"
                style={{ width: `${100 / visibleItems}%` }}
              >
                <img
                  src={post.first_image_url}
                  alt={post.title}
                  className="carousel-image"
                />
                <h2 className="post-title">{post.title}</h2>
                <h2 className="post-price">${post.price}</h2>
              </Link>
            ))}
          </ul>

          {currentIndex + visibleItems < posts.length && (
            <button className="carousel-nav-button next" onClick={handleNext}>
              &gt;
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default PostsWithImages;
