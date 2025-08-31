🛒 E-Commerce API (FastAPI)

This project is a FastAPI-based E-Commerce REST API that provides endpoints for user authentication, product management, cart management, and checkout.
It is secured with OAuth2 password flow and allows role-based access for admins and users.

🚀 Features

User Management

Register new users

Login & Logout

Promote users to admin role

Product Management (Admin only)

Create products

View products

Shopping Cart

Add products to cart

Checkout cart

📂 Project Structure
.
├── app/
│   ├── main.py           # FastAPI entry point
│   ├── models.py         # Database models
│   ├── schemas.py        # Pydantic schemas
│   ├── routes/           # API endpoints
│   └── auth.py           # Authentication & security
├── requirements.txt
└── README.md

⚙️ Installation & Setup

Clone the repository

git clone https://github.com/yourusername/ecommerce-api.git
cd ecommerce-api


Create and activate a virtual environment

python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate      # On Windows


Install dependencies

pip install -r requirements.txt


Run the FastAPI server

uvicorn app.main:app --reload


Open API Docs

Swagger UI → http://localhost:8000/docs

ReDoc → http://localhost:8000/redoc

🔑 Authentication

This API uses OAuth2 Password Bearer authentication.

To authenticate, first login with your email & password at /login.

You will receive a JWT access token.

Include the token in the Authorization header for protected routes:

Authorization: Bearer <your_token_here>

📌 API Endpoints
👤 User Endpoints

POST /register → Register a new user

POST /login → Login and get access token

PATCH /promote-admin → Promote a user to admin (Admin only)

GET /logout → Logout user

📦 Product Endpoints

POST /admin/products/ → Create a new product (Admin only)

GET /products/ → View all products

🛒 Cart & Order Endpoints

POST /cart/add/ → Add product to cart

POST /cart/checkout/ → Checkout user cart

📑 Schemas
User

Register

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "securepassword"
}


RegisterOut

{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com"
}

Product

Product

{
  "name": "Sneakers",
  "price": 49.99,
  "stock": 100
}


ProductOut

{
  "id": 1,
  "name": "Sneakers",
  "price": 49.99,
  "stock": 100
}

Cart

Cart

{
  "product_id": 1,
  "name": "Sneakers",
  "price": 49.99,
  "quantity": 2
}


CartOut

{
  "id": 1,
  "name": "Sneakers",
  "price": 49.99,
  "quantity": 2,
  "amount": 99.98,
  "created_at": "2025-08-30T10:00:00Z"
}

Order

Order

{
  "id": 1,
  "name": "Sneakers",
  "price": 49.99,
  "amount": 99.98,
  "cart_id": 1,
  "created_at": "2025-08-30T10:05:00Z"
}

🛠️ Tech Stack

FastAPI (API framework)

Pydantic (data validation)

OAuth2 + JWT (authentication)

SQLAlchemy / Database (persistence)

Uvicorn (ASGI server)