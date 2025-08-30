FastAPI Job Application API

This is a FastAPI application for managing job applications, user registration, and login. It allows users to apply for jobs, view applications, and search for applications based on their status.

Features

User Registration: Register a new user with first_name, last_name, email, and password.

Login: Login with email and password to receive a JWT token for authentication.

Job Applications: Users can create job applications, view their applications, and search for applications by status.

Security: OAuth2 Password Bearer token authentication for accessing protected routes.

Requirements

Install dependencies:

pip install -r requirements.txt

Running the Application
uvicorn main:app --reload


The API docs will be available at:

Swagger UI → http://127.0.0.1:8000/docs

ReDoc → http://127.0.0.1:8000/redoc

Endpoints
POST /register — Register a new user
Request Body (Register):
{
  "first_name": "string",
  "last_name": "string",
  "email": "user@example.com",
  "password": "string"
}

Response (RegisterOut):
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "email": "user@example.com"
}

POST /login — Login user
Request Body (Login):
{
  "email": "user@example.com",
  "password": "string"
}

Response:
{
  "token": "<jwt>",
  "token_type": "bearer"
}


Use this token in Authorization header for other endpoints.

GET /logout — Logout (protected)

Invalidates the JWT token.

Requires Authorization: Bearer <token>.

GET /applications/ — View applications (protected)

Get a list of job applications for the authenticated user.

Requires Authorization: Bearer <token>.

POST /applications/ — Create a new job application (protected)
Request Body (JobApplication):
{
  "company": "Company Name",
  "position": "Job Position",
  "date_applied": "2025-08-30",
  "status": "pending"
}

Response (JobApplicationOut):
{
  "id": 1,
  "company": "Company Name",
  "position": "Job Position",
  "date_applied": "2025-08-30",
  "status": "pending",
  "user_id": 2
}

GET /applications/search — Search job applications by status (protected)
Query Parameter (status):

Status of the job application (e.g., "pending", "approved").

Response:
[
  {
    "id": 1,
    "company": "Company Name",
    "position": "Job Position",
    "date_applied": "2025-08-30",
    "status": "pending",
    "user_id": 2
  }
]

Error Responses

400 Bad Request: Missing User-Agent header (handled by middleware).

401 Unauthorized: Invalid or expired JWT token.

404 Not Found: Resource (e.g., user, application) not found.

409 Conflict: Job application already exists.

422 Unprocessable Entity: Validation errors.

500 Internal Server Error: Server issues or unexpected errors.

Project Structure
.
├── app/
│   ├── main.py                # FastAPI entrypoint
│   ├── routers/               # Routes for user management, job applications, etc.
│   ├── models/                # SQLAlchemy models
│   ├── schema/                # Pydantic models for data validation
│   ├── utils/                 # Utility functions (e.g., database initialization)
│   └── crud/                  # CRUD operations
├── requirements.txt           # Project dependencies
└── README.md                  # Project documentation

Authentication

This app uses OAuth2 password flow for login. The POST /login endpoint returns a JWT token.
For protected routes, include the token in the Authorization header:

Authorization: Bearer <your-token-here>

Notes

For a production system, consider using a more secure storage for the JWT tokens (e.g., cookies with HttpOnly and Secure flags).

Use proper validation and hashing for passwords (e.g., bcrypt or passlib).