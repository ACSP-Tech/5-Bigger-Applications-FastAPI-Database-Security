from ..model.user_management import User, JobApplication
from ..sec import  SECRET_KEY, ALGORITHM
from fastapi import HTTPException, status
from sqlmodel import select 
from sqlalchemy import and_
import jwt

def create_jobapplication(data, session, token):
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
        statement = select(JobApplication).where(and_(JobApplication.position == data.position, 
                                                      JobApplication.company == data.company,
                                                      JobApplication.date_applied == str(data.date_applied),  
                                                      JobApplication.user_id == id))
        job = session.exec(statement).first()  
        if job:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="job application already already exist"
            )  
        # Create student
        new_jobappl = JobApplication(company=data.company.lower().strip(), position=data.position.lower().strip(), date_applied=str(data.date_applied), status=data.status.lower().strip(), user_id=id)
        session.add(new_jobappl)
        session.commit()
        session.refresh(new_jobappl)
        return new_jobappl
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create job application: {str(e)}"
        )
    
def get_user_jobapplications(session, token):
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
        statement = select(JobApplication).where(JobApplication.user_id == id)
        user_jobappl  = session.exec(statement).all()   
        if not user_jobappl:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="user hasn't entered any job application yet"
            )
        return user_jobappl
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch job application info: {str(e)}"
        )
    
def get_user_jobapplication_filter(status, session, token):
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
        statement = select(JobApplication).where(and_(JobApplication.user_id == user_id, JobApplication.status == status))
        user_jobappl  = session.exec(statement).all()   
        if not user_jobappl:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="no such status of job application not found for this user"
            )
        return user_jobappl
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch job application info: {str(e)}"
        )