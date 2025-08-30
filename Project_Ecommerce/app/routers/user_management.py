# to create route to be added to the fast api instance in respect to user details

# importing the necessary requirement
from fastapi import APIRouter, HTTPException, status, Depends
from ..schema.user_management import Register, RegisterOut, Login, Promote, PromoteOut
from ..sec import pwd_context
from app.utils import check_filepath
from ..dep import auth, get_session
from ..crud.user_management import create_user, get_token, user_logout, admin_can_promote
import json

router = APIRouter()


@router.post("/register", response_model=RegisterOut, status_code=status.HTTP_201_CREATED)
def registration(detail:Register, session=Depends(get_session)):
    try:
        file_path = check_filepath()
        #reading and loading json file
        with open(file_path, "r") as file:
            old_json = json.load(file)
        # hash password
        hashed_password = pwd_context.hash(detail.password)
        #logic to check if email already exist in db case insensitive
        res = create_user(detail, session, hashed_password)
        old_json[detail.email.lower().strip()] = res.model_dump()
        with open(file_path, "w") as file:
                json.dump(old_json, file)
        return res
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/login", status_code=status.HTTP_200_OK)
def login_user(detail:Login, session=Depends(get_session)):
    try:
        #get token
        res = get_token(detail, session)
        return res
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    
@router.patch("/promote-admin", status_code=status.HTTP_200_OK, response_model=PromoteOut)
def login_user(detail:Promote, session=Depends(get_session), token=Depends(auth)):
    try:
        #get token
        res = admin_can_promote(detail, session, token)
        return res
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/logout", status_code=status.HTTP_200_OK)
def logout(session=Depends(get_session), token=Depends(auth)):
    try:
        #get token
        message = user_logout(session, token)
        return message
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))