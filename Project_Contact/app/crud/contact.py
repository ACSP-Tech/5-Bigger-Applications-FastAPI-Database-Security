from ..model.user_management import User, Contact
from ..sec import  SECRET_KEY, ALGORITHM
from fastapi import HTTPException, status
from sqlmodel import select 
from sqlalchemy import and_
import jwt

def create_contact(data, session, token):
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
        statement = select(Contact).where(and_(Contact.email == data.email, Contact.phone_number == data.phone_number, Contact.user_id == id))
        contact = session.exec(statement).first()  
        if contact:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="contact details for this phone number and email already exist"
            )  
        # Create student
        new_contact = Contact(name=data.name, phone_number=data.phone_number, email=data.email, user_id=id)
        session.add(new_contact)
        session.commit()
        session.refresh(new_contact)
        return new_contact
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create user: {str(e)}"
        )
    
def get_user_contacts(session, token):
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
        statement = select(Contact).where(Contact.user_id == id)
        user_contact  = session.exec(statement).all()   
        if not user_contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="no contact details on user id"
            )
        return user_contact
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch user info: {str(e)}"
        )

def update_user_contacts(id, data, session, token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        user_id = payload.get("id")
        #get a single user
        statement = select(User).where(User.email == email.lower().strip()).where(User.id == user_id) 
        user = session.exec(statement).first() #eexecute that takes in conditions .all()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            ) 
        statement = select(Contact).where(and_(Contact.user_id == user_id, Contact.id == id))
        user_contact  = session.exec(statement).first()
        if not user_contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="no contact details on user id and contact id"
            )
        user_contact.name = data.name.lower().strip()
        user_contact.phone_number = data.phone_number.lower().strip()
        user_contact.email = data.email.lower().strip()
        session.commit()
        session.refresh(user_contact)
        return user_contact
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user: {str(e)}"
        )
    
def delete_user_contact(id, session, token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        user_id = payload.get("id")
        #get a single user
        statement = select(User).where(User.email == email.lower().strip()).where(User.id == user_id)
        user = session.exec(statement).first() #eexecute that takes in conditions .all()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            ) 
        statement = select(Contact).where(and_(Contact.user_id == user_id, Contact.id == id))
        user_contact  = session.exec(statement).first()
        if not user_contact:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="no contact details on user id and contact id"
            )
        session.delete(user_contact)
        session.commit()
        res = {
            "message": f"contact  has been successfully deleted"
        }
        return res
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete user: {str(e)}"
        )