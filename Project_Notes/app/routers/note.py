from fastapi import APIRouter, HTTPException, status, Depends
from ..schema.note import Note, NoteOut
from ..dep import auth, get_session
from app.utils import check_notepath
from ..crud.note import create_note, get_user_notes, get_user_note_single, update_user_note, delete_user_note
import json

router = APIRouter()

@router.post("/notes/", response_model=NoteOut, status_code=status.HTTP_201_CREATED)
def create_user_note(data:Note, session=Depends(get_session), token=Depends(auth)):
    try:
        file_path = check_notepath()
        #reading and loading json file
        with open(file_path, "r") as file:
            old_json = json.load(file)
        #authenticate user and add to student
        message = create_note(data, session, token)
        old_json[data.title.lower().strip()] = message.model_dump()
        with open(file_path, "w") as file:
                json.dump(old_json, file)
        return message
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/notes/", status_code=status.HTTP_200_OK)
def view_notes(session=Depends(get_session), token=Depends(auth)):
    try:
        #authenticate user and add to student
        message = get_user_notes(session, token)
        return message
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.get("/notes/{id}", status_code=status.HTTP_200_OK)
def view_note(id:int, session=Depends(get_session), token=Depends(auth)):
    try:
        #authenticate user and add to student
        message = get_user_note_single(id, session, token)
        return message
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.patch("/notes/{id}", status_code=status.HTTP_200_OK)
def update_note(id:int, data:Note, session=Depends(get_session), token=Depends(auth)):
    try:
        file_path = check_notepath()
        #reading and loading json file
        with open(file_path, "r") as file:
            old_json = json.load(file)
        #authenticate user and add to student
        message = update_user_note(id, data, session, token)
        old_json[data.title.lower().strip()] = message.model_dump()
        with open(file_path, "w") as file:
                json.dump(old_json, file)
        return message
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.delete("/notes/{id}", status_code=status.HTTP_200_OK)
def delete_note(id:int, session=Depends(get_session), token=Depends(auth)):
    try:
        #authenticate user and add to student
        message = delete_user_note(id, session, token)
        return message
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))