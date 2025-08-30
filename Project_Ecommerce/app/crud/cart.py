from ..model.user_management import User, Order, Cart
from ..sec import  SECRET_KEY, ALGORITHM
from fastapi import HTTPException, status
from sqlmodel import select 
from sqlalchemy import and_
import jwt

def create_cart_items(data, token, session):
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
        statement = select(Cart).where(and_(Cart.name == data.name.lower().strip(), Cart.user_id == id))
        cart_item = session.exec(statement).first() #eexecute that takes in conditions .all()
        # Create product
        new_cart = cart_item(name=data.name.lower().strip(), price=data.price, quantity=data.quantity, user_id = id)
        session.add(new_cart)
        session.commit()
        session.refresh(new_cart)
        return new_cart
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update note: {str(e)}"
        )    

def check_out_cart(session, token):
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
        statement = select(Cart).where(and_(Cart.user_id == id))
        cart = session.exec(statement).all()  
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="not cart items found to check out for this user"
            )
        for item in cart:
            new_order = Order(name=item.name, price=item.price, quantity=item.quantity, cart_id=item.id, amount=item.amount)        
        #special function that add to a table
        session.add(new_order)
        session.delete(cart)
        session.commit()
        session.refresh(new_order)
        return new_order
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
