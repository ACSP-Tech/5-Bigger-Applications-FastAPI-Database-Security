from ..model.user_management import User, Order, Cart
from ..sec import  SECRET_KEY, ALGORITHM
from fastapi import HTTPException, status
from sqlmodel import select 
from sqlalchemy import and_
from datetime import date
import jwt

def create_cart_items(data, session, token):
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
        new_cart = Cart(name=data.name.lower().strip(), price=data.price, quantity=data.quantity, product_id=data.product_id, user_id = id, created_at=str(date.today()), amount=data.price*data.quantity)
        session.add(new_cart)
        session.commit()
        session.refresh(new_cart)
        return new_cart
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to add to cart: {str(e)}"
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
        statement = select(Cart).where(Cart.user_id == id)
        cart = session.exec(statement).all()  
        if not cart:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="not cart items found to check out for this user"
            )
        new_orders = []
        for item in cart:
            new_order = Order(
                name=item.name,
                price=item.price,
                quantity=item.quantity,
                cart_id=item.id,
                user_id =item.user_id,
                amount=item.amount,
                created_at=str(date.today())
            )
            session.add(new_order)
            session.delete(item)  # delete each item separately
            new_orders.append(new_order)
        session.commit()
        # refresh all new orders
        for order in new_orders:
            session.refresh(order)
        return new_orders
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
