# CONWAY'S GOODS

An e-commerce platform for selling designer fashion items, integrating authentication, payment processing, and AWS S3 storage.

## Tech Stack

- **Backend**: Flask (Python), PostgreSQL
- **Frontend**: React (TypeScript), Vite
- **Styling**: CSS Modules
- **Storage**: AWS S3
- **Authentication**: Custom authentication system with JWT
- **Payments**: PayPal integration

## Installation

### Prerequisites

- Python 3
- npm
- PostgreSQL

### Setup Instructions

#### Backend Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/RowanHall/conways-goods
   cd conways-goods
   ```
2. **Set up a virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
4. **Set up environment variables**:
   - Create a `.env` file in the root directory.
   - Add the necessary database and AWS credentials (refer to `config.py`).
5. **Initialize the database**:
   ```bash
   python db.py
   ```
6. **Run the backend server**:
   ```bash
   python run.py
   ```

#### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```
2. **Install dependencies**:
   ```bash
   npm install
   ```
3. **Run the development server**:
   ```bash
   npm run dev
   ```

## Project Structure

```
project_root/
│── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── auth.py
│   │   │   ├── payments.py
│   │   │   ├── posts.py
│   │   │   ├── s3.py
│   │   ├── services/
│   │   │   ├── auth_service.py
│   │   │   ├── payments_service.py
│   │   │   ├── post_service.py
│   │   │   ├── s3_service.py
│   │   │   ├── utils/
│   │   │   │   ├── db.py
│   │   │   ├── __init__.py
│   │   ├── extensions.py
│   │   ├── __init__.py
│   ├── config.py
│   ├── run.py
│   ├── requirements.txt
│── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AdminPanel/
│   │   │   ├── Bottom/
│   │   │   ├── Carousel/
│   │   │   ├── CreatePostForm/
│   │   │   ├── DeletePost/
│   │   │   ├── Login/
│   │   │   ├── Navbar/
│   │   │   ├── PayPalCheckout/
│   │   │   ├── PostDisplayWrap/
│   │   │   ├── ProtectedRoute/
│   │   │   ├── Video/
│   │   ├── context/
│   │   │   ├── AuthContext.tsx
│   │   │   ├── CartContext.tsx
│   │   ├── pages/
│   │   │   ├── Cart/
│   │   │   ├── Home/
│   │   │   ├── Post/
│   │   │   ├── Shop/
│   │   ├── styles/
│   │   ├── App.tsx
│   │   ├── index.css
│   │   ├── main.tsx
│   ├── public/
```

## API Endpoints

### Authentication

- `POST /auth/login` - Login a user
- `POST /auth/register` - Register a new user
- `GET /auth/me` - Get current user

### Posts

- `GET /posts/first-image` - Fetch all post previews
- `GET /posts/:id` - Fetch a post by ID
- `POST /posts/create` - Create a new post (Admin only)
- `DELETE /posts/delete/:id` - Delete a post (Admin only)

### Payments

- `POST /payments/capture` - Process a payment

### AWS S3 Storage

- `GET /s3/presigned-url` - Get a presigned URL for uploading a file to S3

## Frontend Features

- **React Router** for navigation
- **Protected Routes** for admin panel
- **Context API** for state management (Authentication & Cart)
- **Axios** for API requests
- **PayPal Integration** for payments
- **Carousel Component** for displaying products
- **Responsive UI** with CSS modules

## Contributors

- Rowan Hall
