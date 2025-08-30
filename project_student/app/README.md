🎓 Student Management API

A FastAPI-based RESTful API for handling user authentication, student records, and grades.
This API allows users to register, log in, create and update student records, add grades, and manage student information securely.

🚀 Features

User registration, login, and logout with OAuth2 password-based authentication.

Create, update, and delete student records.

Add, update, and delete grades for students.

View student details and associated grades.

Fully documented using OpenAPI/Swagger (/docs).

🛠️ Tech Stack

FastAPI (Python 3.9+)

OAuth2 with PasswordBearer flow

Pydantic for data validation

SQLite/Postgres (configurable database)

Uvicorn as ASGI server

📦 Installation

Clone the repo:

git clone https://github.com/your-username/student-management-api.git
cd student-management-api


Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows


Install dependencies:

pip install -r requirements.txt


Run the server:

uvicorn main:app --reload


API will be available at:

http://127.0.0.1:8000

🔐 Authentication

This project uses OAuth2 password flow.

Obtain a token via /login.

Include the token in subsequent requests:

Authorization: Bearer <your_token>

📖 API Endpoints
🔑 Auth

POST /register → Register a new user

POST /login → Login and get access token

GET /logout → Logout user

👨‍🎓 Students

POST /students/create-student → Create student with grades

PATCH /students/update-student-info/{studentid} → Update student record

GET /students/view-student → View all students

GET /students/view-student-grade/{studentid} → View grades of a student

DELETE /students/delete-student-grade-info/{studentid} → Delete a student record

📊 Grades

POST /students/add-grade/{studentid} → Add grade to a student

PATCH /students/update-student-grade-info/{studentid} → Update grade record

📂 Example Request
Register a new user
POST /register
Content-Type: application/json

{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john@example.com",
  "password": "securepassword"
}

Create a student
POST /students/create-student
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Jane Student",
  "age": 20,
  "email": "jane@student.com",
  "grades": [
    {"subject": "Math", "score": 95},
    {"subject": "English", "score": 88}
  ]
}

Update student info
PATCH /students/update-student-info/1
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "Jane Updated",
  "age": 21
}