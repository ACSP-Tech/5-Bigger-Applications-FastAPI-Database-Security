from fastapi import APIRouter, HTTPException, status, Depends
from ..schema.product import Product, ProductOut
from ..dep import auth, get_session
from ..crud.product import create_product, view_products
import json

router = APIRouter()

@router.post("/admin/products/", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_user_note(data:Product, session=Depends(get_session), token=Depends(auth)):
    try:
        message = create_product(data, session, token)
        return message
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/products/", status_code=status.HTTP_200_OK)
def view_notes(session=Depends(get_session)):
    try:
        #authenticate user and add to student
        message = view_products(session)
        return message
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))