import "./Post.css";
import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import Carousel from "../../components/Carousel/Carousel";
import { useCart } from "../../context/CartContext";
import DeletePost from "../../components/DeletePost/DeletePost";
import { useAuth } from "../../context/AuthContext";

const API_BASE_URL = import.meta.env.VITE_BACKEND_URL;
// Define the type for the post data
interface PostData {
  id: number;
  title: string;
  price: number;
  description: string;
  images: string[];
  userId: number;
}

function Post() {
  const { addToCart } = useCart();
  const { postId } = useParams<{ postId: string }>(); // Get post ID from the URL
  const { isAuthenticated } = useAuth();
  const [currentUserId, setCurrentUserId] = useState<number | null>(null);

  const [post, setPost] = useState<PostData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0); // Track the current image index

  useEffect(() => {
    const fetchPost = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/api/posts/${postId}`);
        setPost(response.data);
      } catch (error) {
        if (error instanceof Error) {
          setError(error.message);
        } else {
          setError("An unknown error occurred");
        }
      } finally {
        setLoading(false);
      }
    };

    fetchPost();
  }, [postId]);

  useEffect(() => {
    // Fetch current user ID if authenticated
    if (isAuthenticated) {
      axios
        .get(`${API_BASE_URL}/api/me`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        })
        .then((response) => {
          setCurrentUserId(response.data.id);
        })
        .catch((error) => {
          console.error("Error fetching user:", error);
        });
    }
  }, [isAuthenticated]);

  // Handle Next button click
  const handleNext = () => {
    if (post && post.images.length > 0) {
      setCurrentIndex((prevIndex) => (prevIndex + 1) % post.images.length);
    }
  };

  // Handle Previous button click
  const handlePrev = () => {
    if (post && post.images.length > 0) {
      setCurrentIndex(
        (prevIndex) => (prevIndex - 1 + post.images.length) % post.images.length
      );
    }
  };

  // Handle thumbnail click
  const handleThumbnailClick = (index: number) => {
    setCurrentIndex(index);
  };

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!post) return <div>No post found</div>;

  return (
    <div className="layout_container">
      <div className="post-container">
        <div className="post-images">
          {post.images && post.images.length > 0 ? (
            <>
              <div className="post-images-button-inner">
                <button className="prev-button" onClick={handlePrev}>
                  &lt;
                </button>
                {/* Main Image Display */}
                <img
                  key={currentIndex}
                  src={post.images[currentIndex]}
                  alt={`Post image ${currentIndex + 1}`}
                  className="main-image"
                />

                <button className="next-button" onClick={handleNext}>
                  &gt;
                </button>
              </div>

              {/* Thumbnail Image Previews */}
              <div className="thumbnail-container">
                {post.images.map((image, index) => (
                  <img
                    key={index}
                    src={image}
                    alt={`Thumbnail ${index + 1}`}
                    className={`thumbnail ${
                      index === currentIndex ? "active-thumbnail" : ""
                    }`}
                    onClick={() => handleThumbnailClick(index)}
                  />
                ))}
              </div>
            </>
          ) : (
            <p>No images available</p>
          )}
        </div>

        <div className="post-info-container">
          <div className="post-info-container-inner">
            <h2 className="title">{post.title}</h2>
            <h2 className="price">${post.price} CAD</h2>

            <button
              className="add-to-cart-button"
              onClick={() =>
                addToCart({
                  id: post.id,
                  title: post.title,
                  price: post.price,
                  image: post.images[0],
                })
              }
            >
              ADD TO CART
            </button>
            <a
              href="https://www.instagram.com/direct/t/17842351421346689"
              className="message-seller-button"
            >
              MESSAGE SELLER
            </a>
            {currentUserId === post.userId && <DeletePost postId={post.id} />}
            <p className="description">{post.description}</p>
          </div>
        </div>
      </div>
      <Carousel />
    </div>
  );
}

export default Post;
