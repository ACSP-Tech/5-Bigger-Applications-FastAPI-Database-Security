from fastapi import APIRouter, HTTPException, status, Depends
from ..schema.job import JobApplication, JobApplicationOut
from ..dep import auth, get_session
from ..crud.job import create_jobapplication, get_user_jobapplication_filter, get_user_jobapplications
import json

router = APIRouter()

@router.post("/applications/", response_model=JobApplicationOut, status_code=status.HTTP_201_CREATED)
def create_user_note(data:JobApplication, session=Depends(get_session), token=Depends(auth)):
    try:
        #authenticate user and add to job application
        message = create_jobapplication(data, session, token)
        return message
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/applications/", status_code=status.HTTP_200_OK)
def view_notes(session=Depends(get_session), token=Depends(auth)):
    try:
        #authenticate user and add to student
        message = get_user_jobapplications(session, token)
        return message
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/applications/search", status_code=status.HTTP_200_OK)
def view_note(status:str, session=Depends(get_session), token=Depends(auth)):
    try:
        #authenticate user and add to student
        message = get_user_jobapplication_filter(status, session, token)
        return message
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))