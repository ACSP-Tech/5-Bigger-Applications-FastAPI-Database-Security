FastAPI — Contact Management API

A small FastAPI application for user registration, authentication (JWT), and per-user contact management.
This README is generated from the app OpenAPI specification and includes quick usage examples.

Quick overview

OpenAPI: 3.1.0

Title: FastAPI

Version: 0.1.0

Key features

User registration (/register)

User login (/login) → returns a JWT access token

Protected routes using OAuth2 password flow (token in Authorization: Bearer <token>)

Logout (/logout) (protected)

Create / view / update / delete contacts for the logged-in user (/contacts/, /contacts/{id})

Request/response validation using Pydantic (email validation, phone validation)

How to run (development)

Install requirements (use your virtualenv):

pip install -r requirements.txt


Start the app with uvicorn (run from the package root where main:app is available):

uvicorn main:app --reload


API docs (interactive):

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

Authentication

This app uses OAuth2 password flow (token endpoint POST /login).
You must include the returned token on protected endpoints in the Authorization header:

Authorization: Bearer <token>

Endpoints (summary)
POST /register — Registration

Request body (Register):

{
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "password": "string"
}


Response (RegisterOut):

{
  "id": 1,
  "first_name": "first",
  "last_name": "last",
  "email": "user@example.com"
}

POST /login — Login

Request body (Login):

{
  "email": "user@example.com",
  "password": "string"
}


Response: JSON with token (example):

{
  "token": "<jwt>",
  "token_type": "bearer"
}


Use that token in Authorization for protected endpoints.

GET /logout — Logout (protected)

Invalidates/blacklists the token (implementation dependent).

Requires Authorization: Bearer <token>.

GET /contacts/ — View contacts (protected)

Returns list of contacts for the authenticated user.

Requires Authorization: Bearer <token>.

POST /contacts/ — Create user contact (protected)

Request body (Contact):

{
  "name": "chioma",
  "phone_number": "09068641485",
  "email": "ghjhkj@gmail.com"
}


Response (ContactOut):

{
  "id": 1,
  "name": "chioma",
  "phone_number": "09068641485",
  "email": "ghjhkj@gmail.com",
  "user_id": 2
}


Note — phone validation: the request schema enforces a phone pattern: ^\+?[0-9]{7,15}$ — optional leading +, digits only, length 7–15.

PUT /contacts/{id} — Update contact (protected)

Path param: id (integer)

Body: same shape as Contact (name, phone_number, email)

Requires authentication.

DELETE /contacts/{id} — Delete contact (protected)

Path param: id (integer)

Requires authentication.