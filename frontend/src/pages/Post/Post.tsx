import "./Post.css";
import { useParams } from "react-router-dom";
import React, { useEffect, useState } from "react";
import axios from "axios";

// Define the type for the post data
interface PostData {
  id: number;
  title: string;
  price: number;
  images: string[];
}

function Post() {
  const { postId } = useParams<{ postId: string }>(); // Get post ID from the URL

  const [post, setPost] = useState<PostData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchPost = async () => {
      try {
        const response = await axios.get(
          `http://localhost:5005/api/posts/${postId}`
        );
        setPost(response.data);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchPost();
  }, [postId]);

  if (loading) return <div>Loading...</div>;
  if (error) return <div>Error: {error}</div>;
  if (!post) return <div>No post found</div>;
  return (
    <div className="layout_container">
      <div className="post-container">
        <div className="post-images">
          {post.images && post.images.length > 0 ? (
            post.images.map((image, index) => (
              <img key={index} src={image} alt={`Post image ${index + 1}`} />
            ))
          ) : (
            <p>No images available</p>
          )}
        </div>
        <div className="post-info-container">
          <h1>{post.title}</h1>
          <h1>{post.price}</h1>
        </div>
        {/* Render other post details here */}
      </div>
    </div>
  );
}

export default Post;
