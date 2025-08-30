from fastapi import APIRouter, HTTPException, status, Depends
from ..schema.contact import Contact, ContactOut
from ..sec import pwd_context, SECRET_KEY, ALGORITHM
from app.utils import check_filepath
from ..dep import auth, get_session
from ..crud.contact import create_contact, get_user_contacts, update_user_contacts, delete_user_contact

router = APIRouter()

@router.post("/contacts/", response_model=ContactOut, status_code=status.HTTP_201_CREATED)
def create_user_contact(data:Contact, session=Depends(get_session), token=Depends(auth)):
    try:
        #authenticate user and add to student
        message = create_contact(data, session, token)
        return message
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/contacts/", status_code=status.HTTP_200_OK)
def view_contact(session=Depends(get_session), token=Depends(auth)):
    try:
        #authenticate user and add to student
        message = get_user_contacts(session, token)
        return message
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.put("/contacts/{id}", status_code=status.HTTP_200_OK)
def update_contact(id:int, data:Contact, session=Depends(get_session), token=Depends(auth)):
    try:
        #authenticate user and add to student
        message = update_user_contacts(id, data, session, token)
        return message
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.delete("/contacts/{id}", status_code=status.HTTP_200_OK)
def delete_contact(id:int,  session=Depends(get_session), token=Depends(auth)):
    try:
        #authenticate user and add to student
        message = delete_user_contact(id, session, token)
        return message
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))