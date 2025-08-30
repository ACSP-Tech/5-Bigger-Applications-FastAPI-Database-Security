#importing the necessary requirement
from fastapi import HTTPException, status
from .database_setup import connection
from sqlmodel import SQLModel
import os
import json

#function to handling filepath exceptions and creation if necessary
def check_filepath():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    try:
        file_path1 = os.path.join(BASE_DIR, "users.json")
        if not os.path.exists(file_path1):
            with open(file_path1, "x") as file:
                json.dump({}, file)
        return file_path1
    except:
       raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Error Creating Json file")
    

def create_db_and_tables():
    SQLModel.metadata.create_all(connection) ##each time we start a server create the  new table if needed