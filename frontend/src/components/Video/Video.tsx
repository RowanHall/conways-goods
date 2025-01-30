// import "./Video.css";
// // import "../../styles/base.css";
// import { Link } from "react-router-dom";

// export default function Video() {
//   return (
//     <>
//       <div className="banner">
//         <video className="banner-video">
//           autoPlay muted loop playsInline
//           <source
//             src="https://my-app-images44.s3.us-east-2.amazonaws.com/test/videobanner.mp4"
//             type="video/mp4"
//           />
//           Your browser does not support the video tag.
//         </video>
//         <div className="banner-content">
//           <h1>THE PLATFORM FOR PERSONAL STYLE</h1>
//           <p>
//             Buy, sell, discover authenticated pieces from the world's top
//             brands.
//           </p>
//           <div className="cta-buttons">
//             <Link to="/shop" className="video-banner-button">
//               SHOP NOW
//             </Link>
//             <Link to="/brands" className="video-banner-button">
//               BRANDS
//             </Link>
//           </div>
//         </div>
//       </div>
//     </>
//   );
// }
import "./Video.css";
// import "../../styles/base.css";
import { Link } from "react-router-dom";

export default function Video() {
  return (
    <>
      <div className="banner">
        <video className="banner-video" autoPlay muted loop playsInline>
          <source
            src="https://my-app-images44.s3.us-east-2.amazonaws.com/test/videobanner.mp4"
            type="video/mp4"
          />
          Your browser does not support the video tag.
        </video>
        <div className="banner-content">
          <h1>THE PLATFORM FOR PERSONAL STYLE</h1>

          <p>
            Buy, sell, discover authenticated pieces
            <br />from the world's top brands.
          </p>

          <div className="cta-buttons">
            <Link to="/shop" className="video-banner-button">
              SHOP NOW
            </Link>
            <Link to="/brands" className="video-banner-button">
              BRANDS
            </Link>
          </div>
        </div>
      </div>
    </>
  );
}
