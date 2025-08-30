#main application logic 

#importing the necessary nequirement
from fastapi import Request, FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from datetime import datetime
from .routers import user_management, contact
from .utils import create_db_and_tables

# Configure logging
logging.basicConfig(
    filename="requests.log",          # log file name
    level=logging.INFO,               # log level
    format="%(message)s"  # log format
)

#calling an instance of fast api
app = FastAPI()

#Allow CORS for http://localhost:3000 (frontend).
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:8000"
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
app.include_router(contact.router)


# Middleware to log IP address of every request
@app.middleware("http")
async def log_ip_address(request: Request, call_next):
    client_ip = request.client.host if request.client else "unknown"
    logging.info(f"Client IP: {client_ip}")
    response = await call_next(request)
    return response