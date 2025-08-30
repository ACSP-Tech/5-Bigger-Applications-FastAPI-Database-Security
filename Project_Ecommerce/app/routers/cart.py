from fastapi import APIRouter, HTTPException, status, Depends
from ..schema.cart import Cart, CartOut, Order
from ..dep import auth, get_session
from ..crud.cart import create_cart_items, check_out_cart
import json
from typing import List

router = APIRouter()

@router.post("/cart/add/", response_model=CartOut, status_code=status.HTTP_201_CREATED)
def create_user_cart(data:Cart, session=Depends(get_session), token=Depends(auth)):
    try:
        message = create_cart_items(data, session, token)
        return message
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.post("/cart/checkout/", response_model=List[Order], status_code=status.HTTP_201_CREATED)
def checkout_user_cart(session=Depends(get_session), token=Depends(auth)):
    try:
        message = check_out_cart(session, token)
        return message
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))