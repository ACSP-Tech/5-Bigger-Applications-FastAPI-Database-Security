from ..model.user_management import User, Note
from ..sec import  SECRET_KEY, ALGORITHM
from fastapi import HTTPException, status
from sqlmodel import select 
from sqlalchemy import and_
import jwt

def create_note(data, session, token):
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
        statement = select(Note).where(and_(Note.title == data.title, Note.user_id == id))
        note = session.exec(statement).first()  
        if note:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="note title already exist"
            )  
        # Create student
        new_note = note(name=data.title.lower().strip(), content=data.content, user_id=id)
        session.add(new_note)
        session.commit()
        session.refresh(new_note)
        return new_note
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create note: {str(e)}"
        )
    
def get_user_notes(session, token):
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
        statement = select(Note).where(Note.user_id == id)
        user_notes  = session.exec(statement).all()   
        if not user_notes:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user hasn't entered any note yet"
            )
        return user_notes
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch note info: {str(e)}"
        )
    
def get_user_note_single(id, session, token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        user_id = payload.get("id")
        #get a single user
        statement = select(User).where(and_(User.email == email, User.id == user_id)) 
        user = session.exec(statement).first() #eexecute that takes in conditions .all()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            ) 
        statement = select(Note).where(and_(Note.user_id == user_id, Note.id == id))
        user_note  = session.exec(statement).all()   
        if not user_note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="note not found for this user"
            )
        return user_note
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch note info: {str(e)}"
        )

def update_user_note(id, data, session, token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        user_id = payload.get("id")
        #get a single user
        statement = select(User).where(and_(User.email == email, User.id == user_id))
        user = session.exec(statement).first() #eexecute that takes in conditions .all()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            ) 
        statement = select(Note).where(and_(Note.user_id == user_id, Note.id == id))
        user_note  = session.exec(statement).first()
        if not user_note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="no note details found for this user matching the id passed"
            )
        user_note.title = data.title.lower().strip()
        user_note.content = data.content
        session.commit()
        session.refresh(user_note)
        return user_note
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update note: {str(e)}"
        )
    
def delete_user_note(id, session, token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("email")
        user_id = payload.get("id")
        #get a single user
        statement = select(User).where(and_(User.email == email, User.id == user_id)) 
        user = session.exec(statement).first() #eexecute that takes in conditions .all()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            ) 
        statement = select(Note).where(and_(Note.user_id == user_id, Note.id == id))
        user_note  = session.exec(statement).first()
        if not user_note:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="no such note id for this user"
            )
        session.delete(user_note)
        session.commit()
        res = {
            "message": f"note has been successfully deleted"
        }
        return res
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete note: {str(e)}"
        )