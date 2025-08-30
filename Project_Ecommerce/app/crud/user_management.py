#for managing CRUD interaction with the database in respect to users details

#importing the necessary requirement
from ..model.user_management import User, Blacklist
from sqlmodel import select
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from ..sec import pwd_context, SECRET_KEY, ALGORITHM
from datetime import datetime, timedelta
import jwt
from sqlalchemy import and_

def create_user(data, session, hashed):
    try:
        #get a single user
        statement = select(User).where(User.email == data.email.lower().strip()) 
        user = session.exec(statement).first()
        #automatic admin seeding logic
        role_assign = "admin" if not user else "customer"
        #create the instance of the table, alongside the information
        new_user = User(first_name = data.first_name.lower().strip(),
            last_name = data.last_name.lower().strip(),
            email = data.email.lower().strip(),
            password = hashed,
            role = role_assign
            )
        #special function that add to a table
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    except IntegrityError:  # e.g., duplicate email
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists."
        )
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )

def get_token(data, session):
    try:
        #get a single user
        statement = select(User).where(User.email == data.email.lower().strip()) 
        user = session.exec(statement).first() #eexecute that takes in conditions .all()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        if not pwd_context.verify(data.password, user.password):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Invalid password")
        #generate token
        payload = {
            "exp": datetime.utcnow() + timedelta(minutes=180),
            "id": user.id,
            "email": user.email,
            "role": user.role
            }
        token = jwt.encode(payload=payload, key=SECRET_KEY, algorithm=ALGORITHM)
        res = {
            "token" : token,
            "token_type" : "bearer"
        }
        return res
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
def admin_can_promote(data, token, session):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        id = payload.get("id")
        role = payload.get("role")
        #get a single user
        statement = select(User).where(and_(User.email == email, User.id == id, User.role == role))
        user = session.exec(statement).first() #eexecute that takes in conditions .all()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        if user.role != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only")
        statement = select(User).where(and_(User.id == data.id, User.email == data.email))
        new_admin = session.exec(statement).first() #eexecute that takes in conditions .all()
        if not new_admin:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        new_admin.role = "admin"
        session.commit()
        session.refresh(new_admin)
        return new_admin
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update note: {str(e)}"
        )    
        

def user_logout(session, token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        id = payload.get("id")
        #get a single user
        statement = select(User).where(and_(User.email == email, User.id == id))
        user = session.exec(statement).first() #eexecute that takes in conditions .all()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        new_blacklist = Blacklist(black_token = token)
        #special function that add to a table
        session.add(new_blacklist)
        session.commit()
        session.refresh(new_blacklist)
        return {"msg": f"User with {email} with id {id} successfully logged out"}
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    

def is_blacklisted(token, session)-> bool:
    try:
        #get a single user
        statement = select(Blacklist).where(Blacklist.black_token == token) 
        black_token = session.exec(statement).first()
        if black_token:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Token already blacklisted"
            )
        return False
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))