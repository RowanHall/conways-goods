// import React, { useEffect, useState } from "react";
// import axios from "axios";

// function PostsWithImages() {
//   const [posts, setPosts] = useState([]); // State to store fetched data

//   useEffect(() => {
//     axios
//       .get("http://127.0.0.1:5000/posts/first-image")
//       .then((response) => {
//         console.log("Fetched products:", response.data);
//         setPosts(response.data); // Set the data directly to state
//       })
//       .catch((error) => {
//         console.error("Error fetching products:", error);
//       });
//   }, []);

//   return (
//     <div>
//       <h1>Posts with Images</h1>
//       <ul>
//         {posts.map((post, index) => (
//           <li key={index}>
//             <h2>{post.title}</h2> {/* Access the title */}
//             <img src={post.first_image_url} alt={post.title} /> {/* Access the image URL */}
//           </li>
//         ))}
//       </ul>
//     </div>
//   );
// }

// export default PostsWithImages;
import React, { useEffect, useState } from "react";
import axios from "axios";

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
    <div>
      <h1>Shop</h1>
      <div className="carousel-items-wrapper">
        <div className="carousel-items-padding">
          <div className="item-inner">
            <a className="item-inner-link">
              {posts.map((post, index) => (
                <li key={index} style={{ marginBottom: "20px" }}>
                  <h2>{post.title}</h2> {/* Display the post title */}
                  <img
                    src={post.first_image_url}
                    alt={post.title}
                    style={{
                      maxWidth: "300px",
                      border: "1px solid #ccc",
                      borderRadius: "5px",
                      padding: "5px",
                    }}
                  />{" "}
                </li>
              ))}
            </a>
            <div className="item-heart-price"></div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default PostsWithImages;
