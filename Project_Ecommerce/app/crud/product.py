from ..model.user_management import User, Product
from ..sec import  SECRET_KEY, ALGORITHM
from fastapi import HTTPException, status
from sqlmodel import select 
from sqlalchemy import and_
import jwt

def create_product(data, token, session):
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
        if user.role != "admin":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Admins only")
        statement = select(Product).where(and_(Product.name == data.name.lower().strip()))
        product = session.exec(statement).first() #eexecute that takes in conditions .all()
        if product:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="product name already exist"
            ) 
        # Create product
        new_product = product(name=data.name.lower().strip(), price=data.price, stock=data.stock)
        session.add(new_product)
        session.commit()
        session.refresh(new_product)
        return new_product
    except Exception as e:
        session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update note: {str(e)}"
        )    

def view_products(session):
    try:
        statement = select(Product)
        products = session.exec(statement).all()#eexecute that takes in conditions .all()
        if not products:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="comming soon!!!, no product exist yet"
            )
        return products
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))