import "./Post.css";
import { useParams } from "react-router-dom";

export default function PostPage() {
  const { postId } = useParams(); // Get post ID from the URL
  // const { postId } = useParams();

  // TO-DO: Fetch the post from the backend

  //const post = posts[postId];

  // return post ? (
  //   <div>
  //     <h1>{post.title}</h1>
  //     <p>{post.content}</p>
  //   </div>
  // ) : (
  //   <h1>Post Not Found</h1>
  // );

  return (
    <>
      <div>
        <h1>Post ID: {postId}</h1>
        <p>Displaying details for post {postId}...</p>
      </div>
    </>
  );
}
