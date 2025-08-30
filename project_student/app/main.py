#main application logic 

#importing the necessary nequirement
from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime
from .routers import user_management, student
from .utils import create_db_and_tables

# Configure logging
logging.basicConfig(
    filename="requests.log",          # log file name
    level=logging.INFO,               # log level
    format="%(asctime)s - %(levelname)s - %(message)s"  # log format
)

#calling an instance of fast api
app = FastAPI()

#Allow CORS for http://localhost:3000 (frontend).
origins = [
    "http://localhost:3000",
    "http://localhost:8000"
]

#definiing the cors function
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_headers = ["*"],
    allow_methods = ["*"]
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(user_management.router)
app.include_router(student.router)

#middleware to to log every request into a log file.
@app.middleware("http")
def log_request_func(request:Request, call_next):
    #logging request
    user = request.headers.get("user", "anonymous")
    log_message = f"User: {user} | Method: {request.method} | Path: {request.url.path}"
    logging.info(log_message)  # Write log entry to requests.log
    #continue with request
    response = call_next(request)
    return response