from fastapi.security import OAuth2PasswordBearer
from .crud.user_management import is_blacklisted
from fastapi import Depends, HTTPException, status
from sqlmodel import Session
from .database_setup import connection
import jwt

def get_session():
    with Session(connection) as session:
        yield session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def auth(token=Depends(oauth2_scheme), session=Depends(get_session)):
    try: 
        is_blacklisted(token, session)
        return token
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token already expired")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))