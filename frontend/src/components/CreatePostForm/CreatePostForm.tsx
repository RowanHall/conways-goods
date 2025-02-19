import React, { useState } from "react";
import axios from "axios";
import "./CreatePostForm.css";

// Define category and designer options
const CATEGORIES = [
  "Tops",
  "Bottoms",
  "Outerwear",
  "Accessories",
  "Footwear",
  "Other",
];

const DESIGNERS = ["Nike", "Adidas", "Stussy", "Supreme", "Palace", "Other"];

const CreatePostForm = () => {
  const [formData, setFormData] = useState({
    title: "",
    price: "",
    description: "",
    category: "",
    designer: "",
  });
  const [files, setFiles] = useState<File[]>([]);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [uploading, setUploading] = useState(false);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const filesArray = Array.from(e.target.files);
      setFiles(filesArray);
    }
  };

  const uploadToS3 = async (file: File): Promise<string> => {
    try {
      if (!file || !(file instanceof File)) {
        throw new Error("Invalid file object");
      }

      console.log("Starting upload for file:", {
        name: file.name,
        type: file.type,
        size: file.size,
      });

      const response = await axios.get(
        `http://localhost:5005/api/s3/presigned-url`,
        {
          params: {
            filename: file.name,
            contentType: file.type,
          },
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
          },
        }
      );

      const { url, fields } = response.data;
      console.log("Received presigned URL data:", { url, fields });

      const formData = new FormData();

      // Add all fields from the presigned URL first
      Object.entries(fields).forEach(([key, value]) => {
        formData.append(key, value as string);
        console.log(`Adding field: ${key} = ${value}`);
      });

      // Add the file last
      formData.append("file", file);

      console.log("Uploading to S3...", { url });

      const uploadResponse = await fetch(url, {
        method: "POST",
        body: formData,
      });

      if (!uploadResponse.ok) {
        const errorText = await uploadResponse.text();
        console.error("S3 Upload Error:", errorText);
        throw new Error(
          `Upload failed: ${uploadResponse.status} ${uploadResponse.statusText}`
        );
      }

      // Construct the final URL
      const fileUrl = `https://${fields.bucket}.s3.amazonaws.com/${fields.key}`;
      console.log("Upload successful. File URL:", fileUrl);

      return fileUrl;
    } catch (error: any) {
      console.error("Upload error details:", {
        error: error.response?.data || error.message,
        status: error.response?.status,
        headers: error.response?.headers,
      });
      throw new Error(`Failed to upload to S3: ${error.message}`);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setUploading(true);
    setError("");

    try {
      // Upload all images to S3 and get their URLs
      const imageUrls = await Promise.all(
        files.map((file) => uploadToS3(file))
      );

      // Create post with image URLs
      const response = await axios.post(
        "http://localhost:5005/api/posts/create",
        {
          ...formData,
          price: parseFloat(formData.price),
          images: imageUrls,
        }
      );

      setSuccess(true);
      setFormData({
        title: "",
        price: "",
        description: "",
        category: "",
        designer: "",
      });
      setFiles([]);
    } catch (error) {
      setError("Failed to create post");
      console.error("Error:", error);
    } finally {
      setUploading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="create-post-form">
      {error && <div className="error-message">{error}</div>}
      {success && (
        <div className="success-message">Post created successfully!</div>
      )}

      <div className="form-group">
        <label>Title</label>
        <input
          type="text"
          value={formData.title}
          onChange={(e) => setFormData({ ...formData, title: e.target.value })}
          required
        />
      </div>

      <div className="form-group">
        <label>Price</label>
        <input
          type="number"
          value={formData.price}
          onChange={(e) => setFormData({ ...formData, price: e.target.value })}
          required
        />
      </div>

      <div className="form-group">
        <label>Description</label>
        <textarea
          value={formData.description}
          onChange={(e) =>
            setFormData({ ...formData, description: e.target.value })
          }
        />
      </div>

      <div className="form-group">
        <label>Category</label>
        <select
          value={formData.category}
          onChange={(e) =>
            setFormData({ ...formData, category: e.target.value })
          }
          required
        >
          <option value="">Select a category</option>
          {CATEGORIES.map((category) => (
            <option key={category} value={category}>
              {category}
            </option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label>Designer</label>
        <select
          value={formData.designer}
          onChange={(e) =>
            setFormData({ ...formData, designer: e.target.value })
          }
          required
        >
          <option value="">Select a designer</option>
          {DESIGNERS.map((designer) => (
            <option key={designer} value={designer}>
              {designer}
            </option>
          ))}
        </select>
      </div>

      <div className="form-group">
        <label>Images</label>
        <input
          type="file"
          multiple
          accept="image/*"
          onChange={handleFileChange}
          className="file-input"
        />
        <div className="selected-files">
          {files.map((file, index) => (
            <div key={index} className="file-name">
              {file.name}
            </div>
          ))}
        </div>
      </div>

      <button
        type="submit"
        disabled={uploading}
        className={uploading ? "uploading" : ""}
      >
        {uploading ? "Creating Post..." : "Create Post"}
      </button>
    </form>
  );
};

export default CreatePostForm;
