📝 Notes API (FastAPI)

A simple Notes API built with FastAPI that provides authentication and CRUD operations for managing user notes.

🚀 Features

User Authentication

Register new users

Login with email & password

Logout with token invalidation

Notes Management (Authenticated)

Create personal notes

View all your notes

Retrieve a single note

Update a note

Delete a note

📦 Tech Stack

FastAPI
 – modern, fast web framework

SQLModel
 – SQL + Pydantic + SQLAlchemy ORM

JWT
 – authentication

SQLite (default, can be swapped with PostgreSQL/MySQL)

📖 API Endpoints
🔑 Authentication
Register a new user

POST /register
Request Body:

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "secret123"
}


Response:

{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com"
}

Login

POST /login
Request Body:

{
  "email": "john@example.com",
  "password": "secret123"
}


Response:

{
  "access_token": "<jwt_token>",
  "token_type": "bearer"
}

Logout

GET /logout
Headers:
Authorization: Bearer <token>
Response:

{ "message": "Logged out successfully" }

📝 Notes

(All notes endpoints require authentication with a Bearer token)

Get all notes

GET /notes/
Response:

[
  {
    "id": 1,
    "title": "first note",
    "content": "This is my first note",
    "created_at": "2025-08-30",
    "user_id": 1
  }
]

Create a new note

POST /notes/
Request Body:

{
  "title": "shopping list",
  "content": "milk, eggs, bread"
}


Response:

{
  "id": 2,
  "title": "shopping list",
  "content": "milk, eggs, bread",
  "created_at": "2025-08-30",
  "user_id": 1
}

Get a note by ID

GET /notes/{id}

Update a note

PATCH /notes/{id}
Request Body:

{
  "title": "updated title",
  "content": "updated content"
}

Delete a note

DELETE /notes/{id}

⚙️ Setup & Installation

Clone repo

git clone https://github.com/yourusername/notes-api.git
cd notes-api


Create virtual environment

python -m venv venv
source venv/bin/activate   # (Linux/Mac)
venv\Scripts\activate      # (Windows)


Install dependencies

pip install -r requirements.txt


Run server

uvicorn main:app --reload


Open docs in browser:

Swagger UI → http://127.0.0.1:8000/docs

ReDoc → http://127.0.0.1:8000/redoc

🔐 Authentication Flow

Register → Login → Get Token → Use Authorization: Bearer <token> header for protected routes.